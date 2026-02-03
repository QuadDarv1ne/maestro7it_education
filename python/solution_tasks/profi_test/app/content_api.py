# -*- coding: utf-8 -*-
"""
API конечные точки управления контентом для ПрофиТест
Предоставляет доступ к функциям управления контентом и медиа-файлами
"""
from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
from app.content_management import content_manager, ContentType, ContentStatus, ContentCategory, ContentMetadata
import json
from datetime import datetime

content_api = Blueprint('content_api', __name__)


@content_api.route('/content', methods=['GET'])
@login_required
def get_content_list():
    """
    Получает список контента с фильтрацией и пагинацией.
    """
    try:
        # Параметры фильтрации
        content_type = request.args.get('type')
        status = request.args.get('status')
        category = request.args.get('category')
        author_id = request.args.get('author_id', type=int)
        is_premium = request.args.get('is_premium')
        flagged_only = request.args.get('flagged_only')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        
        # Создаем фильтры
        filters = {}
        if content_type:
            filters['content_type'] = content_type
        if status:
            filters['status'] = status
        if category:
            filters['category'] = category
        if author_id:
            filters['author_id'] = author_id
        if is_premium is not None:
            filters['is_premium'] = is_premium.lower() == 'true'
        if flagged_only:
            filters['flagged_only'] = flagged_only.lower() == 'true'
        
        # Получаем весь контент
        all_content = list(content_manager.content.values())
        
        # Применяем фильтры
        filtered_content = []
        for content in all_content:
            if content_manager._matches_filters(content, filters):
                filtered_content.append(content)
        
        # Пагинация
        total_content = len(filtered_content)
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        paginated_content = filtered_content[start_idx:end_idx]
        
        # Подготавливаем данные для ответа
        content_data = []
        for content in paginated_content:
            content_item = {
                'id': content.id,
                'title': content.metadata.title,
                'description': content.metadata.description,
                'content_type': content.content_type.value,
                'status': content.status.value,
                'category': content.metadata.category.value,
                'author_id': content.author_id,
                'created_at': content.created_at.isoformat(),
                'updated_at': content.updated_at.isoformat(),
                'published_at': content.published_at.isoformat() if content.published_at else None,
                'likes': content.likes,
                'views': content.views,
                'rating': content.rating,
                'ratings_count': content.ratings_count,
                'flags': content.flags,
                'is_featured': content.is_featured,
                'is_premium': content.is_premium,
                'tags': content.metadata.tags,
                'difficulty_level': content.metadata.difficulty_level
            }
            content_data.append(content_item)
        
        return jsonify({
            'success': True,
            'content': content_data,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total_content,
                'pages': (total_content + per_page - 1) // per_page
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@content_api.route('/content/<content_id>', methods=['GET'])
@login_required
def get_content(content_id):
    """
    Получает информацию о конкретном контенте.
    """
    try:
        content = content_manager.get_content(content_id)
        if not content:
            return jsonify({
                'success': False,
                'message': 'Контент не найден'
            }), 404
        
        # Проверяем права доступа
        if content.is_premium and not current_user.is_premium and content.author_id != current_user.id:
            if not current_user.is_admin:
                return jsonify({
                    'success': False,
                    'message': 'Недостаточно прав для просмотра премиум контента'
                }), 403
        
        # Увеличиваем счетчик просмотров
        content_manager.increment_view_count(content_id)
        
        content_data = {
            'id': content.id,
            'title': content.metadata.title,
            'description': content.metadata.description,
            'content_type': content.content_type.value,
            'content_data': content.content_data,
            'status': content.status.value,
            'category': content.metadata.category.value,
            'author_id': content.author_id,
            'created_at': content.created_at.isoformat(),
            'updated_at': content.updated_at.isoformat(),
            'published_at': content.published_at.isoformat() if content.published_at else None,
            'version': content.version,
            'likes': content.likes,
            'views': content.views,
            'shares': content.shares,
            'comments_count': content.comments_count,
            'rating': content.rating,
            'ratings_count': content.ratings_count,
            'flags': content.flags,
            'is_featured': content.is_featured,
            'is_premium': content.is_premium,
            'access_level': content.access_level,
            'tags': content.metadata.tags,
            'language': content.metadata.language,
            'difficulty_level': content.metadata.difficulty_level,
            'estimated_time': content.metadata.estimated_time,
            'target_audience': content.metadata.target_audience,
            'prerequisites': content.metadata.prerequisites,
            'learning_outcomes': content.metadata.learning_outcomes
        }
        
        return jsonify({
            'success': True,
            'content': content_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@content_api.route('/content', methods=['POST'])
@login_required
def create_content():
    """
    Создает новый контент.
    """
    try:
        data = request.get_json()
        
        # Валидация обязательных полей
        required_fields = ['title', 'content_type', 'content_data']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'message': f'Поле {field} обязательно'
                }), 400
        
        # Создаем новый контент
        import uuid
        content_id = str(uuid.uuid4())
        
        # Создаем метаданные
        metadata = ContentMetadata(
            title=data['title'],
            description=data.get('description', ''),
            tags=data.get('tags', []),
            category=ContentCategory(data.get('category', 'educational')),
            language=data.get('language', 'ru'),
            difficulty_level=data.get('difficulty_level', 1),
            estimated_time=data.get('estimated_time', 0),
            target_audience=data.get('target_audience', 'general'),
            prerequisites=data.get('prerequisites', []),
            learning_outcomes=data.get('learning_outcomes', [])
        )
        
        from app.content_management import Content
        new_content = Content(
            id=content_id,
            content_type=ContentType(data['content_type']),
            content_data=data['content_data'],
            author_id=current_user.id,
            status=ContentStatus(data.get('status', 'draft')),
            metadata=metadata,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            is_premium=data.get('is_premium', False),
            access_level=data.get('access_level', 0)
        )
        
        if content_manager.add_content(new_content):
            return jsonify({
                'success': True,
                'message': 'Контент успешно создан',
                'content_id': content_id
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Не удалось создать контент'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@content_api.route('/content/<content_id>', methods=['PUT'])
@login_required
def update_content(content_id):
    """
    Обновляет контент.
    """
    try:
        content = content_manager.get_content(content_id)
        if not content:
            return jsonify({
                'success': False,
                'message': 'Контент не найден'
            }), 404
        
        # Проверяем права доступа
        if content.author_id != current_user.id and not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Недостаточно прав для редактирования контента'
            }), 403
        
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'message': 'Данные для обновления обязательны'
            }), 400
        
        # Подготавливаем поля для обновления
        update_fields = {}
        
        # Обновляем метаданные если они переданы
        if any(field in data for field in ['title', 'description', 'tags', 'category']):
            metadata_updates = {}
            if 'title' in data:
                metadata_updates['title'] = data['title']
            if 'description' in data:
                metadata_updates['description'] = data['description']
            if 'tags' in data:
                metadata_updates['tags'] = data['tags']
            if 'category' in data:
                metadata_updates['category'] = ContentCategory(data['category'])
            
            # Обновляем метаданные
            for key, value in metadata_updates.items():
                setattr(content.metadata, key, value)
            update_fields['metadata'] = content.metadata
        
        # Обновляем другие поля
        field_mapping = {
            'content_data': 'content_data',
            'status': lambda x: ContentStatus(x),
            'is_featured': 'is_featured',
            'is_premium': 'is_premium',
            'access_level': 'access_level'
        }
        
        for api_field, content_field in field_mapping.items():
            if api_field in data:
                if callable(content_field):
                    update_fields[api_field] = content_field(data[api_field])
                else:
                    update_fields[content_field] = data[api_field]
        
        if content_manager.update_content(content_id, **update_fields):
            return jsonify({
                'success': True,
                'message': 'Контент успешно обновлен'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Не удалось обновить контент'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@content_api.route('/content/<content_id>', methods=['DELETE'])
@login_required
def delete_content(content_id):
    """
    Удаляет контент.
    """
    try:
        content = content_manager.get_content(content_id)
        if not content:
            return jsonify({
                'success': False,
                'message': 'Контент не найден'
            }), 404
        
        # Проверяем права доступа
        if content.author_id != current_user.id and not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Недостаточно прав для удаления контента'
            }), 403
        
        if content_manager.delete_content(content_id):
            return jsonify({
                'success': True,
                'message': 'Контент успешно удален'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Не удалось удалить контент'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@content_api.route('/content/<content_id>/publish', methods=['POST'])
@login_required
def publish_content(content_id):
    """
    Публикует контент.
    """
    try:
        content = content_manager.get_content(content_id)
        if not content:
            return jsonify({
                'success': False,
                'message': 'Контент не найден'
            }), 404
        
        # Проверяем права доступа
        if content.author_id != current_user.id and not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Недостаточно прав для публикации контента'
            }), 403
        
        if content_manager.update_content(content_id, status=ContentStatus.PUBLISHED, published_at=datetime.now()):
            return jsonify({
                'success': True,
                'message': 'Контент успешно опубликован'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Не удалось опубликовать контент'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@content_api.route('/content/<content_id>/like', methods=['POST'])
@login_required
def like_content(content_id):
    """
    Ставит лайк контенту.
    """
    try:
        content = content_manager.get_content(content_id)
        if not content:
            return jsonify({
                'success': False,
                'message': 'Контент не найден'
            }), 404
        
        if content_manager.increment_like_count(content_id):
            return jsonify({
                'success': True,
                'message': 'Лайк добавлен',
                'new_like_count': content.likes + 1
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Не удалось добавить лайк'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@content_api.route('/content/<content_id>/rate', methods=['POST'])
@login_required
def rate_content(content_id):
    """
    Оценивает контент.
    """
    try:
        content = content_manager.get_content(content_id)
        if not content:
            return jsonify({
                'success': False,
                'message': 'Контент не найден'
            }), 404
        
        data = request.get_json()
        rating = data.get('rating')
        
        if not rating or not (1 <= rating <= 5):
            return jsonify({
                'success': False,
                'message': 'Рейтинг должен быть от 1 до 5'
            }), 400
        
        if content_manager.add_rating(content_id, rating):
            updated_content = content_manager.get_content(content_id)
            return jsonify({
                'success': True,
                'message': 'Рейтинг добавлен',
                'new_rating': updated_content.rating,
                'ratings_count': updated_content.ratings_count
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


@content_api.route('/content/search', methods=['GET'])
@login_required
def search_content():
    """
    Поиск контента.
    """
    try:
        query = request.args.get('q', '')
        if not query:
            return jsonify({
                'success': False,
                'message': 'Поисковый запрос обязателен'
            }), 400
        
        # Параметры фильтрации
        filters = {}
        content_type = request.args.get('type')
        category = request.args.get('category')
        is_premium = request.args.get('is_premium')
        
        if content_type:
            filters['content_type'] = content_type
        if category:
            filters['category'] = category
        if is_premium is not None:
            filters['is_premium'] = is_premium.lower() == 'true'
        
        # Выполняем поиск
        results = content_manager.search_content(query, filters)
        
        # Подготавливаем результаты
        search_results = []
        for content in results:
            result = {
                'id': content.id,
                'title': content.metadata.title,
                'description': content.metadata.description,
                'content_type': content.content_type.value,
                'category': content.metadata.category.value,
                'author_id': content.author_id,
                'created_at': content.created_at.isoformat(),
                'likes': content.likes,
                'views': content.views,
                'rating': content.rating,
                'tags': content.metadata.tags,
                'is_premium': content.is_premium
            }
            search_results.append(result)
        
        return jsonify({
            'success': True,
            'results': search_results,
            'count': len(search_results)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@content_api.route('/content/popular', methods=['GET'])
@login_required
def get_popular_content():
    """
    Получает популярный контент.
    """
    try:
        limit = int(request.args.get('limit', 10))
        popular_content = content_manager.get_popular_content(limit)
        
        content_data = []
        for content in popular_content:
            content_item = {
                'id': content.id,
                'title': content.metadata.title,
                'description': content.metadata.description,
                'content_type': content.content_type.value,
                'category': content.metadata.category.value,
                'author_id': content.author_id,
                'likes': content.likes,
                'views': content.views,
                'rating': content.rating,
                'tags': content.metadata.tags,
                'is_premium': content.is_premium
            }
            content_data.append(content_item)
        
        return jsonify({
            'success': True,
            'content': content_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@content_api.route('/content/featured', methods=['GET'])
@login_required
def get_featured_content():
    """
    Получает избранный контент.
    """
    try:
        featured_content = content_manager.get_featured_content()
        
        content_data = []
        for content in featured_content:
            content_item = {
                'id': content.id,
                'title': content.metadata.title,
                'description': content.metadata.description,
                'content_type': content.content_type.value,
                'category': content.metadata.category.value,
                'author_id': content.author_id,
                'likes': content.likes,
                'views': content.views,
                'rating': content.rating,
                'tags': content.metadata.tags,
                'is_premium': content.is_premium
            }
            content_data.append(content_item)
        
        return jsonify({
            'success': True,
            'content': content_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@content_api.route('/content/types', methods=['GET'])
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
            ContentType.TEXT: 'Текстовый контент',
            ContentType.IMAGE: 'Изображения',
            ContentType.VIDEO: 'Видео контент',
            ContentType.AUDIO: 'Аудио контент',
            ContentType.DOCUMENT: 'Документы',
            ContentType.TEST: 'Тесты и опросы',
            ContentType.QUESTION: 'Вопросы',
            ContentType.ANSWER: 'Ответы',
            ContentType.COMMENT: 'Комментарии',
            ContentType.REVIEW: 'Отзывы'
        }
        return descriptions.get(content_type, 'Неизвестный тип')


@content_api.route('/content/categories', methods=['GET'])
@login_required
def get_content_categories():
    """
    Получает список категорий контента.
    """
    try:
        categories_data = []
        for category in ContentCategory:
            category_data = {
                'name': category.name,
                'value': category.value,
                'description': self._get_category_description(category)
            }
            categories_data.append(category_data)
        
        return jsonify({
            'success': True,
            'categories': categories_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500
    
    def _get_category_description(self, category):
        """Получает описание категории."""
        descriptions = {
            ContentCategory.EDUCATIONAL: 'Образовательный контент',
            ContentCategory.ENTERTAINMENT: 'Развлекательный контент',
            ContentCategory.NEWS: 'Новости',
            ContentCategory.TUTORIAL: 'Обучающие материалы',
            ContentCategory.REFERENCE: 'Справочные материалы',
            ContentCategory.USER_GENERATED: 'Контент пользователей'
        }
        return descriptions.get(category, 'Неизвестная категория')


@content_api.route('/content/statistics', methods=['GET'])
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
        
        stats = content_manager.get_statistics()
        return jsonify({
            'success': True,
            'statistics': stats
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@content_api.route('/content/upload-media', methods=['POST'])
@login_required
def upload_media():
    """
    Загружает медиа-файл.
    """
    try:
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'message': 'Файл обязателен'
            }), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({
                'success': False,
                'message': 'Выберите файл для загрузки'
            }), 400
        
        # Читаем файл
        file_data = file.read()
        filename = file.filename
        content_type = file.content_type or 'application/octet-stream'
        
        # Загружаем файл
        file_id = content_manager.upload_media_file(file_data, filename, content_type)
        
        if file_id:
            return jsonify({
                'success': True,
                'message': 'Файл успешно загружен',
                'file_id': file_id
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Не удалось загрузить файл'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@content_api.route('/content/media/<file_id>', methods=['GET'])
@login_required
def get_media_info(file_id):
    """
    Получает информацию о медиа-файле.
    """
    try:
        file_info = content_manager.get_media_file_info(file_id)
        if not file_info:
            return jsonify({
                'success': False,
                'message': 'Файл не найден'
            }), 404
        
        return jsonify({
            'success': True,
            'file_info': file_info
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500