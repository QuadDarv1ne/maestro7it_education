from app.models import Notification, User
from app import db
from datetime import datetime

def create_notification(user_id, title, message):
    """Создание нового уведомления для пользователя"""
    notification = Notification()
    notification.user_id = user_id
    notification.title = title
    notification.message = message
    notification.is_read = False
    notification.created_at = datetime.utcnow()
    
    db.session.add(notification)
    db.session.commit()
    
    return notification

def get_user_notifications(user_id, limit=10):
    """Получение уведомлений пользователя"""
    return Notification.query.filter_by(user_id=user_id)\
                           .order_by(Notification.created_at.desc())\
                           .limit(limit)\
                           .all()

def mark_notification_as_read(notification_id):
    """Пометить уведомление как прочитанное"""
    notification = Notification.query.get(notification_id)
    if notification:
        notification.is_read = True
        db.session.commit()
        return True
    return False

def mark_all_notifications_as_read(user_id):
    """Пометить все уведомления пользователя как прочитанные"""
    notifications = Notification.query.filter_by(user_id=user_id, is_read=False).all()
    for notification in notifications:
        notification.is_read = True
    
    db.session.commit()
    return len(notifications)

def get_unread_notifications_count(user_id):
    """Получение количества непрочитанных уведомлений пользователя"""
    return Notification.query.filter_by(user_id=user_id, is_read=False).count()

def delete_old_notifications(days=30):
    """Удаление старых уведомлений (по умолчанию старше 30 дней)"""
    from datetime import timedelta
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    old_notifications = Notification.query.filter(Notification.created_at < cutoff_date).all()
    count = len(old_notifications)
    
    for notification in old_notifications:
        db.session.delete(notification)
    
    db.session.commit()
    return count

# Функции для создания специфических уведомлений

def notify_employee_created(user_id, employee_name):
    """Уведомление о создании нового сотрудника"""
    title = "Новый сотрудник добавлен"
    message = f"Сотрудник {employee_name} был успешно добавлен в систему."
    return create_notification(user_id, title, message)

def notify_employee_updated(user_id, employee_name):
    """Уведомление об обновлении данных сотрудника"""
    title = "Данные сотрудника обновлены"
    message = f"Данные сотрудника {employee_name} были успешно обновлены."
    return create_notification(user_id, title, message)

def notify_vacation_created(user_id, employee_name, vacation_type, start_date):
    """Уведомление о создании отпуска"""
    title = "Новый отпуск зарегистрирован"
    message = f"Для сотрудника {employee_name} зарегистрирован {vacation_type} отпуск, начиная с {start_date.strftime('%d.%m.%Y')}."
    return create_notification(user_id, title, message)

def notify_vacation_ending_soon(user_id, employee_name, end_date, days_left):
    """Уведомление о скором окончании отпуска"""
    title = "Отпуск скоро заканчивается"
    message = f"Отпуск сотрудника {employee_name} заканчивается {end_date.strftime('%d.%m.%Y')} ({days_left} дней осталось)."
    return create_notification(user_id, title, message)