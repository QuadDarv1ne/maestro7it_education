# -*- coding: utf-8 -*-
"""
API конечные точки расширенной системы рейтингов и отзывов для ПрофиТест
Предоставляет доступ к функциям управления рейтингами и отзывами
"""
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.advanced_ratings import rating_manager, RatingType, RatingDimension, ReviewStatus
import json
from datetime import datetime

ratings_api = Blueprint('ratings_api', __name__)


@ratings_api.route('/ratings', methods=['POST'])
@login_required
def add_rating():
    """
    Добавляет новый рейтинг.
    """
    try:
        data = request.get_json()
        
        # Валидация обязательных полей
        required_fields = ['target_id', 'target_type', 'rating_type', 'value']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'message': f'Поле {field} обязательно'
                }), 400
        
        # Создаем новый рейтинг
        rating_id = rating_manager.add_rating(
            target_id=data['target_id'],
            target_type=data['target_type'],
            user_id=current_user.id,
            rating_type=RatingType(data['rating_type']),
            value=float(data['value']),
            dimension=RatingDimension(data.get('dimension', 'overall')),
            comment=data.get('comment'),
            is_anonymous=data.get('is_anonymous', False),
            metadata=data.get('metadata', {})
        )
        
        if rating_id:
            return jsonify({
                'success': True,
                'message': 'Рейтинг успешно добавлен',
                'rating_id': rating_id
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Не удалось добавить рейтинг'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@ratings_api.route('/ratings/target/<target_id>', methods=['GET'])
@login_required
def get_target_ratings(target_id):
    """
    Получает рейтинги для конкретного объекта.
    """
    try:
        # Параметры
        method = request.args.get('method', 'average')  # average, weighted, bayesian
        include_individual = request.args.get('include_individual', 'false').lower() == 'true'
        
        # Рассчитываем общий рейтинг
        rating_info = rating_manager.calculate_target_rating(target_id, method)
        
        # Получаем индивидуальные рейтинги если запрошено
        individual_ratings = []
        if include_individual:
            ratings = rating_manager.get_ratings_for_target(target_id)
            for rating in ratings:
                rating_data = {
                    'id': rating.id,
                    'user_id': rating.user_id if not rating.is_anonymous else None,
                    'rating_type': rating.rating_type.value,
                    'value': rating.value,
                    'dimension': rating.dimension.value,
                    'comment': rating.comment,
                    'created_at': rating.created_at.isoformat(),
                    'is_anonymous': rating.is_anonymous
                }
                individual_ratings.append(rating_data)
        
        response = {
            'success': True,
            'target_id': target_id,
            'rating_info': rating_info
        }
        
        if include_individual:
            response['individual_ratings'] = individual_ratings
        
        return jsonify(response)
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@ratings_api.route('/ratings/user/<int:user_id>', methods=['GET'])
@login_required
def get_user_ratings(user_id):
    """
    Получает рейтинги пользователя.
    """
    try:
        # Проверяем права доступа
        if user_id != current_user.id and not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Недостаточно прав для просмотра чужих рейтингов'
            }), 403
        
        ratings = rating_manager.get_user_ratings(user_id)
        
        ratings_data = []
        for rating in ratings:
            rating_data = {
                'id': rating.id,
                'target_id': rating.target_id,
                'target_type': rating.target_type,
                'rating_type': rating.rating_type.value,
                'value': rating.value,
                'dimension': rating.dimension.value,
                'comment': rating.comment,
                'created_at': rating.created_at.isoformat(),
                'is_anonymous': rating.is_anonymous
            }
            ratings_data.append(rating_data)
        
        # Статистика пользователя
        user_stats = rating_manager.get_user_contribution_stats(user_id)
        
        return jsonify({
            'success': True,
            'ratings': ratings_data,
            'user_stats': user_stats,
            'count': len(ratings_data)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@ratings_api.route('/reviews', methods=['POST'])
@login_required
def add_review():
    """
    Добавляет новый отзыв.
    """
    try:
        data = request.get_json()
        
        # Валидация обязательных полей
        required_fields = ['target_id', 'target_type', 'title', 'content']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'message': f'Поле {field} обязательно'
                }), 400
        
        # Создаем новый отзыв
        review_id = rating_manager.add_review(
            target_id=data['target_id'],
            target_type=data['target_type'],
            user_id=current_user.id,
            title=data['title'],
            content=data['content'],
            is_verified=data.get('is_verified', False),
            tags=data.get('tags', []),
            metadata=data.get('metadata', {})
        )
        
        if review_id:
            return jsonify({
                'success': True,
                'message': 'Отзыв успешно добавлен',
                'review_id': review_id
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Не удалось добавить отзыв'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@ratings_api.route('/reviews/target/<target_id>', methods=['GET'])
@login_required
def get_target_reviews(target_id):
    """
    Получает отзывы для конкретного объекта.
    """
    try:
        status = request.args.get('status')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        
        # Фильтр по статусу
        status_filter = ReviewStatus(status) if status else None
        
        # Получаем отзывы
        all_reviews = rating_manager.get_reviews_for_target(target_id, status_filter)
        
        # Пагинация
        total_reviews = len(all_reviews)
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        paginated_reviews = all_reviews[start_idx:end_idx]
        
        reviews_data = []
        for review in paginated_reviews:
            review_data = {
                'id': review.id,
                'user_id': review.user_id,
                'title': review.title,
                'content': review.content,
                'status': review.status.value,
                'created_at': review.created_at.isoformat(),
                'published_at': review.published_at.isoformat() if review.published_at else None,
                'helpful_count': review.helpful_count,
                'not_helpful_count': review.not_helpful_count,
                'reports': review.reports,
                'is_verified': review.is_verified,
                'tags': review.tags
            }
            reviews_data.append(review_data)
        
        return jsonify({
            'success': True,
            'reviews': reviews_data,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total_reviews,
                'pages': (total_reviews + per_page - 1) // per_page
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@ratings_api.route('/reviews/<review_id>/helpful', methods=['POST'])
@login_required
def mark_review_helpful(review_id):
    """
    Помечает отзыв как полезный.
    """
    try:
        data = request.get_json()
        helpful = data.get('helpful', True)
        
        if rating_manager.mark_review_helpful(review_id, current_user.id, helpful):
            return jsonify({
                'success': True,
                'message': f'Отзыв помечен как {"полезный" if helpful else "неполезный"}'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Не удалось пометить отзыв'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@ratings_api.route('/reviews/<review_id>/report', methods=['POST'])
@login_required
def report_review(review_id):
    """
    Отмечает отзыв как неприемлемый.
    """
    try:
        data = request.get_json()
        reason = data.get('reason', 'Не указана причина')
        
        if rating_manager.report_review(review_id, current_user.id, reason):
            return jsonify({
                'success': True,
                'message': 'Жалоба отправлена'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Не удалось отправить жалобу'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@ratings_api.route('/top-rated/<target_type>', methods=['GET'])
@login_required
def get_top_rated_targets(target_type):
    """
    Получает объекты с наивысшими рейтингами.
    """
    try:
        limit = int(request.args.get('limit', 10))
        
        top_targets = rating_manager.get_top_rated_targets(target_type, limit)
        
        return jsonify({
            'success': True,
            'target_type': target_type,
            'top_targets': top_targets
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@ratings_api.route('/rating-types', methods=['GET'])
@login_required
def get_rating_types():
    """
    Получает список типов рейтингов.
    """
    try:
        types_data = []
        for rating_type in RatingType:
            type_data = {
                'name': rating_type.name,
                'value': rating_type.value,
                'description': self._get_rating_type_description(rating_type),
                'value_range': self._get_rating_type_range(rating_type)
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
    
    def _get_rating_type_description(self, rating_type):
        """Получает описание типа рейтинга."""
        descriptions = {
            RatingType.STAR_RATING: 'Звездный рейтинг (1-5)',
            RatingType.LIKE_DISLIKE: 'Нравится/Не нравится',
            RatingType.THUMBS: 'Большой палец вверх/вниз',
            RatingType.PERCENTAGE: 'Процентный рейтинг (0-100%)',
            RatingType.POINTS: 'Произвольные баллы'
        }
        return descriptions.get(rating_type, 'Неизвестный тип')
    
    def _get_rating_type_range(self, rating_type):
        """Получает диапазон значений для типа рейтинга."""
        ranges = {
            RatingType.STAR_RATING: '1.0 - 5.0',
            RatingType.LIKE_DISLIKE: '0.0 или 1.0',
            RatingType.THUMBS: '0.0 или 1.0',
            RatingType.PERCENTAGE: '0.0 - 100.0',
            RatingType.POINTS: '0.0 и выше'
        }
        return ranges.get(rating_type, 'Неизвестный диапазон')


@ratings_api.route('/rating-dimensions', methods=['GET'])
@login_required
def get_rating_dimensions():
    """
    Получает список измерений рейтинга.
    """
    try:
        dimensions_data = []
        for dimension in RatingDimension:
            dimension_data = {
                'name': dimension.name,
                'value': dimension.value,
                'description': self._get_dimension_description(dimension)
            }
            dimensions_data.append(dimension_data)
        
        return jsonify({
            'success': True,
            'dimensions': dimensions_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500
    
    def _get_dimension_description(self, dimension):
        """Получает описание измерения."""
        descriptions = {
            RatingDimension.OVERALL: 'Общий рейтинг',
            RatingDimension.QUALITY: 'Качество',
            RatingDimension.USABILITY: 'Удобство использования',
            RatingDimension.SUPPORT: 'Поддержка',
            RatingDimension.VALUE: 'Соотношение цена/качество',
            RatingDimension.ACCURACY: 'Точность'
        }
        return descriptions.get(dimension, 'Неизвестное измерение')


@ratings_api.route('/review-statuses', methods=['GET'])
@login_required
def get_review_statuses():
    """
    Получает список статусов отзывов.
    """
    try:
        statuses_data = []
        for status in ReviewStatus:
            status_data = {
                'name': status.name,
                'value': status.value,
                'description': self._get_status_description(status)
            }
            statuses_data.append(status_data)
        
        return jsonify({
            'success': True,
            'statuses': statuses_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500
    
    def _get_status_description(self, status):
        """Получает описание статуса."""
        descriptions = {
            ReviewStatus.PENDING: 'Ожидает модерации',
            ReviewStatus.APPROVED: 'Одобрен',
            ReviewStatus.REJECTED: 'Отклонен',
            ReviewStatus.FLAGGED: 'Помечен как подозрительный',
            ReviewStatus.DELETED: 'Удален'
        }
        return descriptions.get(status, 'Неизвестный статус')


@ratings_api.route('/statistics', methods=['GET'])
@login_required
def get_ratings_statistics():
    """
    Получает статистику по рейтингам и отзывам.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        stats = rating_manager.get_statistics()
        return jsonify({
            'success': True,
            'statistics': stats
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@ratings_api.route('/user-contribution/<int:user_id>', methods=['GET'])
@login_required
def get_user_contribution(user_id):
    """
    Получает статистику вклада пользователя.
    """
    try:
        # Проверяем права доступа
        if user_id != current_user.id and not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Недостаточно прав для просмотра статистики другого пользователя'
            }), 403
        
        stats = rating_manager.get_user_contribution_stats(user_id)
        return jsonify({
            'success': True,
            'user_stats': stats
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@ratings_api.route('/rating-methods', methods=['GET'])
@login_required
def get_rating_methods():
    """
    Получает список методов расчета рейтингов.
    """
    try:
        methods = [
            {
                'name': 'average',
                'description': 'Среднее арифметическое всех рейтингов',
                'complexity': 'low'
            },
            {
                'name': 'weighted',
                'description': 'Взвешенное среднее по измерениям',
                'complexity': 'medium'
            },
            {
                'name': 'bayesian',
                'description': 'Байесовский средний (учитывает количество оценок)',
                'complexity': 'high'
            }
        ]
        
        return jsonify({
            'success': True,
            'methods': methods
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@ratings_api.route('/test-rating', methods=['POST'])
@login_required
def test_rating_system():
    """
    Тестовая функция для проверки системы рейтингов.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        # Создаем тестовый рейтинг
        test_rating_id = rating_manager.add_rating(
            target_id='test_target',
            target_type='test',
            user_id=current_user.id,
            rating_type=RatingType.STAR_RATING,
            value=4.5,
            dimension=RatingDimension.OVERALL,
            comment='Тестовый рейтинг',
            metadata={'test': True}
        )
        
        if test_rating_id:
            # Получаем информацию о рейтинге
            rating_info = rating_manager.calculate_target_rating('test_target')
            
            return jsonify({
                'success': True,
                'message': 'Тестовый рейтинг создан успешно',
                'test_rating_id': test_rating_id,
                'rating_info': rating_info
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Не удалось создать тестовый рейтинг'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500