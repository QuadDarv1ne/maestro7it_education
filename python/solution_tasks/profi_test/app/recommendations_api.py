# -*- coding: utf-8 -*-
"""
API конечные точки расширенной системы рекомендаций для ПрофиТест
Предоставляет доступ к функциям персонализированных рекомендаций
"""
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.ml_recommendations import recommendation_engine, RecommendationType, RecommendationContext
import json
from datetime import datetime

recommendations_api = Blueprint('recommendations_api', __name__)


@recommendations_api.route('/recommendations/personalized', methods=['GET'])
@login_required
def get_personalized_recommendations():
    """
    Получает персонализированные рекомендации для пользователя.
    """
    try:
        limit = int(request.args.get('limit', 10))
        include_explanation = request.args.get('include_explanation', 'true').lower() == 'true'
        
        recommendations = recommendation_engine.get_personalized_recommendations(current_user.id, limit)
        
        # Подготавливаем данные для ответа
        recommendations_data = []
        for rec in recommendations:
            rec_data = {
                'id': rec.id,
                'target_id': rec.target_id,
                'target_type': rec.target_type,
                'score': round(rec.score, 3),
                'recommendation_type': rec.recommendation_type.value,
                'context': [ctx.value for ctx in rec.context],
                'created_at': rec.created_at.isoformat()
            }
            
            if include_explanation:
                rec_data['explanation'] = rec.explanation
                rec_data['metadata'] = rec.metadata
            
            recommendations_data.append(rec_data)
        
        return jsonify({
            'success': True,
            'recommendations': recommendations_data,
            'count': len(recommendations_data),
            'user_id': current_user.id
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@recommendations_api.route('/recommendations/content-based', methods=['GET'])
@login_required
def get_content_based_recommendations():
    """
    Получает рекомендации на основе контента.
    """
    try:
        limit = int(request.args.get('limit', 10))
        
        recommendations = recommendation_engine.get_content_based_recommendations(current_user.id, limit)
        
        recommendations_data = []
        for rec in recommendations:
            rec_data = {
                'id': rec.id,
                'target_id': rec.target_id,
                'target_type': rec.target_type,
                'score': round(rec.score, 3),
                'explanation': rec.explanation,
                'metadata': rec.metadata
            }
            recommendations_data.append(rec_data)
        
        return jsonify({
            'success': True,
            'recommendations': recommendations_data,
            'count': len(recommendations_data)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@recommendations_api.route('/recommendations/collaborative', methods=['GET'])
@login_required
def get_collaborative_recommendations():
    """
    Получает коллаборативные рекомендации.
    """
    try:
        limit = int(request.args.get('limit', 10))
        
        recommendations = recommendation_engine.get_collaborative_recommendations(current_user.id, limit)
        
        recommendations_data = []
        for rec in recommendations:
            rec_data = {
                'id': rec.id,
                'target_id': rec.target_id,
                'target_type': rec.target_type,
                'score': round(rec.score, 3),
                'explanation': rec.explanation,
                'metadata': rec.metadata
            }
            recommendations_data.append(rec_data)
        
        return jsonify({
            'success': True,
            'recommendations': recommendations_data,
            'count': len(recommendations_data)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@recommendations_api.route('/recommendations/hybrid', methods=['GET'])
@login_required
def get_hybrid_recommendations():
    """
    Получает гибридные рекомендации.
    """
    try:
        limit = int(request.args.get('limit', 10))
        
        recommendations = recommendation_engine.get_hybrid_recommendations(current_user.id, limit)
        
        recommendations_data = []
        for rec in recommendations:
            rec_data = {
                'id': rec.id,
                'target_id': rec.target_id,
                'target_type': rec.target_type,
                'score': round(rec.score, 3),
                'recommendation_type': rec.recommendation_type.value,
                'explanation': rec.explanation,
                'metadata': rec.metadata
            }
            recommendations_data.append(rec_data)
        
        return jsonify({
            'success': True,
            'recommendations': recommendations_data,
            'count': len(recommendations_data)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@recommendations_api.route('/recommendations/trending', methods=['GET'])
@login_required
def get_trending_recommendations():
    """
    Получает трендовые рекомендации.
    """
    try:
        limit = int(request.args.get('limit', 10))
        
        recommendations = recommendation_engine.get_trending_recommendations(limit)
        
        recommendations_data = []
        for rec in recommendations:
            rec_data = {
                'id': rec.id,
                'target_id': rec.target_id,
                'target_type': rec.target_type,
                'score': round(rec.score, 3),
                'explanation': rec.explanation,
                'metadata': rec.metadata
            }
            recommendations_data.append(rec_data)
        
        return jsonify({
            'success': True,
            'recommendations': recommendations_data,
            'count': len(recommendations_data)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@recommendations_api.route('/preferences', methods=['GET'])
@login_required
def get_user_preferences():
    """
    Получает предпочтения пользователя.
    """
    try:
        user_id = current_user.id
        preferences = recommendation_engine.user_preferences.get(user_id)
        
        if not preferences:
            return jsonify({
                'success': False,
                'message': 'Предпочтения пользователя не найдены'
            }), 404
        
        preferences_data = {
            'user_id': preferences.user_id,
            'interests': preferences.interests,
            'skills': preferences.skills,
            'career_goals': preferences.career_goals,
            'preferred_content_types': preferences.preferred_content_types,
            'preference_scores': preferences.preference_scores,
            'interaction_history_count': len(preferences.interaction_history),
            'last_updated': preferences.last_updated.isoformat()
        }
        
        return jsonify({
            'success': True,
            'preferences': preferences_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@recommendations_api.route('/preferences', methods=['PUT'])
@login_required
def update_user_preferences():
    """
    Обновляет предпочтения пользователя.
    """
    try:
        data = request.get_json()
        user_id = current_user.id
        
        # Обновляем различные типы предпочтений
        updated_fields = []
        
        preference_fields = ['interests', 'skills', 'career_goals', 'preferred_content_types']
        for field in preference_fields:
            if field in data:
                values = data[field] if isinstance(data[field], list) else [data[field]]
                weight = data.get(f'{field}_weight', 1.0)
                
                if recommendation_engine.update_user_preference(user_id, field, values, weight):
                    updated_fields.append(field)
        
        if updated_fields:
            return jsonify({
                'success': True,
                'message': f'Предпочтения обновлены: {", ".join(updated_fields)}',
                'updated_fields': updated_fields
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Не удалось обновить предпочтения'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@recommendations_api.route('/interactions', methods=['POST'])
@login_required
def record_user_interaction():
    """
    Записывает взаимодействие пользователя с контентом.
    """
    try:
        data = request.get_json()
        
        # Валидация обязательных полей
        required_fields = ['content_id', 'interaction_type']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'message': f'Поле {field} обязательно'
                }), 400
        
        success = recommendation_engine.record_user_interaction(
            user_id=current_user.id,
            content_id=data['content_id'],
            interaction_type=data['interaction_type'],
            rating=data.get('rating')
        )
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Взаимодействие успешно записано'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Не удалось записать взаимодействие'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@recommendations_api.route('/recommendations/types', methods=['GET'])
@login_required
def get_recommendation_types():
    """
    Получает список типов рекомендаций.
    """
    try:
        types_data = []
        for rec_type in RecommendationType:
            type_data = {
                'name': rec_type.name,
                'value': rec_type.value,
                'description': self._get_recommendation_type_description(rec_type)
            }
            types_data.append(type_data)
        
        return jsonify({
            'success': True,
            'types': types_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500
    
def _get_recommendation_type_description(rec_type):
    """Получает описание типа рекомендации."""
    descriptions = {
        RecommendationType.CONTENT_BASED: 'На основе контента',
        RecommendationType.COLLABORATIVE: 'Коллаборативные',
        RecommendationType.HYBRID: 'Гибридные',
        RecommendationType.CONTEXTUAL: 'Контекстуальные',
        RecommendationType.TRENDING: 'Трендовые',
        RecommendationType.PERSONALIZED: 'Персонализированные'
    }
    return descriptions.get(rec_type, 'Неизвестный тип')


@recommendations_api.route('/recommendations/contexts', methods=['GET'])
@login_required
def get_recommendation_contexts():
    """
    Получает список контекстов рекомендаций.
    """
    try:
        contexts_data = []
        for context in RecommendationContext:
            context_data = {
                'name': context.name,
                'value': context.value,
                'description': self._get_context_description(context)
            }
            contexts_data.append(context_data)
        
        return jsonify({
            'success': True,
            'contexts': contexts_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500
    
def _get_context_description(context):
    """Получает описание контекста."""
    descriptions = {
        RecommendationContext.USER_PROFILE: 'На основе профиля пользователя',
        RecommendationContext.BEHAVIOR: 'На основе поведения',
        RecommendationContext.TIME: 'Временной контекст',
        RecommendationContext.LOCATION: 'Географический контекст',
        RecommendationContext.DEVICE: 'Контекст устройства',
        RecommendationContext.SEASONAL: 'Сезонный контекст'
    }
    return descriptions.get(context, 'Неизвестный контекст')


@recommendations_api.route('/statistics', methods=['GET'])
@login_required
def get_recommendations_statistics():
    """
    Получает статистику по рекомендациям.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        stats = recommendation_engine.get_recommendation_statistics()
        return jsonify({
            'success': True,
            'statistics': stats
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@recommendations_api.route('/recommendations/<recommendation_id>', methods=['GET'])
@login_required
def get_recommendation_details(recommendation_id):
    """
    Получает детали конкретной рекомендации.
    """
    try:
        recommendation = recommendation_engine.recommendations.get(recommendation_id)
        if not recommendation:
            return jsonify({
                'success': False,
                'message': 'Рекомендация не найдена'
            }), 404
        
        # Получаем дополнительную информацию о контенте
        content_info = recommendation_engine.content_features.get(recommendation.target_id, {})
        
        recommendation_data = {
            'id': recommendation.id,
            'target_id': recommendation.target_id,
            'target_type': recommendation.target_type,
            'score': round(recommendation.score, 3),
            'recommendation_type': recommendation.recommendation_type.value,
            'context': [ctx.value for ctx in recommendation.context],
            'created_at': recommendation.created_at.isoformat(),
            'explanation': recommendation.explanation,
            'metadata': recommendation.metadata,
            'content_info': {
                'title': content_info.get('title', 'Неизвестный контент'),
                'description': content_info.get('description', ''),
                'category': content_info.get('category', 'unknown'),
                'tags': content_info.get('tags', []),
                'difficulty': content_info.get('difficulty', 'unknown')
            }
        }
        
        return jsonify({
            'success': True,
            'recommendation': recommendation_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@recommendations_api.route('/recommendations/config', methods=['GET'])
@login_required
def get_recommendation_config():
    """
    Получает конфигурацию системы рекомендаций.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        config = recommendation_engine.recommendation_config
        return jsonify({
            'success': True,
            'config': config
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@recommendations_api.route('/recommendations/config', methods=['PUT'])
@login_required
def update_recommendation_config():
    """
    Обновляет конфигурацию системы рекомендаций.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        data = request.get_json()
        
        # Обновляем только разрешенные параметры
        allowed_params = [
            'max_recommendations', 'min_similarity_threshold', 
            'diversity_factor', 'freshness_boost', 'popularity_weight'
        ]
        
        for param in allowed_params:
            if param in data:
                recommendation_engine.recommendation_config[param] = data[param]
        
        return jsonify({
            'success': True,
            'message': 'Конфигурация рекомендаций обновлена'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@recommendations_api.route('/recommendations/feedback', methods=['POST'])
@login_required
def submit_recommendation_feedback():
    """
    Отправляет обратную связь по рекомендации.
    """
    try:
        data = request.get_json()
        
        # Валидация обязательных полей
        required_fields = ['recommendation_id', 'feedback_type']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'message': f'Поле {field} обязательно'
                }), 400
        
        recommendation_id = data['recommendation_id']
        feedback_type = data['feedback_type']  # 'helpful', 'not_helpful', 'irrelevant'
        comment = data.get('comment', '')
        
        # В реальной системе здесь будет сохранение обратной связи
        # Пока просто логируем
        
        return jsonify({
            'success': True,
            'message': 'Обратная связь по рекомендации отправлена'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@recommendations_api.route('/recommendations/batch', methods=['POST'])
@login_required
def get_batch_recommendations():
    """
    Получает пакет рекомендаций разными методами.
    """
    try:
        data = request.get_json()
        methods = data.get('methods', ['personalized'])
        limit = data.get('limit', 5)
        
        batch_results = {}
        
        for method in methods:
            try:
                if method == 'personalized':
                    recommendations = recommendation_engine.get_personalized_recommendations(current_user.id, limit)
                elif method == 'content_based':
                    recommendations = recommendation_engine.get_content_based_recommendations(current_user.id, limit)
                elif method == 'collaborative':
                    recommendations = recommendation_engine.get_collaborative_recommendations(current_user.id, limit)
                elif method == 'hybrid':
                    recommendations = recommendation_engine.get_hybrid_recommendations(current_user.id, limit)
                elif method == 'trending':
                    recommendations = recommendation_engine.get_trending_recommendations(limit)
                else:
                    continue
                
                batch_results[method] = []
                for rec in recommendations:
                    rec_data = {
                        'id': rec.id,
                        'target_id': rec.target_id,
                        'target_type': rec.target_type,
                        'score': round(rec.score, 3),
                        'explanation': rec.explanation
                    }
                    batch_results[method].append(rec_data)
                    
            except Exception as e:
                batch_results[method] = {'error': str(e)}
        
        return jsonify({
            'success': True,
            'results': batch_results
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@recommendations_api.route('/test-recommendations', methods=['POST'])
@login_required
def test_recommendation_system():
    """
    Тестовая функция для проверки системы рекомендаций.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        # Обновляем предпочтения тестового пользователя
        recommendation_engine.update_user_preference(
            user_id=current_user.id,
            preference_type='interests',
            values=['психология', 'карьера', 'технологии'],
            weight=1.0
        )
        
        # Получаем тестовые рекомендации
        test_recommendations = recommendation_engine.get_personalized_recommendations(current_user.id, 5)
        
        # Записываем тестовое взаимодействие
        if test_recommendations:
            test_content_id = test_recommendations[0].target_id
            recommendation_engine.record_user_interaction(
                user_id=current_user.id,
                content_id=test_content_id,
                interaction_type='view'
            )
        
        return jsonify({
            'success': True,
            'message': 'Тестовая система рекомендаций выполнена успешно',
            'test_recommendations_count': len(test_recommendations),
            'user_preferences_updated': True
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@recommendations_api.route('/recommendations/popular', methods=['GET'])
@login_required
def get_popular_recommendations():
    """
    Получает популярные рекомендации.
    """
    try:
        limit = int(request.args.get('limit', 10))
        
        # Получаем популярные рекомендации (на основе взаимодействий и рейтингов)
        # Временно используем трендовые рекомендации до реализации метода
        popular_recommendations = recommendation_engine.get_trending_recommendations(limit)
        
        recommendations_data = []
        for rec in popular_recommendations:
            rec_data = {
                'id': rec.id,
                'target_id': rec.target_id,
                'target_type': rec.target_type,
                'score': round(rec.score, 3),
                'explanation': rec.explanation,
                'metadata': rec.metadata
            }
            recommendations_data.append(rec_data)
        
        return jsonify({
            'success': True,
            'recommendations': recommendations_data,
            'count': len(recommendations_data)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500