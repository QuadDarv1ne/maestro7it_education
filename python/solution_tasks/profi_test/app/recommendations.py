from flask import Blueprint, jsonify, render_template
from flask_login import login_required, current_user
from app import db
from app.models import TestResult
from app.ai_recommender import AIRecommendationEngine

recommendations_bp = Blueprint('recommendations', __name__)

@recommendations_bp.route('/recommendations/<int:result_id>')
@login_required
def get_recommendations(result_id):
    """Получить персонализированные рекомендации для результата теста"""
    result = TestResult.query.get_or_404(result_id)
    
    # Проверка доступа к результату
    if result.user_id != current_user.id and not current_user.is_admin:
        return jsonify({'error': 'Доступ запрещен'}), 403
    
    # Создание экземпляра движка рекомендаций
    recommender = AIRecommendationEngine(db.session)
    
    # Получение рекомендаций
    recommendations = recommender.get_personalized_recommendations(result)
    
    return jsonify(recommendations)

@recommendations_bp.route('/recommendations/<int:result_id>/detailed')
@login_required
def detailed_recommendations(result_id):
    """Просмотр детализированных рекомендаций"""
    result = TestResult.query.get_or_404(result_id)
    
    # Проверка доступа к результату
    if result.user_id != current_user.id and not current_user.is_admin:
        return jsonify({'error': 'Доступ запрещен'}), 403
    
    # Создание экземпляра движка рекомендаций
    recommender = AIRecommendationEngine(db.session)
    
    # Получение рекомендаций
    recommendations = recommender.get_personalized_recommendations(result)
    
    return render_template('recommendations/detailed.html', 
                         result=result, 
                         recommendations=recommendations)

@recommendations_bp.route('/similar_users/<int:result_id>')
@login_required
def similar_users(result_id):
    """Найти пользователей с похожими результатами"""
    result = TestResult.query.get_or_404(result_id)
    
    # Проверка доступа к результату
    if result.user_id != current_user.id and not current_user.is_admin:
        return jsonify({'error': 'Доступ запрещен'}), 403
    
    # Создание экземпляра движка рекомендаций
    recommender = AIRecommendationEngine(db.session)
    
    # Поиск похожих пользователей
    similar_users_list = recommender.find_similar_users(result)
    
    similar_users_data = []
    for user, similarity in similar_users_list:
        similar_users_data.append({
            'username': user.username,
            'similarity': round(similarity * 100, 2),
            'is_admin': user.is_admin
        })
    
    return jsonify(similar_users_data)