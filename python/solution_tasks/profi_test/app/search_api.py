# -*- coding: utf-8 -*-
"""
API конечные точки расширенной системы поиска для ПрофиТест
Предоставляет доступ к функциям продвинутого поиска по контенту и пользователям
"""
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.advanced_search import search_engine, SearchType
import json
from datetime import datetime

search_api = Blueprint('search_api', __name__)


@search_api.route('/search', methods=['GET'])
@login_required
def search_content():
    """
    Выполняет поиск по контенту и пользователям.
    """
    try:
        # Получаем параметры запроса
        query = request.args.get('q', '').strip()
        if not query:
            return jsonify({
                'success': False,
                'message': 'Поисковый запрос не может быть пустым'
            }), 400
        
        search_type_str = request.args.get('type', 'all')
        try:
            search_type = SearchType(search_type_str)
        except ValueError:
            search_type = SearchType.ALL
        
        # Получаем фильтры
        filters = {}
        category = request.args.get('category')
        if category:
            filters['category'] = category
        
        content_type = request.args.get('content_type')
        if content_type:
            filters['content_type'] = content_type
        
        difficulty = request.args.get('difficulty')
        if difficulty:
            filters['difficulty'] = difficulty
        
        status = request.args.get('status')
        if status:
            filters['status'] = status
        
        tags = request.args.get('tags')
        if tags:
            filters['tags'] = tags.split(',')
        
        # Получаем параметры сортировки и пагинации
        sort_by = request.args.get('sort_by', 'relevance')
        sort_order = request.args.get('sort_order', 'desc')
        page = int(request.args.get('page', 1))
        per_page = min(int(request.args.get('per_page', 20)), 100)  # Ограничиваем максимум
        
        # Выполняем поиск
        results = search_engine.search(
            query=query,
            search_type=search_type,
            filters=filters,
            sort_by=sort_by,
            sort_order=sort_order,
            page=page,
            per_page=per_page,
            user_id=current_user.id
        )
        
        return jsonify(results)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@search_api.route('/search/suggestions', methods=['GET'])
