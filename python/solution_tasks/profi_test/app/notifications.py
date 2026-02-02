from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Notification
from datetime import datetime

notifications = Blueprint('notifications', __name__)

@notifications.route('/notifications')
@login_required
def user_notifications():
    """View user notifications"""
    page = request.args.get('page', 1, type=int)
    user_notifications = Notification.query.filter_by(
        user_id=current_user.id
    ).order_by(Notification.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    # Mark as read
    for notification in user_notifications.items:
        if not notification.is_read:
            notification.is_read = True
            notification.read_at = datetime.utcnow()
    
    db.session.commit()
    
    return render_template('notifications/list.html', notifications=user_notifications)

@notifications.route('/notifications/unread_count')
@login_required
def unread_count():
    """Get count of unread notifications"""
    count = Notification.query.filter_by(
        user_id=current_user.id, 
        is_read=False
    ).count()
    
    return jsonify({'count': count})

@notifications.route('/notifications/mark_all_read', methods=['POST'])
@login_required
def mark_all_read():
    """Mark all notifications as read"""
    notifications = Notification.query.filter_by(
        user_id=current_user.id, 
        is_read=False
    ).all()
    
    for notification in notifications:
        notification.is_read = True
        notification.read_at = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Все уведомления отмечены как прочитанные'})

@notifications.route('/notifications/<int:notification_id>/delete', methods=['POST'])
@login_required
def delete_notification(notification_id):
    """Delete notification"""
    notification = Notification.query.get_or_404(notification_id)
    
    # Check permission
    if notification.user_id != current_user.id and not current_user.is_admin:
        return jsonify({'error': 'Нет доступа'}), 403
    
    db.session.delete(notification)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Уведомление удалено'})

def create_notification(user_id, title, message, notification_type='info'):
    """Create a new notification"""
    notification = Notification(
        user_id=user_id,
        title=title,
        message=message,
        type=notification_type
    )
    
    db.session.add(notification)
    db.session.commit()
    
    return notification

def create_system_notification(title, message, notification_type='info'):
    """Create system notification for all users"""
    from app.models import User
    
    users = User.query.all()
    
    for user in users:
        create_notification(user.id, title, message, notification_type)
    
    return True

@notifications.route('/notifications/vacancy_alerts')
@login_required
def vacancy_alerts():
    """Get user's vacancy alerts settings"""
    from app.models import UserPreference
    
    # Get or create user preferences
    prefs = UserPreference.query.filter_by(user_id=current_user.id).first()
    if not prefs:
        prefs = UserPreference(user_id=current_user.id)
        db.session.add(prefs)
        db.session.commit()
    
    return jsonify({
        'success': True,
        'alerts_enabled': prefs.vacancy_alerts_enabled,
        'preferred_professions': prefs.preferred_professions
    })

@notifications.route('/notifications/vacancy_alerts/update', methods=['POST'])
@login_required
def update_vacancy_alerts():
    """Update user's vacancy alerts settings"""
    from app.models import UserPreference
    import json
    
    data = request.get_json()
    enabled = data.get('enabled', False)
    professions = data.get('professions', [])
    
    # Get or create user preferences
    prefs = UserPreference.query.filter_by(user_id=current_user.id).first()
    if not prefs:
        prefs = UserPreference(user_id=current_user.id)
        db.session.add(prefs)
    
    prefs.vacancy_alerts_enabled = enabled
    prefs.preferred_professions = json.dumps(professions)
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Настройки уведомлений обновлены'
    })