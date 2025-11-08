from app.models import Employee, Department, Position, Vacation, Order
from app import db
from datetime import datetime, date, timedelta
from functools import lru_cache

# Try to import pandas
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

@lru_cache(maxsize=32)
def generate_employee_report():
    """Генерация отчета по сотрудникам"""
    # Получаем всех сотрудников с их подразделениями и должностями
    employees = db.session.query(
        Employee, Department, Position
    ).join(
        Department, Employee.department_id == Department.id
    ).join(
        Position, Employee.position_id == Position.id
    ).all()
    
    report_data = []
    for employee, department, position in employees:
        # Получаем информацию об отпусках
        vacations = Vacation.query.filter_by(employee_id=employee.id).all()
        total_vacation_days = sum([(v.end_date - v.start_date).days + 1 for v in vacations])
        
        # Получаем последний приказ
        last_order = Order.query.filter_by(employee_id=employee.id).order_by(Order.date_issued.desc()).first()
        
        report_data.append({
            'id': employee.id,
            'full_name': employee.full_name,
            'email': employee.email,
            'employee_id': employee.employee_id,
            'hire_date': employee.hire_date,
            'department': department.name,
            'position': position.title,
            'status': employee.status,
            'total_vacation_days': total_vacation_days,
            'last_order_type': last_order.type if last_order else None,
            'last_order_date': last_order.date_issued if last_order else None
        })
    
    return report_data

@lru_cache(maxsize=32)
def generate_department_report():
    """Генерация отчета по подразделениям"""
    departments = Department.query.all()
    
    report_data = []
    for department in departments:
        # Подсчитываем количество сотрудников
        employee_count = len(department.employees)
        
        # Подсчитываем количество активных сотрудников
        active_count = len([emp for emp in department.employees if emp.status == 'active'])
        
        # Подсчитываем количество уволенных сотрудников
        dismissed_count = employee_count - active_count
        
        # Среднее количество дней отпуска на сотрудника
        total_vacation_days = 0
        vacation_count = 0
        for employee in department.employees:
            vacations = Vacation.query.filter_by(employee_id=employee.id).all()
            for vacation in vacations:
                total_vacation_days += (vacation.end_date - vacation.start_date).days + 1
                vacation_count += 1
        
        avg_vacation_days = total_vacation_days / employee_count if employee_count > 0 else 0
        
        report_data.append({
            'id': department.id,
            'name': department.name,
            'total_employees': employee_count,
            'active_employees': active_count,
            'dismissed_employees': dismissed_count,
            'avg_vacation_days': round(avg_vacation_days, 2)
        })
    
    return report_data

@lru_cache(maxsize=32)
def generate_vacation_report(period_days=365):
    """Генерация отчета по отпускам за указанный период"""
    # Определяем дату начала периода
    end_date = date.today()
    start_date = end_date - timedelta(days=period_days)
    
    # Получаем отпуска за период
    vacations = Vacation.query.filter(
        Vacation.start_date >= start_date,
        Vacation.end_date <= end_date
    ).all()
    
    report_data = []
    for vacation in vacations:
        # Определяем тип отпуска на русском
        vacation_type_names = {
            'paid': 'Оплачиваемый',
            'unpaid': 'Неоплачиваемый',
            'sick': 'Больничный'
        }
        
        # Длительность отпуска в днях
        duration = (vacation.end_date - vacation.start_date).days + 1
        
        report_data.append({
            'employee_name': vacation.employee.full_name,
            'department': vacation.employee.department.name,
            'position': vacation.employee.position.title,
            'start_date': vacation.start_date,
            'end_date': vacation.end_date,
            'duration': duration,
            'type': vacation_type_names.get(vacation.type, vacation.type)
        })
    
    return report_data

@lru_cache(maxsize=32)
def generate_hiring_report(period_months=12):
    """Генерация отчета по найму за указанный период (в месяцах)"""
    # Определяем дату начала периода
    end_date = date.today()
    start_date = end_date - timedelta(days=period_months * 30)  # Приблизительно
    
    # Получаем сотрудников, принятых за период
    employees = Employee.query.filter(
        Employee.hire_date >= start_date,
        Employee.hire_date <= end_date
    ).all()
    
    # Группируем по месяцам
    monthly_hiring = {}
    for employee in employees:
        month_key = employee.hire_date.strftime('%Y-%m')
        if month_key not in monthly_hiring:
            monthly_hiring[month_key] = {
                'month': month_key,
                'count': 0,
                'employees': []
            }
        monthly_hiring[month_key]['count'] += 1
        monthly_hiring[month_key]['employees'].append({
            'name': employee.full_name,
            'department': employee.department.name,
            'position': employee.position.title,
            'hire_date': employee.hire_date
        })
    
    # Преобразуем в список и сортируем по месяцам
    report_data = list(monthly_hiring.values())
    report_data.sort(key=lambda x: x['month'])
    
    return report_data

def export_report_to_csv(report_data, filename):
    """Экспорт отчета в CSV файл"""
    if not report_data:
        return False
    
    # Try to use pandas if available
    try:
        import pandas as pd
        # Создаем DataFrame из данных
        df = pd.DataFrame(report_data)
        
        # Сохраняем в CSV
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        return True
    except:
        # Manual CSV export as fallback
        import csv
        try:
            with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
                if report_data:
                    writer = csv.DictWriter(f, fieldnames=report_data[0].keys())
                    writer.writeheader()
                    writer.writerows(report_data)
            return True
        except:
            return False

def export_report_to_excel(report_data, filename):
    """Экспорт отчета в Excel файл"""
    if not report_data:
        return False
    
    if not PANDAS_AVAILABLE:
        # Excel export not available without pandas
        return False
    
    try:
        # Try to use pandas
        import pandas as pd
        # Создаем DataFrame из данных
        df = pd.DataFrame(report_data)
        
        # Сохраняем в Excel
        df.to_excel(filename, index=False)
        return True
    except:
        return False

