# -*- coding: utf-8 -*-
"""
API конечные точки управления пользователями для ПрофиТест
Предоставляет доступ к функциям управления пользователями и правами доступа
"""
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.user_management import user_manager, UserRole, Permission
import json
from datetime import datetime

user_api = Blueprint('user_api', __name__)


@user_api.route('/users', methods=['GET'])
@login_required
def get_users():
    """
    Получает список пользователей с фильтрацией и пагинацией.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        # Параметры фильтрации
        role_filter = request.args.get('role')
        active_filter = request.args.get('active')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        
        # Получаем всех пользователей
        all_users = list(user_manager.users.values())
        
        # Применяем фильтры
        filtered_users = all_users
        
        if role_filter:
            try:
                role = UserRole(role_filter)
                filtered_users = [u for u in filtered_users if u.role == role]
            except ValueError:
                return jsonify({
                    'success': False,
                    'message': 'Некорректная роль'
                }), 400
        
        if active_filter is not None:
            is_active = active_filter.lower() == 'true'
            filtered_users = [u for u in filtered_users if u.is_active == is_active]
        
        # Пагинация
        total_users = len(filtered_users)
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        paginated_users = filtered_users[start_idx:end_idx]
        
        # Подготавливаем данные для ответа
        users_data = []
        for user in paginated_users:
            user_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role.value,
                'created_at': user.created_at.isoformat(),
                'last_login': user.last_login.isoformat() if user.last_login else None,
                'is_active': user.is_active,
                'is_verified': user.is_verified,
                'profile_completion': user.profile_completion,
                'permissions_count': len(user.permissions)
            }
            users_data.append(user_data)
        
        return jsonify({
            'success': True,
            'users': users_data,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total_users,
                'pages': (total_users + per_page - 1) // per_page
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@user_api.route('/users/<int:user_id>', methods=['GET'])
@login_required
def get_user(user_id):
    """
    Получает информацию о конкретном пользователе.
    """
    try:
        # Проверяем права доступа
        if user_id != current_user.id and not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Недостаточно прав для просмотра чужого профиля'
            }), 403
        
        user = user_manager.get_user(user_id)
        if not user:
            return jsonify({
                'success': False,
                'message': 'Пользователь не найден'
            }), 404
        
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role.value,
            'created_at': user.created_at.isoformat(),
            'last_login': user.last_login.isoformat() if user.last_login else None,
            'is_active': user.is_active,
            'is_verified': user.is_verified,
            'profile_completion': user.profile_completion,
            'permissions': [p.value for p in user.permissions],
            'metadata': user.metadata,
            'login_attempts': user.login_attempts,
            'two_factor_enabled': user.two_factor_enabled
        }
        
        return jsonify({
            'success': True,
            'user': user_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@user_api.route('/users', methods=['POST'])
@login_required
def create_user():
    """
    Создает нового пользователя.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        data = request.get_json()
        
        # Валидация обязательных полей
        required_fields = ['username', 'email', 'role']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'message': f'Поле {field} обязательно'
                }), 400
        
        # Создаем нового пользователя
        from app.user_management import User
        new_user = User(
            id=max(user_manager.users.keys()) + 1 if user_manager.users else 1,
            username=data['username'],
            email=data['email'],
            role=UserRole(data['role']),
            created_at=datetime.now(),
            is_active=data.get('is_active', True),
            is_verified=data.get('is_verified', False),
            profile_completion=data.get('profile_completion', 0.0)
        )
        
        if user_manager.add_user(new_user):
            return jsonify({
                'success': True,
                'message': 'Пользователь успешно создан',
                'user_id': new_user.id
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Не удалось создать пользователя'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@user_api.route('/users/<int:user_id>', methods=['PUT'])
@login_required
def update_user(user_id):
    """
    Обновляет информацию о пользователе.
    """
    try:
        # Проверяем права доступа
        if user_id != current_user.id and not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Недостаточно прав для редактирования чужого профиля'
            }), 403
        
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'message': 'Данные для обновления обязательны'
            }), 400
        
        # Обновляем пользователя
        update_fields = {}
        allowed_fields = ['username', 'email', 'is_active', 'is_verified', 'profile_completion', 'metadata']
        
        # Администратор может обновлять дополнительные поля
        if current_user.is_admin:
            allowed_fields.extend(['role'])
        
        for field in allowed_fields:
            if field in data:
                if field == 'role':
                    try:
                        update_fields[field] = UserRole(data[field])
                    except ValueError:
                        return jsonify({
                            'success': False,
                            'message': 'Некорректная роль'
                        }), 400
                else:
                    update_fields[field] = data[field]
        
        if user_manager.update_user(user_id, **update_fields):
            return jsonify({
                'success': True,
                'message': 'Пользователь успешно обновлен'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Не удалось обновить пользователя'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@user_api.route('/users/<int:user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
    """
    Удаляет пользователя.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        # Запрещаем удаление системного администратора
        user = user_manager.get_user(user_id)
        if user and user.username == 'admin':
            return jsonify({
                'success': False,
                'message': 'Невозможно удалить системного администратора'
            }), 403
        
        if user_manager.delete_user(user_id):
            return jsonify({
                'success': True,
                'message': 'Пользователь успешно удален'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Не удалось удалить пользователя'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@user_api.route('/users/<int:user_id>/suspend', methods=['POST'])
@login_required
def suspend_user(user_id):
    """
    Блокирует пользователя.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        data = request.get_json()
        duration_hours = data.get('duration_hours', 24)
        
        if user_manager.suspend_user(user_id, duration_hours):
            return jsonify({
                'success': True,
                'message': f'Пользователь заблокирован на {duration_hours} часов'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Не удалось заблокировать пользователя'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@user_api.route('/users/<int:user_id>/unsuspend', methods=['POST'])
@login_required
def unsuspend_user(user_id):
    """
    Снимает блокировку с пользователя.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        if user_manager.unsuspend_user(user_id):
            return jsonify({
                'success': True,
                'message': 'Блокировка с пользователя снята'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Не удалось снять блокировку'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@user_api.route('/users/<int:user_id>/permissions', methods=['GET'])
@login_required
def get_user_permissions(user_id):
    """
    Получает права доступа пользователя.
    """
    try:
        # Проверяем права доступа
        if user_id != current_user.id and not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Недостаточно прав для просмотра прав другого пользователя'
            }), 403
        
        permissions = user_manager.get_user_permissions(user_id)
        permissions_list = [p.value for p in permissions]
        
        return jsonify({
            'success': True,
            'permissions': permissions_list,
            'count': len(permissions_list)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@user_api.route('/users/<int:user_id>/permissions', methods=['POST'])
@login_required
def add_user_permission(user_id):
    """
    Добавляет право пользователю.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        data = request.get_json()
        permission_name = data.get('permission')
        
        if not permission_name:
            return jsonify({
                'success': False,
                'message': 'Необходимо указать право'
            }), 400
        
        try:
            permission = Permission(permission_name)
        except ValueError:
            return jsonify({
                'success': False,
                'message': 'Некорректное право доступа'
            }), 400
        
        if user_manager.add_permission(user_id, permission):
            return jsonify({
                'success': True,
                'message': 'Право успешно добавлено'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Не удалось добавить право'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@user_api.route('/users/<int:user_id>/permissions/<permission_name>', methods=['DELETE'])
@login_required
def remove_user_permission(user_id, permission_name):
    """
    Удаляет право у пользователя.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        try:
            permission = Permission(permission_name)
        except ValueError:
            return jsonify({
                'success': False,
                'message': 'Некорректное право доступа'
            }), 400
        
        if user_manager.remove_permission(user_id, permission):
            return jsonify({
                'success': True,
                'message': 'Право успешно удалено'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Не удалось удалить право'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@user_api.route('/users/<int:user_id>/check-permission/<permission_name>', methods=['GET'])
@login_required
def check_user_permission(user_id, permission_name):
    """
    Проверяет, имеет ли пользователь определенное право.
    """
    try:
        # Проверяем права доступа
        if user_id != current_user.id and not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Недостаточно прав для проверки прав другого пользователя'
            }), 403
        
        try:
            permission = Permission(permission_name)
        except ValueError:
            return jsonify({
                'success': False,
                'message': 'Некорректное право доступа'
            }), 400
        
        has_permission = user_manager.check_permission(user_id, permission)
        
        return jsonify({
            'success': True,
            'has_permission': has_permission,
            'permission': permission_name
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@user_api.route('/roles', methods=['GET'])
@login_required
def get_roles():
    """
    Получает список доступных ролей.
    """
    try:
        roles_data = []
        for role in UserRole:
            role_data = {
                'name': role.name,
                'value': role.value,
                'description': self._get_role_description(role)
            }
            roles_data.append(role_data)
        
        return jsonify({
            'success': True,
            'roles': roles_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500
    
    def _get_role_description(self, role):
        """Получает описание роли."""
        descriptions = {
            UserRole.GUEST: 'Гостевой пользователь с ограниченными правами',
            UserRole.USER: 'Обычный пользователь с базовыми правами',
            UserRole.PREMIUM_USER: 'Премиум пользователь с расширенными правами',
            UserRole.MODERATOR: 'Модератор с правами управления контентом',
            UserRole.ADMIN: 'Администратор с правами управления системой',
            UserRole.SUPER_ADMIN: 'Супер-администратор с полными правами'
        }
        return descriptions.get(role, 'Неизвестная роль')


@user_api.route('/permissions', methods=['GET'])
@login_required
def get_permissions():
    """
    Получает список доступных прав доступа.
    """
    try:
        permissions_data = []
        for permission in Permission:
            permission_data = {
                'name': permission.name,
                'value': permission.value,
                'description': self._get_permission_description(permission)
            }
            permissions_data.append(permission_data)
        
        return jsonify({
            'success': True,
            'permissions': permissions_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500
    
    def _get_permission_description(self, permission):
        """Получает описание права доступа."""
        descriptions = {
            Permission.VIEW_PROFILE: 'Просмотр своего профиля',
            Permission.EDIT_PROFILE: 'Редактирование своего профиля',
            Permission.VIEW_TESTS: 'Просмотр тестов',
            Permission.TAKE_TESTS: 'Прохождение тестов',
            Permission.ACCESS_PREMIUM_FEATURES: 'Доступ к премиум функциям',
            Permission.VIEW_DETAILED_ANALYTICS: 'Просмотр детальной аналитики',
            Permission.EXPORT_DATA: 'Экспорт данных',
            Permission.MODERATE_CONTENT: 'Модерация контента',
            Permission.MANAGE_COMMENTS: 'Управление комментариями',
            Permission.VIEW_USER_ACTIVITY: 'Просмотр активности пользователей',
            Permission.MANAGE_USERS: 'Управление пользователями',
            Permission.MANAGE_TESTS: 'Управление тестами',
            Permission.VIEW_SYSTEM_LOGS: 'Просмотр системных логов',
            Permission.CONFIGURE_SYSTEM: 'Настройка системы',
            Permission.FULL_ACCESS: 'Полный доступ ко всем функциям',
            Permission.MANAGE_ADMINISTRATORS: 'Управление администраторами',
            Permission.SYSTEM_MAINTENANCE: 'Обслуживание системы'
        }
        return descriptions.get(permission, 'Неизвестное право')


@user_api.route('/statistics', methods=['GET'])
@login_required
def get_user_statistics():
    """
    Получает статистику по пользователям.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        stats = user_manager.get_statistics()
        return jsonify({
            'success': True,
            'statistics': stats
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@user_api.route('/users/<int:user_id>/report', methods=['GET'])
@login_required
def get_user_report(user_id):
    """
    Генерирует отчет по пользователю.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        report = user_manager.generate_user_report(user_id)
        
        if 'error' in report:
            return jsonify({
                'success': False,
                'message': report['error']
            }), 404
        
        return jsonify({
            'success': True,
            'report': report
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@user_api.route('/bulk-update', methods=['POST'])
@login_required
def bulk_update_users():
    """
    Массовое обновление пользователей.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        data = request.get_json()
        user_updates = data.get('updates', [])
        
        if not user_updates:
            return jsonify({
                'success': False,
                'message': 'Необходимо указать обновления'
            }), 400
        
        results = user_manager.bulk_update_users(user_updates)
        
        return jsonify({
            'success': True,
            'results': results
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@user_api.route('/search', methods=['GET'])
@login_required
def search_users():
    """
    Поиск пользователей по различным критериям.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        query = request.args.get('q', '').lower()
        role_filter = request.args.get('role')
        
        # Поиск по имени пользователя и email
        matching_users = []
        for user in user_manager.users.values():
            if (query in user.username.lower() or 
                query in user.email.lower() or 
                query in user.role.value.lower()):
                
                if role_filter and user.role.value != role_filter:
                    continue
                    
                matching_users.append({
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'role': user.role.value,
                    'is_active': user.is_active
                })
        
        return jsonify({
            'success': True,
            'users': matching_users,
            'count': len(matching_users)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500