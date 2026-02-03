# -*- coding: utf-8 -*-
"""
API конечные точки расширенной системы комментариев для ПрофиТест
Предоставляет доступ к функциям управления комментариями и отзывами
"""
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.advanced_comments import comment_manager, Comment, CommentType, CommentStatus
import json
from datetime import datetime
import uuid

comments_api = Blueprint('comments_api', __name__)


@comments_api.route('/comments', methods=['GET'])
@login_required
def get_comments():
    """
    Получает список комментариев с фильтрацией и пагинацией.
    """
    try:
        # Параметры фильтрации
        target_id = request.args.get('target_id')
        target_type = request.args.get('target_type')
        comment_type = request.args.get('type')
        status = request.args.get('status')
        author_id = request.args.get('author_id', type=int)
        flagged_only = request.args.get('flagged_only')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        
        # Создаем фильтры
        filters = {}
        if status:
            filters['status'] = status
        if comment_type:
            filters['comment_type'] = comment_type
        if author_id:
            filters['author_id'] = author_id
        if target_id:
            filters['target_id'] = target_id
        if flagged_only:
            filters['flagged_only'] = flagged_only.lower() == 'true'
        
        # Получаем комментарии
        if target_id:
            all_comments = comment_manager.get_comments_by_target(target_id)
        else:
            all_comments = list(comment_manager.comments.values())
        
        # Применяем фильтры
        filtered_comments = []
        for comment in all_comments:
            if comment_manager._matches_filters(comment, filters):
                filtered_comments.append(comment)
        
        # Пагинация
        total_comments = len(filtered_comments)
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        paginated_comments = filtered_comments[start_idx:end_idx]
        
        # Подготавливаем данные для ответа
        comments_data = []
        for comment in paginated_comments:
            comment_data = {
                'id': comment.id,
                'content': comment.content,
                'author_id': comment.author_id,
                'target_id': comment.target_id,
                'target_type': comment.target_type,
                'comment_type': comment.comment_type.value,
                'status': comment.status.value,
                'created_at': comment.created_at.isoformat(),
                'updated_at': comment.updated_at.isoformat(),
                'parent_id': comment.parent_id,
                'likes': comment.likes,
                'dislikes': comment.dislikes,
                'reports': comment.reports,
                'rating': comment.rating,
                'is_edited': comment.is_edited,
                'edited_at': comment.edited_at.isoformat() if comment.edited_at else None,
                'tags': comment.tags
            }
            comments_data.append(comment_data)
        
        return jsonify({
            'success': True,
            'comments': comments_data,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total_comments,
                'pages': (total_comments + per_page - 1) // per_page
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@comments_api.route('/comments/<comment_id>', methods=['GET'])
@login_required
def get_comment(comment_id):
    """
    Получает информацию о конкретном комментарии.
    """
    try:
        comment = comment_manager.get_comment(comment_id)
        if not comment:
            return jsonify({
                'success': False,
                'message': 'Комментарий не найден'
            }), 404
        
        comment_data = {
            'id': comment.id,
            'content': comment.content,
            'author_id': comment.author_id,
            'target_id': comment.target_id,
            'target_type': comment.target_type,
            'comment_type': comment.comment_type.value,
            'status': comment.status.value,
            'created_at': comment.created_at.isoformat(),
            'updated_at': comment.updated_at.isoformat(),
            'parent_id': comment.parent_id,
            'likes': comment.likes,
            'dislikes': comment.dislikes,
            'reports': comment.reports,
            'rating': comment.rating,
            'is_edited': comment.is_edited,
            'edited_at': comment.edited_at.isoformat() if comment.edited_at else None,
            'tags': comment.tags,
            'metadata': comment.metadata
        }
        
        # Получаем дочерние комментарии если есть
        child_comments = comment_manager.get_child_comments(comment_id)
        if child_comments:
            comment_data['replies'] = len(child_comments)
        
        return jsonify({
            'success': True,
            'comment': comment_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@comments_api.route('/comments', methods=['POST'])
@login_required
def create_comment():
    """
    Создает новый комментарий.
    """
    try:
        data = request.get_json()
        
        # Валидация обязательных полей
        required_fields = ['content', 'target_id', 'target_type']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'message': f'Поле {field} обязательно'
                }), 400
        
        # Создаем новый комментарий
        comment_id = str(uuid.uuid4())
        
        new_comment = Comment(
            id=comment_id,
            content=data['content'],
            author_id=current_user.id,
            target_id=data['target_id'],
            target_type=data['target_type'],
            comment_type=CommentType(data.get('comment_type', 'comment')),
            status=CommentStatus.PENDING,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            parent_id=data.get('parent_id'),
            tags=data.get('tags', []),
            metadata=data.get('metadata', {})
        )
        
        if comment_manager.add_comment(new_comment):
            return jsonify({
                'success': True,
                'message': 'Комментарий успешно создан',
                'comment_id': comment_id
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Не удалось создать комментарий'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@comments_api.route('/comments/<comment_id>', methods=['PUT'])
@login_required
def update_comment(comment_id):
    """
    Обновляет комментарий.
    """
    try:
        comment = comment_manager.get_comment(comment_id)
        if not comment:
            return jsonify({
                'success': False,
                'message': 'Комментарий не найден'
            }), 404
        
        # Проверяем права доступа
        if comment.author_id != current_user.id and not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Недостаточно прав для редактирования комментария'
            }), 403
        
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'message': 'Данные для обновления обязательны'
            }), 400
        
        # Подготавливаем поля для обновления
        update_fields = {}
        
        if 'content' in data:
            update_fields['content'] = data['content']
        if 'status' in data:
            update_fields['status'] = CommentStatus(data['status'])
        if 'tags' in data:
            update_fields['tags'] = data['tags']
        if 'metadata' in data:
            update_fields['metadata'] = data['metadata']
        
        if comment_manager.update_comment(comment_id, **update_fields):
            return jsonify({
                'success': True,
                'message': 'Комментарий успешно обновлен'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Не удалось обновить комментарий'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@comments_api.route('/comments/<comment_id>', methods=['DELETE'])
@login_required
def delete_comment(comment_id):
    """
    Удаляет комментарий.
    """
    try:
        comment = comment_manager.get_comment(comment_id)
        if not comment:
            return jsonify({
                'success': False,
                'message': 'Комментарий не найден'
            }), 404
        
        # Проверяем права доступа
        if comment.author_id != current_user.id and not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Недостаточно прав для удаления комментария'
            }), 403
        
        if comment_manager.delete_comment(comment_id):
            return jsonify({
                'success': True,
                'message': 'Комментарий успешно удален'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Не удалось удалить комментарий'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@comments_api.route('/comments/<comment_id>/like', methods=['POST'])
@login_required
def like_comment(comment_id):
    """
    Ставит лайк комментарию.
    """
    try:
        comment = comment_manager.get_comment(comment_id)
        if not comment:
            return jsonify({
                'success': False,
                'message': 'Комментарий не найден'
            }), 404
        
        if comment_manager.add_like(comment_id, current_user.id):
            return jsonify({
                'success': True,
                'message': 'Лайк добавлен',
                'new_like_count': comment.likes + 1
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


@comments_api.route('/comments/<comment_id>/dislike', methods=['POST'])
@login_required
def dislike_comment(comment_id):
    """
    Ставит дизлайк комментарию.
    """
    try:
        comment = comment_manager.get_comment(comment_id)
        if not comment:
            return jsonify({
                'success': False,
                'message': 'Комментарий не найден'
            }), 404
        
        if comment_manager.add_dislike(comment_id, current_user.id):
            return jsonify({
                'success': True,
                'message': 'Дизлайк добавлен',
                'new_dislike_count': comment.dislikes + 1
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Не удалось добавить дизлайк'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@comments_api.route('/comments/<comment_id>/report', methods=['POST'])
@login_required
def report_comment(comment_id):
    """
    Отмечает комментарий как неприемлемый.
    """
    try:
        data = request.get_json()
        reason = data.get('reason', 'Не указана причина')
        
        if comment_manager.report_comment(comment_id, current_user.id, reason):
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


@comments_api.route('/comments/<comment_id>/rate', methods=['POST'])
@login_required
def rate_comment(comment_id):
    """
    Оценивает комментарий.
    """
    try:
        comment = comment_manager.get_comment(comment_id)
        if not comment:
            return jsonify({
                'success': False,
                'message': 'Комментарий не найден'
            }), 404
        
        data = request.get_json()
        rating = data.get('rating')
        
        if not rating or not (0 <= rating <= 5):
            return jsonify({
                'success': False,
                'message': 'Рейтинг должен быть от 0 до 5'
            }), 400
        
        if comment_manager.add_rating(comment_id, current_user.id, rating):
            updated_comment = comment_manager.get_comment(comment_id)
            return jsonify({
                'success': True,
                'message': 'Рейтинг добавлен',
                'new_rating': updated_comment.rating
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


@comments_api.route('/comments/<comment_id>/replies', methods=['GET'])
@login_required
def get_comment_replies(comment_id):
    """
    Получает ответы на комментарий.
    """
    try:
        replies = comment_manager.get_child_comments(comment_id)
        
        replies_data = []
        for reply in replies:
            reply_data = {
                'id': reply.id,
                'content': reply.content,
                'author_id': reply.author_id,
                'created_at': reply.created_at.isoformat(),
                'likes': reply.likes,
                'dislikes': reply.dislikes,
                'rating': reply.rating
            }
            replies_data.append(reply_data)
        
        return jsonify({
            'success': True,
            'replies': replies_data,
            'count': len(replies)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@comments_api.route('/comments/search', methods=['GET'])
@login_required
def search_comments():
    """
    Поиск комментариев.
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
        comment_type = request.args.get('type')
        target_id = request.args.get('target_id')
        
        if comment_type:
            filters['comment_type'] = comment_type
        if target_id:
            filters['target_id'] = target_id
        
        # Выполняем поиск
        results = comment_manager.search_comments(query, filters)
        
        # Подготавливаем результаты
        search_results = []
        for comment in results:
            result = {
                'id': comment.id,
                'content': comment.content,
                'author_id': comment.author_id,
                'target_id': comment.target_id,
                'target_type': comment.target_type,
                'comment_type': comment.comment_type.value,
                'created_at': comment.created_at.isoformat(),
                'likes': comment.likes,
                'dislikes': comment.dislikes,
                'rating': comment.rating
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


@comments_api.route('/comments/types', methods=['GET'])
@login_required
def get_comment_types():
    """
    Получает список типов комментариев.
    """
    try:
        types_data = []
        for comment_type in CommentType:
            type_data = {
                'name': comment_type.name,
                'value': comment_type.value,
                'description': self._get_comment_type_description(comment_type)
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
    
    def _get_comment_type_description(self, comment_type):
        """Получает описание типа комментария."""
        descriptions = {
            CommentType.COMMENT: 'Обычный комментарий',
            CommentType.REVIEW: 'Отзыв',
            CommentType.QUESTION: 'Вопрос',
            CommentType.ANSWER: 'Ответ',
            CommentType.FEEDBACK: 'Обратная связь',
            CommentType.SUGGESTION: 'Предложение'
        }
        return descriptions.get(comment_type, 'Неизвестный тип')


@comments_api.route('/comments/statuses', methods=['GET'])
@login_required
def get_comment_statuses():
    """
    Получает список статусов комментариев.
    """
    try:
        statuses_data = []
        for status in CommentStatus:
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
            CommentStatus.PENDING: 'Ожидает модерации',
            CommentStatus.APPROVED: 'Одобрен',
            CommentStatus.REJECTED: 'Отклонен',
            CommentStatus.FLAGGED: 'Помечен как подозрительный',
            CommentStatus.DELETED: 'Удален'
        }
        return descriptions.get(status, 'Неизвестный статус')


@comments_api.route('/comments/statistics', methods=['GET'])
@login_required
def get_comments_statistics():
    """
    Получает статистику по комментариям.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        stats = comment_manager.get_statistics()
        return jsonify({
            'success': True,
            'statistics': stats
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@comments_api.route('/comments/moderation/queue', methods=['GET'])
@login_required
def get_moderation_queue():
    """
    Получает очередь на модерацию.
    """
    try:
        if not current_user.is_admin and not current_user.is_moderator:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ модератора'
            }), 403
        
        queue = comment_manager.moderation.moderation_queue
        flagged_comments = comment_manager.moderation.flagged_comments
        
        queue_data = []
        for comment_id in queue:
            comment = comment_manager.get_comment(comment_id)
            if comment:
                comment_data = {
                    'id': comment.id,
                    'content': comment.content,
                    'author_id': comment.author_id,
                    'target_id': comment.target_id,
                    'created_at': comment.created_at.isoformat(),
                    'reports': comment.reports,
                    'status': comment.status.value
                }
                queue_data.append(comment_data)
        
        return jsonify({
            'success': True,
            'queue': queue_data,
            'flagged_count': len(flagged_comments),
            'queue_size': len(queue)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@comments_api.route('/comments/<comment_id>/moderate', methods=['POST'])
@login_required
def moderate_comment(comment_id):
    """
    Модерирует комментарий.
    """
    try:
        if not current_user.is_admin and not current_user.is_moderator:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ модератора'
            }), 403
        
        data = request.get_json()
        action = data.get('action')  # 'approve' или 'reject'
        reason = data.get('reason', '')
        
        if action not in ['approve', 'reject']:
            return jsonify({
                'success': False,
                'message': 'Некорректное действие'
            }), 400
        
        comment = comment_manager.get_comment(comment_id)
        if not comment:
            return jsonify({
                'success': False,
                'message': 'Комментарий не найден'
            }), 404
        
        if action == 'approve':
            if comment_manager.moderation.approve_comment(comment_id, current_user.id):
                comment_manager.update_comment(comment_id, status=CommentStatus.APPROVED)
                return jsonify({
                    'success': True,
                    'message': 'Комментарий одобрен'
                })
        else:  # reject
            if comment_manager.moderation.flag_comment(comment_id, reason, current_user.id):
                comment_manager.update_comment(comment_id, status=CommentStatus.REJECTED)
                return jsonify({
                    'success': True,
                    'message': 'Комментарий отклонен'
                })
        
        return jsonify({
            'success': False,
            'message': 'Не удалось выполнить модерацию'
        }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500