@lru_cache(maxsize=32)
def get_employee_statistics():
    """Получение статистики по сотрудникам"""
    total_employees = Employee.query.count()
    active_employees = Employee.query.filter_by(status='active').count()
    dismissed_employees = Employee.query.filter_by(status='dismissed').count()
    
    # Статистика по подразделениям
    department_stats = []
    departments = Department.query.all()
    for dept in departments:
        dept_count = len(dept.employees)
        department_stats.append({
            'name': dept.name,
            'count': dept_count
        })
    
    # Статистика по должностям
    position_stats = []
    positions = Position.query.all()
    for pos in positions:
        pos_count = len(pos.employees)
        position_stats.append({
            'title': pos.title,
            'count': pos_count
        })
    
    return {
        'total_employees': total_employees,
        'active_employees': active_employees,
        'dismissed_employees': dismissed_employees,
        'department_stats': department_stats,
        'position_stats': position_stats
    }

@lru_cache(maxsize=32)
def get_vacation_statistics():
    """Получение статистики по отпускам"""
    # Общее количество отпусков
    total_vacations = Vacation.query.count()
    
    # Количество отпусков по типам
    paid_vacations = Vacation.query.filter_by(type='paid').count()
    unpaid_vacations = Vacation.query.filter_by(type='unpaid').count()
    sick_vacations = Vacation.query.filter_by(type='sick').count()
    
    # Средняя продолжительность отпуска
    vacations = Vacation.query.all()
    if vacations:
        total_days = sum([(v.end_date - v.start_date).days + 1 for v in vacations])
        avg_duration = total_days / len(vacations)
    else:
        avg_duration = 0
    
    return {
        'total_vacations': total_vacations,
        'paid_vacations': paid_vacations,
        'unpaid_vacations': unpaid_vacations,
        'sick_vacations': sick_vacations,
        'avg_duration': round(avg_duration, 2)
    }

@lru_cache(maxsize=32)
def generate_vacation_calendar(year, month):
    """Генерация календаря отпусков на месяц"""
    from calendar import monthrange
    from datetime import date
    
    # Получаем первый и последний день месяца
    first_day = date(year, month, 1)
    last_day = date(year, month, monthrange(year, month)[1])
    
    # Получаем отпуска, которые пересекаются с этим месяцем
    vacations = Vacation.query.filter(
        Vacation.start_date <= last_day,
        Vacation.end_date >= first_day
    ).all()
    
    # Создаем календарь
    calendar_data = {}
    
    # Заполняем календарь отпусками
    for vacation in vacations:
        # Определяем даты отпуска в пределах месяца
        start = max(vacation.start_date, first_day)
        end = min(vacation.end_date, last_day)
        
        # Добавляем отпуск в календарь для каждой даты
        current_date = start
        while current_date <= end:
            if current_date not in calendar_data:
                calendar_data[current_date] = []
            calendar_data[current_date].append(vacation)
            current_date += timedelta(days=1)
    
    return calendar_data

@lru_cache(maxsize=32)
def generate_turnover_report(period_days=365):
    """Генерация отчета по текучести кадров"""
    # Определяем дату начала периода
    end_date = date.today()
    start_date = end_date - timedelta(days=period_days)
    
    # Получаем уволенных сотрудников за период
    dismissed_employees = Employee.query.filter(
        Employee.status == 'dismissed',
        Employee.hire_date >= start_date,
        Employee.hire_date <= end_date
    ).all()
    
    # Группируем по месяцам
    monthly_turnover = {}
    for employee in dismissed_employees:
        month_key = employee.hire_date.strftime('%Y-%m')
        if month_key not in monthly_turnover:
            monthly_turnover[month_key] = {
                'month': month_key,
                'count': 0,
                'employees': []
            }
        monthly_turnover[month_key]['count'] += 1
        monthly_turnover[month_key]['employees'].append({
            'name': employee.full_name,
            'department': employee.department.name,
            'position': employee.position.title,
            'hire_date': employee.hire_date
        })
    
    # Преобразуем в список и сортируем по месяцам
    report_data = list(monthly_turnover.values())
    report_data.sort(key=lambda x: x['month'])
    
    return report_data

@lru_cache(maxsize=32)
def generate_performance_report():
    """Генерация отчета по эффективности"""
    # Получаем всех сотрудников
    employees = Employee.query.all()
    
    report_data = []
    for employee in employees:
        # Получаем информацию об отпусках
        vacations = Vacation.query.filter_by(employee_id=employee.id).all()
        total_vacation_days = sum([(v.end_date - v.start_date).days + 1 for v in vacations])
        
        # Получаем последний приказ
        last_order = Order.query.filter_by(employee_id=employee.id).order_by(Order.date_issued.desc()).first()
        
        report_data.append({
            'id': employee.id,
            'full_name': employee.full_name,
            'department': employee.department.name,
            'position': employee.position.title,
            'hire_date': employee.hire_date,
            'status': employee.status,
            'total_vacation_days': total_vacation_days,
            'last_order_type': last_order.type if last_order else None,
            'last_order_date': last_order.date_issued if last_order else None
        })
    
    return report_data

@lru_cache(maxsize=32)
def generate_salary_report():
    """Генерация отчета по зарплате (заглушка для демонстрации)"""
    # Получаем всех сотрудников
    employees = Employee.query.all()
    
    report_data = []
    for employee in employees:
        report_data.append({
            'id': employee.id,
            'full_name': employee.full_name,
            'department': employee.department.name,
            'position': employee.position.title,
            'status': employee.status
        })
    
    return report_data