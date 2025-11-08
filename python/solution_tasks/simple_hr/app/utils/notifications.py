from app.models import Notification, User
from app import db
from datetime import datetime, timedelta
import logging

# Set up logging
logger = logging.getLogger(__name__)

def create_notification(user_id, title, message, priority='normal', category='info'):
    """Создание нового уведомления для пользователя"""
    try:
        notification = Notification()
        notification.user_id = user_id
        notification.title = title
        notification.message = message
        notification.is_read = False
        notification.created_at = datetime.utcnow()
        notification.priority = priority  # 'low', 'normal', 'high', 'urgent'
        notification.category = category  # 'info', 'success', 'warning', 'error'
        
        db.session.add(notification)
        db.session.commit()
        
        return notification
    except Exception as e:
        logger.error(f"Error creating notification: {str(e)}")
        db.session.rollback()
        return None

def get_user_notifications(user_id, limit=10, include_read=False):
    """Получение уведомлений пользователя"""
    try:
        query = Notification.query.filter_by(user_id=user_id)
        if not include_read:
            query = query.filter_by(is_read=False)
        
        return query.order_by(Notification.created_at.desc()).limit(limit).all()
    except Exception as e:
        logger.error(f"Error getting user notifications: {str(e)}")
        return []

def mark_notification_as_read(notification_id):
    """Пометить уведомление как прочитанное"""
    try:
        notification = Notification.query.get(notification_id)
        if notification:
            notification.is_read = True
            db.session.commit()
            return True
        return False
    except Exception as e:
        logger.error(f"Error marking notification as read: {str(e)}")
        db.session.rollback()
        return False

def mark_all_notifications_as_read(user_id):
    """Пометить все уведомления пользователя как прочитанные"""
    try:
        notifications = Notification.query.filter_by(user_id=user_id, is_read=False).all()
        count = 0
        for notification in notifications:
            notification.is_read = True
            count += 1
        
        db.session.commit()
        return count
    except Exception as e:
        logger.error(f"Error marking all notifications as read: {str(e)}")
        db.session.rollback()
        return 0

def get_unread_notifications_count(user_id):
    """Получение количества непрочитанных уведомлений пользователя"""
    try:
        return Notification.query.filter_by(user_id=user_id, is_read=False).count()
    except Exception as e:
        logger.error(f"Error getting unread notifications count: {str(e)}")
        return 0

def delete_old_notifications(days=30):
    """Удаление старых уведомлений (по умолчанию старше 30 дней)"""
    try:
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        old_notifications = Notification.query.filter(Notification.created_at < cutoff_date).all()
        count = len(old_notifications)
        
        for notification in old_notifications:
            db.session.delete(notification)
        
        db.session.commit()
        return count
    except Exception as e:
        logger.error(f"Error deleting old notifications: {str(e)}")
        db.session.rollback()
        return 0

def get_notifications_by_category(user_id, category, limit=10):
    """Получение уведомлений пользователя по категории"""
    try:
        return Notification.query.filter_by(user_id=user_id, category=category)\
                               .order_by(Notification.created_at.desc())\
                               .limit(limit)\
                               .all()
    except Exception as e:
        logger.error(f"Error getting notifications by category: {str(e)}")
        return []

def get_high_priority_notifications(user_id, limit=5):
    """Получение уведомлений с высоким приоритетом"""
    try:
        return Notification.query.filter_by(user_id=user_id)\
                               .filter(Notification.priority.in_(['high', 'urgent']))\
                               .order_by(Notification.created_at.desc())\
                               .limit(limit)\
                               .all()
    except Exception as e:
        logger.error(f"Error getting high priority notifications: {str(e)}")
        return []

# Функции для создания специфических уведомлений

def notify_employee_created(user_id, employee_name):
    """Уведомление о создании нового сотрудника"""
    title = "Новый сотрудник добавлен"
    message = f"Сотрудник {employee_name} был успешно добавлен в систему."
    return create_notification(user_id, title, message, priority='normal', category='success')

def notify_employee_updated(user_id, employee_name):
    """Уведомление об обновлении данных сотрудника"""
    title = "Данные сотрудника обновлены"
    message = f"Данные сотрудника {employee_name} были успешно обновлены."
    return create_notification(user_id, title, message, priority='normal', category='info')

