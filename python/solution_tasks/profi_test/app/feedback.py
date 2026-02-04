from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from app import db
from app.models import User, TestResult, Feedback, Notification, ABTest, ABTestResult
from datetime import datetime
import json

feedback_bp = Blueprint('feedback', __name__)

# Модель уже определена в models.py

@feedback_bp.route('/feedback')
@login_required
def feedback_page():
    # Страница для пользователей, чтобы отправлять отзывы
    return render_template('feedback/index.html')


@feedback_bp.route('/api/feedback', methods=['POST'])
@login_required
def submit_feedback():
    # Отправка пользовательского отзыва
    data = request.get_json()
    
    feedback_type = data.get('type', 'general_feedback')
    title = data.get('title', '')
    content = data.get('content', '')
    rating = data.get('rating')
    
    # Проверка обязательных полей
    if not title or not content:
        return jsonify({'error': 'Title and content are required'}), 400
    
    # Проверка рейтинга, если он предоставлен
    if rating is not None and (rating < 1 or rating > 5):
        return jsonify({'error': 'Rating must be between 1 and 5'}), 400
    
    # Создание отзыва
    feedback = Feedback(
        user_id=current_user.id,
        feedback_type=feedback_type,
        title=title,
        content=content,
        rating=rating
    )
    
    db.session.add(feedback)
    db.session.commit()
    
    # Отправка уведомления администратору о новом отзыве
    from app.models import User
    admin_users = User.query.filter_by(is_admin=True).all()
    for admin in admin_users:
        notification = Notification(
            user_id=admin.id,
            title=f"Новый отзыв от {current_user.username}",
            message=f"Получен новый {feedback_type}: {title[:50]}...",
            type='info'
        )
        db.session.add(notification)
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Ваш отзыв успешно отправлен',
        'feedback_id': feedback.id
    })


@feedback_bp.route('/api/feedback')
@login_required
def get_user_feedback():
    # Получение отзывов, отправленных текущим пользователем
    page = request.args.get('page', 1, type=int)
    feedbacks = Feedback.query.filter_by(user_id=current_user.id).order_by(
        Feedback.created_at.desc()
    ).paginate(page=page, per_page=10, error_out=False)
    
    feedback_list = []
    for feedback in feedbacks.items:
        feedback_list.append({
            'id': feedback.id,
            'type': feedback.feedback_type,
            'title': feedback.title,
            'content': feedback.content,
            'rating': feedback.rating,
            'is_resolved': feedback.is_resolved,
            'created_at': feedback.created_at.isoformat(),
            'resolved_at': feedback.resolved_at.isoformat() if feedback.resolved_at else None,
            'resolution_notes': feedback.resolution_notes
        })
    
    return jsonify({
        'feedbacks': feedback_list,
        'total': feedbacks.total,
        'pages': feedbacks.pages,
        'current_page': page
    })


@feedback_bp.route('/api/feedback/<int:feedback_id>', methods=['PUT'])
@login_required
def update_feedback(feedback_id):
    # Обновление отзыва (отметка как решенного, добавление заметок) - только для администраторов
    if not current_user.is_admin:
        return jsonify({'error': 'Admin access required'}), 403
    
    feedback = Feedback.query.get_or_404(feedback_id)
    
    data = request.get_json()
    is_resolved = data.get('is_resolved')
    resolution_notes = data.get('resolution_notes', '')
    
    if is_resolved is not None:
        feedback.is_resolved = is_resolved
        if is_resolved:
            feedback.resolved_at = datetime.now(datetime.UTC)
    
    if resolution_notes:
        feedback.resolution_notes = resolution_notes
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Feedback updated successfully'
    })