@login_required
def get_search_suggestions():
    """
    Получает предложения для автозаполнения поиска.
    """
    try:
        query_prefix = request.args.get('q', '').strip()
        if not query_prefix:
            return jsonify({
                'success': False,
                'message': 'Префикс запроса не может быть пустым'
            }), 400
        
        limit = int(request.args.get('limit', 10))
        
        suggestions = search_engine.get_search_suggestions(query_prefix, limit)
        
        return jsonify({
            'success': True,
            'suggestions': suggestions,
            'count': len(suggestions)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@search_api.route('/search/popular', methods=['GET'])
@login_required
def get_popular_searches():
    """
    Получает популярные поисковые запросы.
    """
    try:
        limit = int(request.args.get('limit', 10))
        
        popular_searches = search_engine.get_popular_searches(limit)
        
        return jsonify({
            'success': True,
            'popular_searches': popular_searches,
            'count': len(popular_searches)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@search_api.route('/search/history', methods=['GET'])
@login_required
def get_search_history():
    """
    Получает историю поиска пользователя.
    """
    try:
        limit = int(request.args.get('limit', 20))
        offset = int(request.args.get('offset', 0))
        
        # Фильтруем историю по текущему пользователю
        user_history = [
            record for record in search_engine.search_history 
            if record.get('user_id') == current_user.id
        ]
        
        # Сортируем по времени
        user_history.sort(key=lambda x: x['timestamp'], reverse=True)
        
        # Применяем пагинацию
        paginated_history = user_history[offset:offset + limit]
        
        return jsonify({
            'success': True,
            'history': paginated_history,
            'total': len(user_history),
            'count': len(paginated_history)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@search_api.route('/search/history/<search_id>', methods=['DELETE'])
@login_required
def delete_search_history_item(search_id):
    """
    Удаляет элемент из истории поиска.
    """
    try:
        # Находим и удаляем запись из истории
        history_item = None
        for i, record in enumerate(search_engine.search_history):
            if record.get('search_id') == search_id and record.get('user_id') == current_user.id:
                history_item = search_engine.search_history.pop(i)
                break
        
        if history_item:
            return jsonify({
                'success': True,
                'message': 'Элемент истории поиска удален'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Элемент истории поиска не найден'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@search_api.route('/search/history', methods=['DELETE'])
@login_required
def clear_search_history():
    """
    Очищает всю историю поиска пользователя.
    """
    try:
        # Удаляем все записи пользователя из истории
        initial_count = len(search_engine.search_history)
        search_engine.search_history = [
            record for record in search_engine.search_history 
            if record.get('user_id') != current_user.id
        ]
        deleted_count = initial_count - len(search_engine.search_history)
        
        return jsonify({
            'success': True,
            'message': f'История поиска очищена. Удалено {deleted_count} записей'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@search_api.route('/search/content', methods=['POST'])
@login_required
def add_content_to_search():
    """
    Добавляет контент в индекс поиска.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        data = request.get_json()
        
        # Валидация обязательных полей
        required_fields = ['id', 'title', 'type']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'message': f'Поле {field} обязательно'
                }), 400
        
        success = search_engine.add_content(data)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Контент добавлен в индекс поиска'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Не удалось добавить контент в индекс поиска'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@search_api.route('/search/user', methods=['POST'])
@login_required
def add_user_to_search():
    """
    Добавляет пользователя в индекс поиска.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        data = request.get_json()
        
        # Валидация обязательных полей
        required_fields = ['id', 'name', 'username']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'message': f'Поле {field} обязательно'
                }), 400
        
        success = search_engine.add_user(data)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Пользователь добавлен в индекс поиска'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Не удалось добавить пользователя в индекс поиска'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@search_api.route('/search/statistics', methods=['GET'])
@login_required
def get_search_statistics():
    """
    Получает статистику по поиску.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        stats = search_engine.get_search_statistics()
        
        return jsonify({
            'success': True,
            'statistics': stats
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@search_api.route('/search/types', methods=['GET'])
@login_required
def get_search_types():
    """
    Получает список доступных типов поиска.
    """
    try:
        types_data = []
        for search_type in SearchType:
            type_data = {
                'name': search_type.name,
                'value': search_type.value,
                'description': self._get_search_type_description(search_type)
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
    
    def _get_search_type_description(self, search_type):
        """Получает описание типа поиска."""
        descriptions = {
            SearchType.CONTENT: 'Поиск по контенту',
            SearchType.USER: 'Поиск по пользователям',
            SearchType.TEST: 'Поиск по тестам',
            SearchType.ARTICLE: 'Поиск по статьям',
            SearchType.VIDEO: 'Поиск по видео',
            SearchType.ALL: 'Поиск по всему контенту'
        }
        return descriptions.get(search_type, 'Неизвестный тип поиска')


@search_api.route('/search/filters', methods=['GET'])
@login_required
def get_search_filters():
    """
    Получает список доступных фильтров поиска.
    """
    try:
        filters_data = [
            {
                'name': 'category',
                'type': 'string',
                'description': 'Фильтр по категории'
            },
            {
                'name': 'content_type',
                'type': 'string',
                'description': 'Фильтр по типу контента'
            },
            {
                'name': 'difficulty',
                'type': 'string',
                'description': 'Фильтр по сложности'
            },
            {
                'name': 'status',
                'type': 'string',
                'description': 'Фильтр по статусу'
            },
            {
                'name': 'tags',
                'type': 'array',
                'description': 'Фильтр по тегам'
            },
            {
                'name': 'date_range',
                'type': 'object',
                'description': 'Фильтр по диапазону дат'
            },
            {
                'name': 'rating',
                'type': 'object',
                'description': 'Фильтр по рейтингу'
            }
        ]
        
        return jsonify({
            'success': True,
            'filters': filters_data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@search_api.route('/search/advanced', methods=['POST'])
@login_required
def advanced_search():
    """
    Выполняет расширенный поиск с комплексными параметрами.
    """
    try:
        data = request.get_json()
        
        # Обязательные параметры
        query = data.get('query', '').strip()
        if not query:
            return jsonify({
                'success': False,
                'message': 'Поисковый запрос не может быть пустым'
            }), 400
        
        # Опциональные параметры
        search_type_str = data.get('search_type', 'all')
        try:
            search_type = SearchType(search_type_str)
        except ValueError:
            search_type = SearchType.ALL
        
        filters = data.get('filters', {})
        sort_by = data.get('sort_by', 'relevance')
        sort_order = data.get('sort_order', 'desc')
        page = data.get('page', 1)
        per_page = min(data.get('per_page', 20), 100)
        
        # Выполняем поиск
        results = search_engine.search(
            query=query,
            search_type=search_type,
            filters=filters,
            sort_by=sort_by,
            sort_order=sort_order,
            page=page,
            per_page=per_page,
            user_id=current_user.id
        )
        
        return jsonify({
            'success': True,
            'results': results,
            'search_parameters': {
                'query': query,
                'search_type': search_type.value,
                'filters': filters,
                'sort_by': sort_by,
                'sort_order': sort_order,
                'page': page,
                'per_page': per_page
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@search_api.route('/search/batch', methods=['POST'])
@login_required
def batch_search():
    """
    Выполняет пакетный поиск по нескольким запросам.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        data = request.get_json()
        queries = data.get('queries', [])
        
        if not queries:
            return jsonify({
                'success': False,
                'message': 'Список запросов не может быть пустым'
            }), 400
        
        batch_results = {}
        
        for i, query_data in enumerate(queries):
            try:
                query = query_data.get('query', '')
                if not query:
                    batch_results[f'query_{i}'] = {'error': 'Пустой запрос'}
                    continue
                
                search_type_str = query_data.get('search_type', 'all')
                try:
                    search_type = SearchType(search_type_str)
                except ValueError:
                    search_type = SearchType.ALL
                
                filters = query_data.get('filters', {})
                limit = min(query_data.get('limit', 10), 50)
                
                # Выполняем поиск
                results = search_engine.search(
                    query=query,
                    search_type=search_type,
                    filters=filters,
                    sort_by='relevance',
                    sort_order='desc',
                    page=1,
                    per_page=limit,
                    user_id=current_user.id
                )
                
                batch_results[f'query_{i}'] = results
                
            except Exception as e:
                batch_results[f'query_{i}'] = {'error': str(e)}
        
        return jsonify({
            'success': True,
            'batch_results': batch_results,
            'total_queries': len(queries)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@search_api.route('/search/test', methods=['POST'])
@login_required
def test_search_system():
    """
    Тестовая функция для проверки системы поиска.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        # Добавляем тестовый контент
        test_content = {
            'id': 'test_content_1',
            'type': 'test',
            'title': 'Тестовый профориентационный тест',
            'description': 'Тест для проверки системы поиска',
            'category': 'test',
            'tags': ['тест', 'профориентация', 'психология'],
            'difficulty': 'medium',
            'status': 'published',
            'rating': 4.0
        }
        
        search_engine.add_content(test_content)
        
        # Выполняем тестовый поиск
        test_results = search_engine.search(
            query='профориентация',
            search_type=SearchType.ALL,
            user_id=current_user.id
        )
        
        # Получаем статистику
        stats = search_engine.get_search_statistics()
        
        return jsonify({
            'success': True,
            'message': 'Тестовая система поиска выполнена успешно',
            'test_results': test_results.get('results', []),
            'statistics': stats,
            'content_added': True
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500