def notify_vacation_created(user_id, employee_name, vacation_type, start_date):
    """Уведомление о создании отпуска"""
    title = "Новый отпуск зарегистрирован"
    message = f"Для сотрудника {employee_name} зарегистрирован {vacation_type} отпуск, начиная с {start_date.strftime('%d.%m.%Y')}."
    return create_notification(user_id, title, message, priority='normal', category='success')

def notify_vacation_ending_soon(user_id, employee_name, end_date, days_left):
    """Уведомление о скором окончании отпуска"""
    title = "Отпуск скоро заканчивается"
    message = f"Отпуск сотрудника {employee_name} заканчивается {end_date.strftime('%d.%m.%Y')} ({days_left} дней осталось)."
    priority = 'urgent' if days_left <= 3 else 'high' if days_left <= 7 else 'normal'
    return create_notification(user_id, title, message, priority=priority, category='warning')

def notify_employee_birthday(user_id, employee_name, birthday):
    """Уведомление о дне рождения сотрудника"""
    title = "День рождения сотрудника"
    message = f"Сегодня день рождения у сотрудника {employee_name}!"
    return create_notification(user_id, title, message, priority='normal', category='info')

def notify_system_maintenance(user_id, maintenance_time):
    """Уведомление о техническом обслуживании системы"""
    title = "Техническое обслуживание"
    message = f"Система будет недоступна для обслуживания {maintenance_time}."
    return create_notification(user_id, title, message, priority='high', category='warning')

def notify_security_alert(user_id, alert_message):
    """Уведомление о проблемах безопасности"""
    title = "Предупреждение безопасности"
    message = alert_message
    return create_notification(user_id, title, message, priority='urgent', category='error')

def notify_performance_report_available(user_id):
    """Уведомление о доступности отчета по эффективности"""
    title = "Новый отчет по эффективности"
    message = "Доступен новый отчет по эффективности сотрудников."
    return create_notification(user_id, title, message, priority='normal', category='info')

def notify_data_export_completed(user_id, export_type):
    """Уведомление о завершении экспорта данных"""
    title = "Экспорт данных завершен"
    message = f"Экспорт данных типа {export_type} успешно завершен."
    return create_notification(user_id, title, message, priority='normal', category='success')

def notify_system_update(user_id, update_description):
    """Уведомление об обновлении системы"""
    title = "Обновление системы"
    message = f"Система была обновлена: {update_description}"
    return create_notification(user_id, title, message, priority='normal', category='info')

# Bulk notification functions

def notify_all_users(title, message, category='info', priority='normal'):
    """Уведомление всех пользователей"""
    try:
        users = User.query.all()
        notifications = []
        
        for user in users:
            notification = create_notification(user.id, title, message, priority, category)
            if notification:
                notifications.append(notification)
        
        return notifications
    except Exception as e:
        logger.error(f"Error notifying all users: {str(e)}")
        return []

def notify_users_by_role(role, title, message, category='info', priority='normal'):
    """Уведомление пользователей по роли"""
    try:
        users = User.query.filter_by(role=role).all()
        notifications = []
        
        for user in users:
            notification = create_notification(user.id, title, message, priority, category)
            if notification:
                notifications.append(notification)
        
        return notifications
    except Exception as e:
        logger.error(f"Error notifying users by role: {str(e)}")
        return []

def get_notification_statistics(user_id):
    """Получение статистики уведомлений пользователя"""
    try:
        total = Notification.query.filter_by(user_id=user_id).count()
        unread = Notification.query.filter_by(user_id=user_id, is_read=False).count()
        by_category = {}
        categories = ['info', 'success', 'warning', 'error']
        for category in categories:
            by_category[category] = Notification.query.filter_by(user_id=user_id, category=category).count()
        
        return {
            'total': total,
            'unread': unread,
            'by_category': by_category
        }
    except Exception as e:
        logger.error(f"Error getting notification statistics: {str(e)}")
        return {
            'total': 0,
            'unread': 0,
            'by_category': {}
        }