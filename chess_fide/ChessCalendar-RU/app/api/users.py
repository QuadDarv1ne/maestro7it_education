"""
API endpoints для управления пользователями
"""
from flask import Blueprint, request, jsonify, g
from app import db
from app.models.user import User
from app.middleware.security_middleware import require_api_key, require_admin, audit_logger
import logging

logger = logging.getLogger(__name__)

users_api = Blueprint('users_api', __name__, url_prefix='/api/v1/users')


@users_api.route('/', methods=['GET'])
@require_api_key
@require_admin
def list_users():
    """Получить список пользователей (только для администраторов)"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 100)
        
        # Фильтры
        is_active = request.args.get('is_active', type=lambda v: v.lower() == 'true')
        is_admin = request.args.get('is_admin', type=lambda v: v.lower() == 'true')
        search = request.args.get('search', '').strip()
        
        # Запрос
        query = User.query
        
        if is_active is not None:
            query = query.filter_by(is_active=is_active)
        
        if is_admin is not None:
            query = query.filter_by(is_admin=is_admin)
        
        if search:
            query = query.filter(
                db.or_(
                    User.username.contains(search),
                    User.email.contains(search)
                )
            )
        
        # Пагинация
        pagination = query.order_by(User.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        # Логирование
        audit_logger.log_event(
            user_id=g.current_user.id,
            action='list',
            resource='users',
            details={'page': page, 'per_page': per_page}
        )
        
        return jsonify({
            'users': [user.to_dict() for user in pagination.items],
            'total': pagination.total,
            'page': page,
            'per_page': per_page,
            'pages': pagination.pages
        }), 200
        
    except Exception as e:
        logger.error(f"Error listing users: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@users_api.route('/<int:user_id>', methods=['GET'])
@require_api_key
def get_user(user_id):
    """Получить информацию о пользователе"""
    try:
        # Проверка прав доступа
        if g.current_user.id != user_id and not g.current_user.is_admin:
            return jsonify({
                'error': 'Access denied',
                'message': 'You can only view your own profile'
            }), 403
        
        user = User.query.get_or_404(user_id)
        
        # Логирование
        audit_logger.log_event(
            user_id=g.current_user.id,
            action='view',
            resource='user',
            resource_id=user_id
        )
        
        return jsonify(user.to_dict()), 200
        
    except Exception as e:
        logger.error(f"Error getting user {user_id}: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@users_api.route('/<int:user_id>', methods=['PUT'])
@require_api_key
def update_user(user_id):
    """Обновить информацию о пользователе"""
    try:
        # Проверка прав доступа
        if g.current_user.id != user_id and not g.current_user.is_admin:
            return jsonify({
                'error': 'Access denied',
                'message': 'You can only update your own profile'
            }), 403
        
        user = User.query.get_or_404(user_id)
        data = request.get_json()
        
        # Обновление разрешенных полей
        if 'email' in data:
            # Проверка уникальности email
            existing = User.query.filter_by(email=data['email']).first()
            if existing and existing.id != user_id:
                return jsonify({
                    'error': 'Email already exists',
                    'message': 'This email is already registered'
                }), 400
            user.email = data['email']
        
        # Только администраторы могут изменять эти поля
        if g.current_user.is_admin:
            if 'is_active' in data:
                user.is_active = data['is_active']
            if 'is_admin' in data:
                user.is_admin = data['is_admin']
        
        db.session.commit()
        
        # Логирование
        audit_logger.log_event(
            user_id=g.current_user.id,
            action='update',
            resource='user',
            resource_id=user_id,
            details=data
        )
        
        return jsonify({
            'message': 'User updated successfully',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        logger.error(f"Error updating user {user_id}: {e}")
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500


@users_api.route('/<int:user_id>/password', methods=['PUT'])
@require_api_key
def change_password(user_id):
    """Изменить пароль пользователя"""
    try:
        # Проверка прав доступа
        if g.current_user.id != user_id:
            return jsonify({
                'error': 'Access denied',
                'message': 'You can only change your own password'
            }), 403
        
        user = User.query.get_or_404(user_id)
        data = request.get_json()
        
        # Проверка текущего пароля
        if not data.get('current_password'):
            return jsonify({
                'error': 'Current password required',
                'message': 'Please provide your current password'
            }), 400
        
        if not user.check_password(data['current_password']):
            return jsonify({
                'error': 'Invalid password',
                'message': 'Current password is incorrect'
            }), 401
        
        # Проверка нового пароля
        if not data.get('new_password'):
            return jsonify({
                'error': 'New password required',
                'message': 'Please provide a new password'
            }), 400
        
        # Валидация нового пароля
        is_valid, error_msg = user.validate_password_strength(data['new_password'])
        if not is_valid:
            return jsonify({
                'error': 'Weak password',
                'message': error_msg
            }), 400
        
        # Установка нового пароля
        user.set_password(data['new_password'])
        db.session.commit()
        
        # Логирование
        audit_logger.log_event(
            user_id=user_id,
            action='change_password',
            resource='user',
            resource_id=user_id
        )
        
        logger.info(f"Password changed for user {user_id}")
        
        return jsonify({
            'message': 'Password changed successfully'
        }), 200
        
    except ValueError as e:
        return jsonify({
            'error': 'Validation error',
            'message': str(e)
        }), 400
    except Exception as e:
        logger.error(f"Error changing password for user {user_id}: {e}")
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500


@users_api.route('/<int:user_id>/api-key', methods=['POST'])
@require_api_key
def regenerate_api_key(user_id):
    """Перегенерировать API ключ пользователя"""
    try:
        # Проверка прав доступа
        if g.current_user.id != user_id and not g.current_user.is_admin:
            return jsonify({
                'error': 'Access denied',
                'message': 'You can only regenerate your own API key'
            }), 403
        
        user = User.query.get_or_404(user_id)
        old_key = user.api_key
        
        # Генерация нового ключа
        user.generate_api_key()
        db.session.commit()
        
        # Логирование
        audit_logger.log_event(
            user_id=g.current_user.id,
            action='regenerate_api_key',
            resource='user',
            resource_id=user_id
        )
        
        logger.info(f"API key regenerated for user {user_id}")
        
        return jsonify({
            'message': 'API key regenerated successfully',
            'api_key': user.api_key
        }), 200
        
    except Exception as e:
        logger.error(f"Error regenerating API key for user {user_id}: {e}")
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500


@users_api.route('/<int:user_id>', methods=['DELETE'])
@require_api_key
@require_admin
def delete_user(user_id):
    """Удалить пользователя (только для администраторов)"""
    try:
        user = User.query.get_or_404(user_id)
        
        # Нельзя удалить самого себя
        if user.id == g.current_user.id:
            return jsonify({
                'error': 'Cannot delete yourself',
                'message': 'You cannot delete your own account'
            }), 400
        
        username = user.username
        db.session.delete(user)
        db.session.commit()
        
        # Логирование
        audit_logger.log_event(
            user_id=g.current_user.id,
            action='delete',
            resource='user',
            resource_id=user_id,
            details={'username': username}
        )
        
        logger.info(f"User {user_id} ({username}) deleted by admin {g.current_user.id}")
        
        return jsonify({
            'message': 'User deleted successfully'
        }), 200
        
    except Exception as e:
        logger.error(f"Error deleting user {user_id}: {e}")
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500


@users_api.route('/stats', methods=['GET'])
@require_api_key
@require_admin
def get_stats():
    """Получить статистику пользователей (только для администраторов)"""
    try:
        from datetime import datetime, timedelta
        
        total_users = User.query.count()
        active_users = User.query.filter_by(is_active=True).count()
        admin_users = User.query.filter_by(is_admin=True).count()
        
        # Пользователи за последние 30 дней
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        recent_users = User.query.filter(
            User.created_at >= thirty_days_ago
        ).count()
        
        # Активные пользователи за последние 7 дней
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        active_last_week = User.query.filter(
            User.last_login >= seven_days_ago
        ).count()
        
        # Заблокированные пользователи
        locked_users = User.query.filter(
            User.locked_until > datetime.utcnow()
        ).count()
        
        stats = {
            'total_users': total_users,
            'active_users': active_users,
            'inactive_users': total_users - active_users,
            'admin_users': admin_users,
            'recent_users_30d': recent_users,
            'active_last_week': active_last_week,
            'locked_users': locked_users
        }
        
        # Логирование
        audit_logger.log_event(
            user_id=g.current_user.id,
            action='view_stats',
            resource='users'
        )
        
        return jsonify(stats), 200
        
    except Exception as e:
        logger.error(f"Error getting user stats: {e}")
        return jsonify({'error': 'Internal server error'}), 500
