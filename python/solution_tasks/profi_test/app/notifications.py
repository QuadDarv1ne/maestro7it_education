# -*- coding: utf-8 -*-
"""
Blueprint для пользовательских уведомлений
"""
from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from app.advanced_notifications import notification_manager, NotificationStatus

notifications = Blueprint('notifications', __name__)

@notifications.route('/user-notifications')
@login_required
def user_notifications():
    """Получает уведомления пользователя"""
    try:
        user_notifications = notification_manager.get_user_notifications(
            user_id=current_user.id,
            status=NotificationStatus.UNREAD,
            limit=10
        )
        
        notifications_data = []
        for notification in user_notifications:
            notification_data = {
                'id': notification.id,
                'title': notification.title,
                'message': notification.message,
                'type': notification.notification_type.value,
                'priority': notification.priority.value,
                'created_at': notification.created_at.isoformat(),
                'is_read': notification.status == NotificationStatus.READ
            }
            notifications_data.append(notification_data)
        
        return jsonify({
            'success': True,
            'notifications': notifications_data,
            'count': len(notifications_data)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@notifications.route('/unread-count')
def unread_count():
    """Получает количество непрочитанных уведомлений"""
    try:
        if current_user.is_authenticated:
            user_notifications = notification_manager.get_user_notifications(
                user_id=current_user.id,
                status=NotificationStatus.UNREAD
            )
            count = len(user_notifications)
        else:
            count = 0
            
        return jsonify({
            'success': True,
            'count': count
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500