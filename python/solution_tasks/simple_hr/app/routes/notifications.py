from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.models import Notification
from app.utils.notifications import (
    get_user_notifications, 
    mark_notification_as_read, 
    mark_all_notifications_as_read,
    get_unread_notifications_count
)
from app import db

bp = Blueprint('notifications', __name__)

@bp.route('/')
@login_required
def list_notifications():
    """Список уведомлений пользователя"""
    page = request.args.get('page', 1, type=int)
    notifications = Notification.query.filter_by(user_id=current_user.id)\
                                   .order_by(Notification.created_at.desc())\
                                   .paginate(page=page, per_page=10, error_out=False)
    
    return render_template('notifications/list.html', notifications=notifications)

@bp.route('/unread_count')
@login_required
def unread_count():
    """Получение количества непрочитанных уведомлений (AJAX)"""
    count = get_unread_notifications_count(current_user.id)
    return jsonify({'count': count})

@bp.route('/mark_as_read/<int:notification_id>', methods=['POST'])
@login_required
def mark_as_read(notification_id):
    """Пометить уведомление как прочитанное"""
    notification = Notification.query.get_or_404(notification_id)
    
    # Проверяем, что уведомление принадлежит текущему пользователю
    if notification.user_id != current_user.id:
        flash('У вас нет прав для выполнения этого действия')
        return redirect(url_for('notifications.list_notifications'))
    
    if mark_notification_as_read(notification_id):
        flash('Уведомление помечено как прочитанное')
    else:
        flash('Ошибка при пометке уведомления')
    
    return redirect(url_for('notifications.list_notifications'))

@bp.route('/mark_all_as_read', methods=['POST'])
@login_required
def mark_all_as_read():
    """Пометить все уведомления как прочитанные"""
    count = mark_all_notifications_as_read(current_user.id)
    flash(f'{count} уведомлений помечены как прочитанные')
    return redirect(url_for('notifications.list_notifications'))

@bp.route('/delete/<int:notification_id>', methods=['POST'])
@login_required
def delete_notification(notification_id):
    """Удалить уведомление"""
    notification = Notification.query.get_or_404(notification_id)
    
    # Проверяем, что уведомление принадлежит текущему пользователю
    if notification.user_id != current_user.id:
        flash('У вас нет прав для выполнения этого действия')
        return redirect(url_for('notifications.list_notifications'))
    
    try:
        db.session.delete(notification)
        db.session.commit()
        flash('Уведомление удалено')
    except Exception as e:
        db.session.rollback()
        flash('Ошибка при удалении уведомления')
    
    return redirect(url_for('notifications.list_notifications'))

@bp.route('/delete_all', methods=['POST'])
@login_required
def delete_all_notifications():
    """Удалить все уведомления пользователя"""
    notifications = Notification.query.filter_by(user_id=current_user.id).all()
    count = len(notifications)
    
    try:
        for notification in notifications:
            db.session.delete(notification)
        db.session.commit()
        flash(f'{count} уведомлений удалены')
    except Exception as e:
        db.session.rollback()
        flash('Ошибка при удалении уведомлений')
    
    return redirect(url_for('notifications.list_notifications'))