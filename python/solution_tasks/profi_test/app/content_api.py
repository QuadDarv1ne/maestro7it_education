# -*- coding: utf-8 -*-
"""
API конечные точки расширенной системы управления контентом для ПрофиТест
Предоставляет доступ к функциям модерации, анализа качества и оптимизации контента
"""
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.content_management import (
    content_moderation_engine, content_quality_analyzer, 
    content_optimizer, ContentItem, ContentType, ContentStatus, ContentQuality
)
import json
from datetime import datetime

content_api_v2 = Blueprint('content_api_v2', __name__)


@content_api_v2.route('/content/moderate', methods=['POST'])
@login_required
def moderate_content():
    """
    Модерирует контент по установленным правилам.
    """
    try:
        data = request.get_json()
        
        # Валидация обязательных полей
        required_fields = ['id', 'title', 'description', 'content_type', 'author_id']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'message': f'Поле {field} обязательно'
                }), 400
        
        # Создаем объект контента
        content = ContentItem(
            id=data['id'],
            title=data['title'],
            description=data['description'],
            content_type=ContentType(data.get('content_type', 'article')),
            author_id=data['author_id'],
            status=ContentStatus(data.get('status', 'draft')),
            quality_score=data.get('quality_score', 0.0),
            quality_level=ContentQuality(data.get('quality_level', 'needs_improvement')),
            tags=data.get('tags', []),
            category=data.get('category', ''),
            created_at=datetime.fromisoformat(data['created_at']) if 'created_at' in data else datetime.now(),
            updated_at=datetime.fromisoformat(data['updated_at']) if 'updated_at' in data else datetime.now(),
            metadata=data.get('metadata', {})
        )
        
        # Выполняем модерацию
        moderation_result = content_moderation_engine.moderate_content(content)
        
        return jsonify({
            'success': True,
            'moderation_result': moderation_result
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@content_api_v2.route('/content/quality/analyze', methods=['POST'])
@login_required
def analyze_content_quality():
    """
    Анализирует качество контента.
    """
    try:
        data = request.get_json()
        
        # Валидация обязательных полей
        required_fields = ['id', 'title', 'description']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'message': f'Поле {field} обязательно'
                }), 400
        
        # Создаем объект контента
        content = ContentItem(
            id=data['id'],
            title=data['title'],
            description=data['description'],
            content_type=ContentType(data.get('content_type', 'article')),
            author_id=data.get('author_id', current_user.id),
            status=ContentStatus(data.get('status', 'draft')),
            quality_score=data.get('quality_score', 0.0),
            quality_level=ContentQuality(data.get('quality_level', 'needs_improvement')),
            tags=data.get('tags', []),
            category=data.get('category', ''),
            created_at=datetime.fromisoformat(data['created_at']) if 'created_at' in data else datetime.now(),
            updated_at=datetime.fromisoformat(data['updated_at']) if 'updated_at' in data else datetime.now(),
            metadata=data.get('metadata', {})
        )
        
        # Анализируем качество
        quality_analysis = content_quality_analyzer.analyze_content_quality(content)
        
        return jsonify({
            'success': True,
            'quality_analysis': quality_analysis
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@content_api_v2.route('/content/optimize', methods=['POST'])
@login_required
def optimize_content():
    """
    Генерирует рекомендации по оптимизации контента.
    """
    try:
        data = request.get_json()
        
        # Создаем объект контента
        content = ContentItem(
            id=data['id'],
            title=data['title'],
            description=data['description'],
            content_type=ContentType(data.get('content_type', 'article')),
            author_id=data.get('author_id', current_user.id),
            status=ContentStatus(data.get('status', 'draft')),
            quality_score=data.get('quality_score', 0.0),
            quality_level=ContentQuality(data.get('quality_level', 'needs_improvement')),
            tags=data.get('tags', []),
            category=data.get('category', ''),
            created_at=datetime.fromisoformat(data['created_at']) if 'created_at' in data else datetime.now(),
            updated_at=datetime.fromisoformat(data['updated_at']) if 'updated_at' in data else datetime.now(),
            metadata=data.get('metadata', {})
        )
        
        # Создаем метрики если предоставлены
        metrics = None
        if 'metrics' in data:
            metrics_data = data['metrics']
            metrics = ContentMetrics(
                content_id=data['id'],
                views=metrics_data.get('views', 0),
                unique_views=metrics_data.get('unique_views', 0),
                likes=metrics_data.get('likes', 0),
                shares=metrics_data.get('shares', 0),
                completion_rate=metrics_data.get('completion_rate', 0.0),
                avg_time_spent=metrics_data.get('avg_time_spent', 0.0),
                bounce_rate=metrics_data.get('bounce_rate', 0.0),
                engagement_score=metrics_data.get('engagement_score', 0.0)
            )
        
        # Генерируем рекомендации
        recommendations = content_optimizer.generate_optimization_recommendations(content, metrics)
        
        return jsonify({
            'success': True,
            'content_id': content.id,
            'recommendations': recommendations,
            'recommendations_count': len(recommendations)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@content_api_v2.route('/content/moderation/history', methods=['GET'])
@login_required
def get_moderation_history():
    """
    Получает историю модерации контента.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        content_id = request.args.get('content_id')
        
        history = content_moderation_engine.get_moderation_history(content_id)
        
        # Преобразуем в JSON-сериализуемый формат
        history_data = []
        for record in history:
            history_data.append({
                'content_id': record['content_id'],
                'result': record['result'],
                'timestamp': record['timestamp'].isoformat()
            })
        
        return jsonify({
            'success': True,
            'history': history_data,
            'count': len(history_data)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@content_api_v2.route('/content/flagged', methods=['GET'])
@login_required
def get_flagged_content():
    """
    Получает список отмеченного контента.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        flagged_content = content_moderation_engine.get_flagged_content()
        
        return jsonify({
            'success': True,
            'flagged_content': flagged_content,
            'count': len(flagged_content)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@content_api_v2.route('/content/batch/moderate', methods=['POST'])
@login_required
def batch_moderate_content():
    """
    Выполняет пакетную модерацию нескольких элементов контента.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        data = request.get_json()
        contents = data.get('contents', [])
        
        if not contents:
            return jsonify({
                'success': False,
                'message': 'Список контента не может быть пустым'
            }), 400
        
        batch_results = {}
        
        for i, content_data in enumerate(contents):
            try:
                content = ContentItem(
                    id=content_data['id'],
                    title=content_data['title'],
                    description=content_data['description'],
                    content_type=ContentType(content_data.get('content_type', 'article')),
                    author_id=content_data['author_id'],
                    status=ContentStatus(content_data.get('status', 'draft')),
                    quality_score=content_data.get('quality_score', 0.0),
                    quality_level=ContentQuality(content_data.get('quality_level', 'needs_improvement')),
                    tags=content_data.get('tags', []),
                    category=content_data.get('category', ''),
                    created_at=datetime.fromisoformat(content_data['created_at']) if 'created_at' in content_data else datetime.now(),
                    updated_at=datetime.fromisoformat(content_data['updated_at']) if 'updated_at' in content_data else datetime.now(),
                    metadata=content_data.get('metadata', {})
                )
                
                moderation_result = content_moderation_engine.moderate_content(content)
                batch_results[f'content_{i}'] = moderation_result
                
            except Exception as e:
                batch_results[f'content_{i}'] = {'error': str(e)}
        
        return jsonify({
            'success': True,
            'batch_results': batch_results,
            'total_contents': len(contents)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@content_api_v2.route('/content/batch/quality', methods=['POST'])
@login_required
def batch_analyze_content_quality():
    """
    Выполняет пакетный анализ качества нескольких элементов контента.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        data = request.get_json()
        contents = data.get('contents', [])
        
        if not contents:
            return jsonify({
                'success': False,
                'message': 'Список контента не может быть пустым'
            }), 400
        
        batch_results = {}
        
        for i, content_data in enumerate(contents):
            try:
                content = ContentItem(
                    id=content_data['id'],
                    title=content_data['title'],
                    description=content_data['description'],
                    content_type=ContentType(content_data.get('content_type', 'article')),
                    author_id=content_data['author_id'],
                    status=ContentStatus(content_data.get('status', 'draft')),
                    quality_score=content_data.get('quality_score', 0.0),
                    quality_level=ContentQuality(content_data.get('quality_level', 'needs_improvement')),
                    tags=content_data.get('tags', []),
                    category=content_data.get('category', ''),
                    created_at=datetime.fromisoformat(content_data['created_at']) if 'created_at' in content_data else datetime.now(),
                    updated_at=datetime.fromisoformat(content_data['updated_at']) if 'updated_at' in content_data else datetime.now(),
                    metadata=content_data.get('metadata', {})
                )
                
                quality_analysis = content_quality_analyzer.analyze_content_quality(content)
                batch_results[f'content_{i}'] = quality_analysis
                
            except Exception as e:
                batch_results[f'content_{i}'] = {'error': str(e)}
        
        return jsonify({
            'success': True,
            'batch_results': batch_results,
            'total_contents': len(contents)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@content_api_v2.route('/content/types', methods=['GET'])
@login_required
def get_content_types():
    """
    Получает список типов контента.
    """
    try:
        types_data = []
        for content_type in ContentType:
            type_data = {
                'name': content_type.name,
                'value': content_type.value,
                'description': self._get_content_type_description(content_type)
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
    
    def _get_content_type_description(self, content_type):
        """Получает описание типа контента."""
        descriptions = {
            ContentType.TEST: 'Интерактивный тест',
            ContentType.ARTICLE: 'Статья',
            ContentType.VIDEO: 'Видео',
            ContentType.COURSE: 'Обучающий курс',
            ContentType.PODCAST: 'Подкаст',
            ContentType.INTERACTIVE: 'Интерактивный контент'
        }
        return descriptions.get(content_type, 'Неизвестный тип контента')


@content_api_v2.route('/content/statuses', methods=['GET'])
@login_required
def get_content_statuses():
    """
    Получает список статусов контента.
    """
    try:
        statuses_data = []
        for status in ContentStatus:
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
        """Получает описание статуса контента."""
        descriptions = {
            ContentStatus.DRAFT: 'Черновик',
            ContentStatus.PENDING_REVIEW: 'На модерации',
            ContentStatus.PUBLISHED: 'Опубликован',
            ContentStatus.ARCHIVED: 'В архиве',
            ContentStatus.REJECTED: 'Отклонен'
        }
        return descriptions.get(status, 'Неизвестный статус')


@content_api_v2.route('/content/quality/levels', methods=['GET'])
@login_required
def get_quality_levels():
    """
    Получает список уровней качества контента.
    """
    try:
        levels_data = []
        for level in ContentQuality:
            level_data = {
                'name': level.name,
                'value': level.value,
                'description': self._get_quality_level_description(level)
            }
            levels_data.append(level_data)
        
        return jsonify({
            'success': True,
            'quality_levels': levels_data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500
    
    def _get_quality_level_description(self, level):
        """Получает описание уровня качества контента."""
        descriptions = {
            ContentQuality.EXCELLENT: 'Отличное качество',
            ContentQuality.GOOD: 'Хорошее качество',
            ContentQuality.AVERAGE: 'Среднее качество',
            ContentQuality.POOR: 'Низкое качество',
            ContentQuality.NEEDS_IMPROVEMENT: 'Требует улучшения'
        }
        return descriptions.get(level, 'Неизвестный уровень качества')


@content_api_v2.route('/content/statistics', methods=['GET'])
@login_required
def get_content_statistics():
    """
    Получает статистику по контенту.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        # В реальной системе здесь будет запрос к базе данных
        # Пока возвращаем тестовые данные
        stats = {
            'total_content': 150,
            'content_by_type': {
                'test': 45,
                'article': 60,
                'video': 25,
                'course': 15,
                'other': 5
            },
            'content_by_status': {
                'published': 120,
                'draft': 20,
                'pending_review': 8,
                'archived': 2
            },
            'quality_distribution': {
                'excellent': 25,
                'good': 65,
                'average': 40,
                'poor': 15,
                'needs_improvement': 5
            },
            'flagged_content': len(content_moderation_engine.get_flagged_content())
        }
        
        return jsonify({
            'success': True,
            'statistics': stats
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@content_api_v2.route('/content/test', methods=['POST'])
@login_required
def test_content_management():
    """
    Тестовая функция для проверки системы управления контентом.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        # Создаем тестовый контент
        test_content = ContentItem(
            id='test_content_1',
            title='Тестовая статья о профориентации',
            description='Полезная статья о выборе профессии и профориентации для студентов',
            content_type=ContentType.ARTICLE,
            author_id=current_user.id,
            status=ContentStatus.DRAFT,
            quality_score=0.0,
            quality_level=ContentQuality.NEEDS_IMPROVEMENT,
            tags=['профориентация', 'карьера', 'обучение'],
            category='career',
            created_at=datetime.now(),
            updated_at=datetime.now(),
            metadata={
                'difficulty': 'medium',
                'estimated_time': 15,
                'target_audience': 'students'
            }
        )
        
        # Выполняем модерацию
        moderation_result = content_moderation_engine.moderate_content(test_content)
        
        # Анализируем качество
        quality_analysis = content_quality_analyzer.analyze_content_quality(test_content)
        
        # Генерируем рекомендации
        recommendations = content_optimizer.generate_optimization_recommendations(test_content)
        
        return jsonify({
            'success': True,
            'message': 'Тестовая система управления контентом выполнена успешно',
            'test_results': {
                'content_id': test_content.id,
                'moderation_status': moderation_result['status'],
                'moderation_score': moderation_result['score'],
                'quality_score': quality_analysis['overall_score'],
                'quality_level': quality_analysis['quality_level'],
                'recommendations_count': len(recommendations)
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500