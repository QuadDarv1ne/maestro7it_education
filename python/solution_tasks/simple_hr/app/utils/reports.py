from app.models import Employee, Department, Position, Vacation, Order
from app import db
from datetime import datetime, date, timedelta

# Try to import pandas
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

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
    
    if not PANDAS_AVAILABLE:
        # Manual CSV export
        import csv
        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            if report_data:
                writer = csv.DictWriter(f, fieldnames=report_data[0].keys())
                writer.writeheader()
                writer.writerows(report_data)
        return True
    
    try:
        # Создаем DataFrame из данных
        df = pd.DataFrame(report_data)
        
        # Сохраняем в CSV
        df.to_csv(filename, index=False, encoding='utf-8-sig')
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
        # Создаем DataFrame из данных
        df = pd.DataFrame(report_data)
        
        # Сохраняем в Excel
        df.to_excel(filename, index=False)
        return True
    except:
        return False

def get_employee_statistics():
    """Получение статистики по сотрудникам"""
    total_employees = Employee.query.count()
    active_employees = Employee.query.filter_by(status='active').count()
    dismissed_employees = Employee.query.filter_by(status='dismissed').count()
    
    # Статистика по подразделениям
    departments = Department.query.all()
    dept_stats = []
    for dept in departments:
        emp_count = len(dept.employees)
        active_count = len([emp for emp in dept.employees if emp.status == 'active'])
        dept_stats.append({
            'name': dept.name,
            'total': emp_count,
            'active': active_count,
            'dismissed': emp_count - active_count
        })
    
    # Статистика по должностям
    positions = Position.query.all()
    pos_stats = []
    for pos in positions:
        emp_count = len(pos.employees)
        pos_stats.append({
            'title': pos.title,
            'count': emp_count
        })
    
    return {
        'total_employees': total_employees,
        'active_employees': active_employees,
        'dismissed_employees': dismissed_employees,
        'department_stats': dept_stats,
        'position_stats': pos_stats
    }

def get_vacation_statistics():
    """Получение статистики по отпускам"""
    total_vacations = Vacation.query.count()
    
    # Статистика по типам отпусков
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
        'average_duration': round(avg_duration, 2)
    }

def generate_vacation_calendar(year, month):
    """Генерация календаря отпусков на месяц"""
    from calendar import monthrange
    
    # Получаем первый и последний день месяца
    start_date = date(year, month, 1)
    end_date = date(year, month, monthrange(year, month)[1])
    
    # Получаем отпуска, которые пересекаются с этим месяцем
    vacations = Vacation.query.filter(
        Vacation.start_date <= end_date,
        Vacation.end_date >= start_date
    ).all()
    
    # Создаем календарь
    calendar_data = []
    
    # Для каждого дня месяца
    current_date = start_date
    while current_date <= end_date:
        # Находим отпуска, действующие в этот день
        day_vacations = []
        for vacation in vacations:
            if vacation.start_date <= current_date <= vacation.end_date:
                # Определяем тип отпуска на русском
                vacation_type_names = {
                    'paid': 'Оплачиваемый',
                    'unpaid': 'Неоплачиваемый',
                    'sick': 'Больничный'
                }
                
                day_vacations.append({
                    'employee_name': vacation.employee.full_name,
                    'department': vacation.employee.department.name,
                    'position': vacation.employee.position.title,
                    'type': vacation_type_names.get(vacation.type, vacation.type)
                })
        
        calendar_data.append({
            'date': current_date,
            'vacations': day_vacations
        })
        
        current_date += timedelta(days=1)
    
    return calendar_data

def generate_turnover_report(period_days=365):
    """Генерация отчета по обороту кадров (принято/уволено за период)"""
    # Определяем дату начала периода
    end_date = date.today()
    start_date = end_date - timedelta(days=period_days)
    
    # Получаем сотрудников, принятых за период
    hired_employees = Employee.query.filter(
        Employee.hire_date >= start_date,
        Employee.hire_date <= end_date
    ).all()
    
    # Получаем сотрудников, уволенных за период
    # Для этого ищем приказы об увольнении
    dismissal_orders = Order.query.filter(
        Order.type == 'dismissal',
        Order.date_issued >= start_date,
        Order.date_issued <= end_date
    ).all()
    
    # Получаем информацию об уволенных сотрудниках
    dismissed_employees = []
    for order in dismissal_orders:
        employee = Employee.query.get(order.employee_id)
        if employee:
            dismissed_employees.append({
                'employee_name': employee.full_name,
                'department': employee.department.name if employee.department else '',
                'position': employee.position.title if employee.position else '',
                'dismissal_date': order.date_issued
            })
    
    # Группируем по месяцам
    monthly_hiring = {}
    for employee in hired_employees:
        month_key = employee.hire_date.strftime('%Y-%m')
        if month_key not in monthly_hiring:
            monthly_hiring[month_key] = {
                'month': month_key,
                'hired': 0,
                'dismissed': 0,
                'hired_employees': [],
                'dismissed_employees': []
            }
        monthly_hiring[month_key]['hired'] += 1
        monthly_hiring[month_key]['hired_employees'].append({
            'name': employee.full_name,
            'department': employee.department.name if employee.department else '',
            'position': employee.position.title if employee.position else '',
            'hire_date': employee.hire_date
        })
    
    # Добавляем уволенных сотрудников
    for emp_data in dismissed_employees:
        month_key = emp_data['dismissal_date'].strftime('%Y-%m')
        if month_key not in monthly_hiring:
            monthly_hiring[month_key] = {
                'month': month_key,
                'hired': 0,
                'dismissed': 0,
                'hired_employees': [],
                'dismissed_employees': []
            }
        monthly_hiring[month_key]['dismissed'] += 1
        monthly_hiring[month_key]['dismissed_employees'].append(emp_data)
    
    # Преобразуем в список и сортируем по месяцам
    report_data = list(monthly_hiring.values())
    report_data.sort(key=lambda x: x['month'])
    
    return report_data