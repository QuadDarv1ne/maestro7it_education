from app.models import Vacation, Employee, User
from app.utils.notifications import notify_vacation_ending_soon
from app import db
from datetime import datetime, timedelta

def check_upcoming_vacation_endings():
    """Проверка отпусков, которые скоро заканчиваются"""
    # Получаем все текущие отпуска
    today = datetime.utcnow().date()
    # Ищем отпуска, которые заканчиваются через 3 дня или меньше
    upcoming_end_date = today + timedelta(days=3)
    
    vacations = Vacation.query.filter(
        Vacation.end_date >= today,
        Vacation.end_date <= upcoming_end_date
    ).all()
    
    reminder_count = 0
    
    for vacation in vacations:
        # Вычисляем количество оставшихся дней
        days_left = (vacation.end_date - today).days
        
        # Получаем сотрудника
        employee = Employee.query.get(vacation.employee_id)
        if not employee:
            continue
            
        # Получаем всех пользователей с ролью HR для уведомления
        hr_users = User.query.filter_by(role='hr').all()
        
        # Отправляем уведомления всем HR
        for user in hr_users:
            notify_vacation_ending_soon(
                user.id, 
                employee.full_name, 
                vacation.end_date, 
                days_left
            )
            reminder_count += 1
    
    return reminder_count

def check_upcoming_vacation_starts():
    """Проверка отпусков, которые скоро начинаются"""
    # Получаем все отпуска, которые начинаются через 3 дня или меньше
    today = datetime.utcnow().date()
    upcoming_start_date = today + timedelta(days=3)
    
    vacations = Vacation.query.filter(
        Vacation.start_date >= today,
        Vacation.start_date <= upcoming_start_date
    ).all()
    
    reminder_count = 0
    
    for vacation in vacations:
        # Вычисляем количество дней до начала
        days_until_start = (vacation.start_date - today).days
        
        # Получаем сотрудника
        employee = Employee.query.get(vacation.employee_id)
        if not employee:
            continue
            
        # Получаем всех пользователей с ролью HR для уведомления
        hr_users = User.query.filter_by(role='hr').all()
        
        # Отправляем уведомления всем HR
        for user in hr_users:
            # Создаем уведомление о скором начале отпуска
            title = "Скоро начало отпуска"
            message = f"Отпуск сотрудника {employee.full_name} начинается {vacation.start_date.strftime('%d.%m.%Y')} ({days_until_start} дней осталось)."
            from app.utils.notifications import create_notification
            create_notification(user.id, title, message)
            reminder_count += 1
    
    return reminder_count

def cleanup_old_vacations():
    """Очистка старых отпусков (старше 1 года)"""
    one_year_ago = datetime.utcnow().date() - timedelta(days=365)
    
    old_vacations = Vacation.query.filter(Vacation.end_date < one_year_ago).all()
    count = len(old_vacations)
    
    for vacation in old_vacations:
        db.session.delete(vacation)
    
    db.session.commit()
    return count

def get_vacation_statistics():
    """Получение статистики по отпускам"""
    total_vacations = Vacation.query.count()
    
    # Статистика по типам отпусков
    paid_vacations = Vacation.query.filter_by(type='paid').count()
    unpaid_vacations = Vacation.query.filter_by(type='unpaid').count()
    sick_vacations = Vacation.query.filter_by(type='sick').count()
    
    # Статистика по текущим отпускам
    today = datetime.utcnow().date()
    current_vacations = Vacation.query.filter(
        Vacation.start_date <= today,
        Vacation.end_date >= today
    ).count()
    
    return {
        'total': total_vacations,
        'paid': paid_vacations,
        'unpaid': unpaid_vacations,
        'sick': sick_vacations,
        'current': current_vacations
    }

# Функция для запуска всех проверок
def run_daily_checks():
    """Запуск всех ежедневных проверок"""
    results = {}
    
    try:
        results['vacation_endings'] = check_upcoming_vacation_endings()
        results['vacation_starts'] = check_upcoming_vacation_starts()
        results['cleaned_vacations'] = cleanup_old_vacations()
        results['vacation_stats'] = get_vacation_statistics()
    except Exception as e:
        print(f"Ошибка при выполнении ежедневных проверок: {e}")
        results['error'] = str(e)
    
    return results