@feedback_bp.route('/ab-tests/current-algorithm')
@login_required
def get_recommendation_algorithm():
    # Определение, какой алгоритм использовать для рекомендаций на основе A/B теста
    # Проверка, есть ли активный A/B тест для алгоритмов рекомендаций
    active_test = ABTest.query.filter_by(name='ml_recommendation_algorithm', is_active=True).first()
    
    if not active_test:
        # Возврат стандартного алгоритма, если нет активного теста
        return 'current_ml_algorithm'
    
    # Определение, какой вариант должен получить этот пользователь
    # Использование ID пользователя для постоянного назначения одного и того же варианта
    user_assignment_seed = current_user.id % 100
    traffic_percentage = int(active_test.traffic_split * 100)
    
    assigned_variant = 'B' if user_assignment_seed < traffic_percentage else 'A'
    
    # Запись этого назначения
    existing_result = ABTestResult.query.filter_by(
        ab_test_id=active_test.id,
        user_id=current_user.id
    ).first()
    
    if not existing_result:
        result = ABTestResult(
            ab_test_id=active_test.id,
            user_id=current_user.id,
            assigned_variant=assigned_variant
        )
        db.session.add(result)
        db.session.commit()
    
    # Возврат алгоритма на основе назначенного варианта
    if assigned_variant == 'A':
        return active_test.variant_a
    else:
        return active_test.variant_b


@feedback_bp.route('/api/ab-tests')
@login_required
def get_ab_tests():
    # Получение информации об активных A/B тестах
    if not current_user.is_admin:
        return jsonify({'error': 'Admin access required'}), 403
    
    tests = ABTest.query.all()
    test_list = []
    
    for test in tests:
        # Расчет метрик для каждого варианта
        results = ABTestResult.query.filter_by(ab_test_id=test.id).all()
        
        variant_a_results = [r for r in results if r.assigned_variant == 'A']
        variant_b_results = [r for r in results if r.assigned_variant == 'B']
        
        variant_a_metrics = {
            'count': len(variant_a_results),
            'avg_metric': sum(r.metric_value for r in variant_a_results) / len(variant_a_results) if variant_a_results else 0
        }
        
        variant_b_metrics = {
            'count': len(variant_b_results),
            'avg_metric': sum(r.metric_value for r in variant_b_results) / len(variant_b_results) if variant_b_results else 0
        }
        
        test_list.append({
            'id': test.id,
            'name': test.name,
            'description': test.description,
            'variant_a': test.variant_a,
            'variant_b': test.variant_b,
            'traffic_split': test.traffic_split,
            'is_active': test.is_active,
            'created_at': test.created_at.isoformat(),
            'started_at': test.started_at.isoformat() if test.started_at else None,
            'ended_at': test.ended_at.isoformat() if test.ended_at else None,
            'results': {
                'variant_a': variant_a_metrics,
                'variant_b': variant_b_metrics
            }
        })
    
    return jsonify({'tests': test_list})


@feedback_bp.route('/api/ab-tests', methods=['POST'])
@login_required
def create_ab_test():
    # Создание нового A/B теста - только для администраторов
    if not current_user.is_admin:
        return jsonify({'error': 'Admin access required'}), 403
    
    data = request.get_json()
    
    name = data.get('name')
    description = data.get('description', '')
    variant_a = data.get('variant_a')
    variant_b = data.get('variant_b')
    traffic_split = data.get('traffic_split', 0.5)
    
    # Проверка обязательных полей
    if not name or not variant_a or not variant_b:
        return jsonify({'error': 'Name, variant_a, and variant_b are required'}), 400
    
    # Проверка разделения трафика
    if traffic_split < 0 or traffic_split > 1:
        return jsonify({'error': 'Traffic split must be between 0 and 1'}), 400
    
    # Создание A/B теста
    ab_test = ABTest(
        name=name,
        description=description,
        variant_a=variant_a,
        variant_b=variant_b,
        traffic_split=traffic_split
    )
    
    db.session.add(ab_test)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'A/B test created successfully',
        'test_id': ab_test.id
    })


@feedback_bp.route('/api/ab-tests/<int:test_id>/activate', methods=['PUT'])
@login_required
def toggle_ab_test(test_id):
    # Активация/деактивация A/B теста - только для администраторов
    if not current_user.is_admin:
        return jsonify({'error': 'Admin access required'}), 403
    
    test = ABTest.query.get_or_404(test_id)
    
    test.is_active = not test.is_active
    
    if test.is_active:
        test.started_at = datetime.utcnow()
    else:
        test.ended_at = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'is_active': test.is_active,
        'message': f'A/B test {"activated" if test.is_active else "deactivated"} successfully'
    })


# Добавление моделей в основной модуль моделей также
def register_models_in_app():
    # Эта функция предназначена для документации - модели уже определены выше
    pass