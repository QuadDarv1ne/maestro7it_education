from app.models import Vacation, User
from app.utils.notifications import notify_vacation_ending_soon
from app import db
from datetime import datetime, timedelta

def check_upcoming_vacation_endings():
    """Проверка отпусков, которые скоро заканчиваются, и отправка уведомлений"""
    # Получаем все активные отпуска
    today = datetime.utcnow().date()
    # Проверяем отпуска, которые заканчиваются через 3 дня или меньше
    upcoming_date = today + timedelta(days=3)
    
    vacations = Vacation.query.filter(
        Vacation.end_date >= today,
        Vacation.end_date <= upcoming_date
    ).all()
    
    notification_count = 0
    
    for vacation in vacations:
        # Рассчитываем количество оставшихся дней
        days_left = (vacation.end_date - today).days
        
        # Получаем всех пользователей с ролью HR и admin для уведомления
        users = User.query.filter(User.role.in_(['hr', 'admin'])).all()
        
        for user in users:
            # Отправляем уведомление
            notify_vacation_ending_soon(
                user.id, 
                vacation.employee.full_name, 
                vacation.end_date, 
                days_left
            )
            notification_count += 1
    
    return notification_count

def get_vacation_statistics():
    """Получение статистики по отпускам"""
    today = datetime.utcnow().date()
    
    # Все активные отпуска
    active_vacations = Vacation.query.filter(
        Vacation.start_date <= today,
        Vacation.end_date >= today
    ).count()
    
    # Отпуска, заканчивающиеся сегодня
    ending_today = Vacation.query.filter(
        Vacation.end_date == today
    ).count()
    
    # Отпуска, начинающиеся сегодня
    starting_today = Vacation.query.filter(
        Vacation.start_date == today
    ).count()
    
    return {
        'active_vacations': active_vacations,
        'ending_today': ending_today,
        'starting_today': starting_today
    }

def get_upcoming_vacations(days=7):
    """Получение списка отпусков, начинающихся в ближайшие N дней"""
    today = datetime.utcnow().date()
    future_date = today + timedelta(days=days)
    
    upcoming_vacations = Vacation.query.filter(
        Vacation.start_date >= today,
        Vacation.start_date <= future_date
    ).order_by(Vacation.start_date).all()
    
    return upcoming_vacations

def get_ending_vacations(days=7):
    """Получение списка отпусков, заканчивающихся в ближайшие N дней"""
    today = datetime.utcnow().date()
    future_date = today + timedelta(days=days)
    
    ending_vacations = Vacation.query.filter(
        Vacation.end_date >= today,
        Vacation.end_date <= future_date
    ).order_by(Vacation.end_date).all()
    
    return ending_vacations