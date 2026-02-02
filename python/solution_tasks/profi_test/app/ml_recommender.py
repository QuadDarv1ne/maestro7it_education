from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import User, TestResult
from app.ml_recommendations import get_user_recommendations

ml_recommender = Blueprint('ml_recommender', __name__)

@ml_recommender.route('/ml-recommendations')
@login_required
def get_ml_recommendations():
    """
    Получить ML-рекомендации для текущего пользователя
    """
    recommendations = get_user_recommendations(current_user.id)
    
    return jsonify({
        'success': True,
        'recommendations': recommendations,
        'count': len(recommendations)
    })

@ml_recommender.route('/ml-recommendations/train-model')
@login_required
def train_model():
    """
    Обучить ML-модель (доступно только администраторам)
    """
    if not current_user.is_admin:
        return jsonify({'success': False, 'message': 'Доступно только администраторам'}), 403
    
    from app.ml_recommendations import train_ml_model
    try:
        train_ml_model()
        return jsonify({'success': True, 'message': 'ML-модель успешно обучена'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Ошибка при обучении модели: {str(e)}'}), 500

@ml_recommender.route('/ml-recommendations/user/<int:user_id>')
@login_required
def get_user_ml_recommendations(user_id):
    """
    Получить ML-рекомендации для конкретного пользователя (доступно только администраторам)
    """
    if not current_user.is_admin:
        return jsonify({'success': False, 'message': 'Доступно только администраторам'}), 403
    
    user = User.query.get_or_404(user_id)
    recommendations = get_user_recommendations(user_id)
    
    return jsonify({
        'success': True,
        'user_id': user_id,
        'username': user.username,
        'recommendations': recommendations,
        'count': len(recommendations)
    })