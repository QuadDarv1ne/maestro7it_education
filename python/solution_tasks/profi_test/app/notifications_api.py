# -*- coding: utf-8 -*-
"""
API конечные точки расширенной системы уведомлений для ПрофиТест
Предоставляет доступ к функциям управления уведомлениями
"""
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.advanced_notifications import notification_manager, NotificationType, NotificationStatus, NotificationPriority, NotificationChannel
import json
from datetime import datetime

notifications_api = Blueprint('notifications_api', __name__)


@notifications_api.route('/notifications', methods=['GET'])
@login_required
def get_notifications():
    """
    Получает список уведомлений пользователя с фильтрацией и пагинацией.
    """
    try:
        # Параметры фильтрации
        status = request.args.get('status')
        notification_type = request.args.get('type')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        
        # Создаем фильтры
        status_filter = NotificationStatus(status) if status else None
        type_filter = NotificationType(notification_type) if notification_type else None
        
        # Получаем уведомления пользователя
        all_notifications = notification_manager.get_user_notifications(
            current_user.id, 
            status=status_filter, 
            notification_type=type_filter
        )
        
        # Пагинация
        total_notifications = len(all_notifications)
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        paginated_notifications = all_notifications[start_idx:end_idx]
        
        # Подготавливаем данные для ответа
        notifications_data = []
        for notification in paginated_notifications:
            notification_data = {
                'id': notification.id,
                'title': notification.title,
                'message': notification.message,
                'notification_type': notification.notification_type.value,
                'priority': notification.priority.value,
                'status': notification.status.value,
                'created_at': notification.created_at.isoformat(),
                'read_at': notification.read_at.isoformat() if notification.read_at else None,
                'expires_at': notification.expires_at.isoformat() if notification.expires_at else None,
                'channels': [c.value for c in notification.channels],
                'data': notification.data,
                'is_sent': notification.is_sent,
                'delivery_attempts': notification.delivery_attempts
            }
            notifications_data.append(notification_data)
        
        return jsonify({
            'success': True,
            'notifications': notifications_data,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total_notifications,
                'pages': (total_notifications + per_page - 1) // per_page
            },
            'unread_count': notification_manager.get_unread_count(current_user.id)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@notifications_api.route('/notifications/<notification_id>', methods=['GET'])
@login_required
def get_notification(notification_id):
    """
    Получает информацию о конкретном уведомлении.
    """
    try:
        notification = notification_manager.get_notification(notification_id)
        if not notification:
            return jsonify({
                'success': False,
                'message': 'Уведомление не найдено'
            }), 404
        
        # Проверяем права доступа
        if notification.user_id != current_user.id:
            return jsonify({
                'success': False,
                'message': 'Недостаточно прав для просмотра уведомления'
            }), 403
        
        notification_data = {
            'id': notification.id,
            'title': notification.title,
            'message': notification.message,
            'notification_type': notification.notification_type.value,
            'priority': notification.priority.value,
            'status': notification.status.value,
            'created_at': notification.created_at.isoformat(),
            'read_at': notification.read_at.isoformat() if notification.read_at else None,
            'expires_at': notification.expires_at.isoformat() if notification.expires_at else None,
            'channels': [c.value for c in notification.channels],
            'data': notification.data,
            'is_sent': notification.is_sent,
            'sent_channels': [c.value for c in notification.sent_channels],
            'delivery_attempts': notification.delivery_attempts,
            'max_delivery_attempts': notification.max_delivery_attempts
        }
        
        # Помечаем как прочитанное если еще не прочитано
        if notification.status == NotificationStatus.UNREAD:
            notification_manager.mark_as_read(notification_id)
        
        return jsonify({
            'success': True,
            'notification': notification_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@notifications_api.route('/notifications', methods=['POST'])
@login_required
def create_notification():
    """
    Создает новое уведомление.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        data = request.get_json()
        
        # Валидация обязательных полей
        required_fields = ['user_id', 'notification_type', 'title', 'message']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'message': f'Поле {field} обязательно'
                }), 400
        
        # Создаем новое уведомление
        notification_id = notification_manager.create_notification(
            user_id=data['user_id'],
            notification_type=NotificationType(data['notification_type']),
            title=data['title'],
            message=data['message'],
            priority=NotificationPriority(data.get('priority', 'normal')),
            data=data.get('data', {}),
            channels=[NotificationChannel(c) for c in data.get('channels', [])],
            expires_in_hours=data.get('expires_in_hours', 168)
        )
        
        if notification_id:
            # Отправляем уведомление
            notification_manager.send_notification(notification_id)
            
            return jsonify({
                'success': True,
                'message': 'Уведомление успешно создано и отправлено',
                'notification_id': notification_id
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Не удалось создать уведомление'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@notifications_api.route('/notifications/<notification_id>/read', methods=['POST'])
@login_required
def mark_notification_read(notification_id):
    """
    Помечает уведомление как прочитанное.
    """
    try:
        notification = notification_manager.get_notification(notification_id)
        if not notification:
            return jsonify({
                'success': False,
                'message': 'Уведомление не найдено'
            }), 404
        
        # Проверяем права доступа
        if notification.user_id != current_user.id:
            return jsonify({
                'success': False,
                'message': 'Недостаточно прав для изменения уведомления'
            }), 403
        
        if notification_manager.mark_as_read(notification_id):
            return jsonify({
                'success': True,
                'message': 'Уведомление помечено как прочитанное'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Не удалось пометить уведомление как прочитанное'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@notifications_api.route('/notifications/read-all', methods=['POST'])
@login_required
def mark_all_notifications_read():
    """
    Помечает все уведомления пользователя как прочитанные.
    """
    try:
        marked_count = notification_manager.mark_multiple_as_read(current_user.id)
        
        return jsonify({
            'success': True,
            'message': f'Помечено {marked_count} уведомлений как прочитанные',
            'marked_count': marked_count
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@notifications_api.route('/notifications/<notification_id>', methods=['DELETE'])
@login_required
def delete_notification(notification_id):
    """
    Удаляет уведомление.
    """
    try:
        notification = notification_manager.get_notification(notification_id)
        if not notification:
            return jsonify({
                'success': False,
                'message': 'Уведомление не найдено'
            }), 404
        
        # Проверяем права доступа
        if notification.user_id != current_user.id and not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Недостаточно прав для удаления уведомления'
            }), 403
        
        if notification_manager.delete_notification(notification_id):
            return jsonify({
                'success': True,
                'message': 'Уведомление успешно удалено'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Не удалось удалить уведомление'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@notifications_api.route('/notifications/preferences', methods=['GET'])
@login_required
def get_notification_preferences():
    """
    Получает настройки уведомлений пользователя.
    """
    try:
        preferences = notification_manager.get_user_preferences(current_user.id)
        
        preferences_data = {
            'global_enabled': preferences.global_enabled,
            'digest_enabled': preferences.digest_enabled,
            'digest_frequency': preferences.digest_frequency,
            'quiet_hours': preferences.quiet_hours,
            'notification_types': {}
        }
        
        # Преобразуем настройки по типам
        for notif_type, channels in preferences.preferences.items():
            preferences_data['notification_types'][notif_type.value] = {
                channel.value: enabled for channel, enabled in channels.items()
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


@notifications_api.route('/notifications/preferences', methods=['PUT'])
@login_required
def update_notification_preferences():
    """
    Обновляет настройки уведомлений пользователя.
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'message': 'Данные для обновления обязательны'
            }), 400
        
        if notification_manager.update_user_preferences(current_user.id, data):
            return jsonify({
                'success': True,
                'message': 'Настройки уведомлений успешно обновлены'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Не удалось обновить настройки уведомлений'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@notifications_api.route('/notifications/unread-count', methods=['GET'])
@login_required
def get_unread_count():
    """
    Получает количество непрочитанных уведомлений.
    """
    try:
        unread_count = notification_manager.get_unread_count(current_user.id)
        
        return jsonify({
            'success': True,
            'unread_count': unread_count
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@notifications_api.route('/notifications/types', methods=['GET'])
@login_required
def get_notification_types():
    """
    Получает список типов уведомлений.
    """
    try:
        types_data = []
        for notif_type in NotificationType:
            type_data = {
                'name': notif_type.name,
                'value': notif_type.value,
                'description': self._get_notification_type_description(notif_type)
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
    
    def _get_notification_type_description(self, notif_type):
        """Получает описание типа уведомления."""
        descriptions = {
            NotificationType.COMMENT_REPLY: 'Ответ на комментарий',
            NotificationType.COMMENT_MENTION: 'Упоминание в комментарии',
            NotificationType.CONTENT_LIKE: 'Лайк контента',
            NotificationType.CONTENT_SHARE: 'Репост контента',
            NotificationType.NEW_FOLLOWER: 'Новый подписчик',
            NotificationType.SYSTEM_MESSAGE: 'Системное сообщение',
            NotificationType.TEST_RESULT: 'Результаты теста',
            NotificationType.RECOMMENDATION: 'Рекомендации',
            NotificationType.ACHIEVEMENT: 'Достижение',
            NotificationType.REMINDER: 'Напоминание',
            NotificationType.UPDATE: 'Обновление'
        }
        return descriptions.get(notif_type, 'Неизвестный тип')


@notifications_api.route('/notifications/priorities', methods=['GET'])
@login_required
def get_notification_priorities():
    """
    Получает список приоритетов уведомлений.
    """
    try:
        priorities_data = []
        for priority in NotificationPriority:
            priority_data = {
                'name': priority.name,
                'value': priority.value,
                'description': self._get_priority_description(priority)
            }
            priorities_data.append(priority_data)
        
        return jsonify({
            'success': True,
            'priorities': priorities_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500
    
    def _get_priority_description(self, priority):
        """Получает описание приоритета."""
        descriptions = {
            NotificationPriority.LOW: 'Низкий приоритет',
            NotificationPriority.NORMAL: 'Нормальный приоритет',
            NotificationPriority.HIGH: 'Высокий приоритет',
            NotificationPriority.URGENT: 'Срочный приоритет'
        }
        return descriptions.get(priority, 'Неизвестный приоритет')


@notifications_api.route('/notifications/channels', methods=['GET'])
@login_required
def get_notification_channels():
    """
    Получает список каналов доставки уведомлений.
    """
    try:
        channels_data = []
        for channel in NotificationChannel:
            channel_data = {
                'name': channel.name,
                'value': channel.value,
                'description': self._get_channel_description(channel)
            }
            channels_data.append(channel_data)
        
        return jsonify({
            'success': True,
            'channels': channels_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500
    
    def _get_channel_description(self, channel):
        """Получает описание канала."""
        descriptions = {
            NotificationChannel.IN_APP: 'Внутри приложения',
            NotificationChannel.EMAIL: 'Электронная почта',
            NotificationChannel.PUSH: 'Push-уведомления',
            NotificationChannel.SMS: 'SMS сообщения',
            NotificationChannel.TELEGRAM: 'Telegram'
        }
        return descriptions.get(channel, 'Неизвестный канал')


@notifications_api.route('/notifications/statistics', methods=['GET'])
@login_required
def get_notifications_statistics():
    """
    Получает статистику по уведомлениям.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        stats = notification_manager.get_statistics()
        user_stats = {
            'user_unread_count': notification_manager.get_unread_count(current_user.id)
        }
        stats.update(user_stats)
        
        return jsonify({
            'success': True,
            'statistics': stats
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@notifications_api.route('/notifications/cleanup', methods=['POST'])
@login_required
def cleanup_expired_notifications():
    """
    Удаляет истекшие уведомления.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        deleted_count = notification_manager.cleanup_expired_notifications()
        
        return jsonify({
            'success': True,
            'message': f'Удалено {deleted_count} истекших уведомлений',
            'deleted_count': deleted_count
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@notifications_api.route('/notifications/test', methods=['POST'])
@login_required
def send_test_notification():
    """
    Отправляет тестовое уведомление текущему пользователю.
    """
    try:
        data = request.get_json()
        notification_type = NotificationType(data.get('type', 'system_message'))
        
        notification_id = notification_manager.create_notification(
            user_id=current_user.id,
            notification_type=notification_type,
            title='Тестовое уведомление',
            message='Это тестовое уведомление для проверки системы',
            priority=NotificationPriority.NORMAL,
            data={'test': True}
        )
        
        if notification_id:
            notification_manager.send_notification(notification_id)
            
            return jsonify({
                'success': True,
                'message': 'Тестовое уведомление отправлено',
                'notification_id': notification_id
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Не удалось отправить тестовое уведомление'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500