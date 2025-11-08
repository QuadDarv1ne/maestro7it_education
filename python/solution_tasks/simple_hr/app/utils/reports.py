from app.models import Employee, Department, Position, Vacation, Order
from app import db
from datetime import datetime, date, timedelta
from functools import lru_cache
import logging
import time

# Set up logging
logger = logging.getLogger(__name__)

# Try to import pandas
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

@lru_cache(maxsize=32)
def generate_employee_report():
    """Генерация отчета по сотрудникам"""
    try:
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
            try:
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
            except Exception as e:
                logger.error(f"Error processing employee {employee.id}: {str(e)}")
                continue
        
        return report_data
    except Exception as e:
        logger.error(f"Error generating employee report: {str(e)}")
        return []

@lru_cache(maxsize=32)
def generate_department_report():
    """Генерация отчета по подразделениям"""
    try:
        departments = Department.query.all()
        
        report_data = []
        for department in departments:
            try:
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
                    try:
                        vacations = Vacation.query.filter_by(employee_id=employee.id).all()
                        for vacation in vacations:
                            total_vacation_days += (vacation.end_date - vacation.start_date).days + 1
                            vacation_count += 1
                    except Exception as e:
                        logger.error(f"Error processing vacations for employee {employee.id}: {str(e)}")
                        continue
                
                avg_vacation_days = total_vacation_days / employee_count if employee_count > 0 else 0
                
                report_data.append({
                    'id': department.id,
                    'name': department.name,
                    'total_employees': employee_count,
                    'active_employees': active_count,
                    'dismissed_employees': dismissed_count,
                    'avg_vacation_days': round(avg_vacation_days, 2)
                })
            except Exception as e:
                logger.error(f"Error processing department {department.id}: {str(e)}")
                continue
        
        return report_data
    except Exception as e:
        logger.error(f"Error generating department report: {str(e)}")
        return []

@lru_cache(maxsize=32)
def generate_vacation_report(period_days=365):
    """Генерация отчета по отпускам за указанный период"""
    try:
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
            try:
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
            except Exception as e:
                logger.error(f"Error processing vacation {vacation.id}: {str(e)}")
                continue
        
        return report_data
    except Exception as e:
        logger.error(f"Error generating vacation report: {str(e)}")
        return []

@lru_cache(maxsize=32)
def generate_hiring_report(period_months=12):
    """Генерация отчета по найму за указанный период (в месяцах)"""
    try:
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
            try:
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
            except Exception as e:
                logger.error(f"Error processing employee {employee.id} for hiring report: {str(e)}")
                continue
        
        # Преобразуем в список и сортируем по месяцам
        report_data = list(monthly_hiring.values())
        report_data.sort(key=lambda x: x['month'])
        
        return report_data
    except Exception as e:
        logger.error(f"Error generating hiring report: {str(e)}")
        return []

def export_report_to_csv(report_data, filename):
    """Экспорт отчета в CSV файл"""
    if not report_data:
        logger.warning("No data to export to CSV")
        return False
    
    # Try to use pandas if available
    try:
        import pandas as pd
        # Создаем DataFrame из данных
        df = pd.DataFrame(report_data)
        
        # Сохраняем в CSV
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        return True
    except Exception as e:
        logger.warning(f"Pandas export failed, falling back to manual CSV export: {str(e)}")
        # Manual CSV export as fallback
        import csv
        try:
            with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
                if report_data:
                    writer = csv.DictWriter(f, fieldnames=report_data[0].keys())
                    writer.writeheader()
                    writer.writerows(report_data)
            return True
        except Exception as e:
            logger.error(f"Manual CSV export failed: {str(e)}")
            return False

def export_report_to_excel(report_data, filename):
    """Экспорт отчета в Excel файл"""
    if not report_data:
        logger.warning("No data to export to Excel")
        return False
    
    if not PANDAS_AVAILABLE:
        # Excel export not available without pandas
        logger.warning("Pandas not available for Excel export")
        return False
    
    try:
        # Try to use pandas
        import pandas as pd
        # Создаем DataFrame из данных
        df = pd.DataFrame(report_data)
        
        # Сохраняем в Excel
        df.to_excel(filename, index=False)
        return True
    except Exception as e:
        logger.error(f"Excel export failed: {str(e)}")
        return False

@lru_cache(maxsize=32)
def get_employee_statistics():
    """Получение статистики по сотрудникам"""
    try:
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
    except Exception as e:
        logger.error(f"Error getting employee statistics: {str(e)}")
        return {
            'total_employees': 0,
            'active_employees': 0,
            'dismissed_employees': 0,
            'department_stats': [],
            'position_stats': []
        }

@lru_cache(maxsize=32)
def get_vacation_statistics():
    """Получение статистики по отпускам"""
    try:
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
    except Exception as e:
        logger.error(f"Error getting vacation statistics: {str(e)}")
        return {
            'total_vacations': 0,
            'paid_vacations': 0,
            'unpaid_vacations': 0,
            'sick_vacations': 0,
            'avg_duration': 0
        }

@lru_cache(maxsize=32)
def generate_vacation_calendar(year, month):
    """Генерация календаря отпусков на месяц"""
    try:
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
            try:
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
            except Exception as e:
                logger.error(f"Error processing vacation {vacation.id} for calendar: {str(e)}")
                continue
        
        return calendar_data
    except Exception as e:
        logger.error(f"Error generating vacation calendar: {str(e)}")
        return {}

@lru_cache(maxsize=32)
def generate_turnover_report(period_days=365):
    """Генерация отчета по текучести кадров"""
    try:
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
            try:
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
            except Exception as e:
                logger.error(f"Error processing employee {employee.id} for turnover report: {str(e)}")
                continue
        
        # Преобразуем в список и сортируем по месяцам
        report_data = list(monthly_turnover.values())
        report_data.sort(key=lambda x: x['month'])
        
        return report_data
    except Exception as e:
        logger.error(f"Error generating turnover report: {str(e)}")
        return []

@lru_cache(maxsize=32)
def generate_performance_report():
    """Генерация отчета по эффективности"""
    try:
        # Получаем всех сотрудников
        employees = Employee.query.all()
        
        report_data = []
        for employee in employees:
            try:
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
            except Exception as e:
                logger.error(f"Error processing employee {employee.id} for performance report: {str(e)}")
                continue
        
        return report_data
    except Exception as e:
        logger.error(f"Error generating performance report: {str(e)}")
        return []

@lru_cache(maxsize=32)
def generate_salary_report():
    """Генерация отчета по зарплате (заглушка для демонстрации)"""
    try:
        # Получаем всех сотрудников
        employees = Employee.query.all()
        
        report_data = []
        for employee in employees:
            try:
                report_data.append({
                    'id': employee.id,
                    'full_name': employee.full_name,
                    'department': employee.department.name,
                    'position': employee.position.title,
                    'status': employee.status
                })
            except Exception as e:
                logger.error(f"Error processing employee {employee.id} for salary report: {str(e)}")
                continue
        
        return report_data
    except Exception as e:
        logger.error(f"Error generating salary report: {str(e)}")
        return []

@lru_cache(maxsize=32)
def generate_employee_birthday_report():
    """Генерация отчета о днях рождения сотрудников в ближайшие 30 дней"""
    try:
        from datetime import date, timedelta
        
        # Получаем текущую дату
        today = date.today()
        # Определяем дату через 30 дней
        next_month = today + timedelta(days=30)
        
        # Получаем всех активных сотрудников
        employees = Employee.query.filter_by(status='active').all()
        
        report_data = []
        for employee in employees:
            try:
                # Проверяем, есть ли у сотрудника день рождения в ближайшие 30 дней
                # Для простоты предположим, что hire_date содержит дату рождения
                # В реальной системе нужно добавить отдельное поле birth_date
                if hasattr(employee, 'birth_date') and employee.birth_date:
                    # Проверяем, попадает ли день рождения в диапазон
                    birthday_this_year = employee.birth_date.replace(year=today.year)
                    if today <= birthday_this_year <= next_month:
                        report_data.append({
                            'id': employee.id,
                            'full_name': employee.full_name,
                            'department': employee.department.name,
                            'position': employee.position.title,
                            'birth_date': employee.birth_date,
                            'days_until_birthday': (birthday_this_year - today).days
                        })
            except Exception as e:
                logger.error(f"Error processing employee {employee.id} for birthday report: {str(e)}")
                continue
        
        # Сортируем по дате дня рождения
        report_data.sort(key=lambda x: x.get('days_until_birthday', 0))
        
        return report_data
    except Exception as e:
        logger.error(f"Error generating birthday report: {str(e)}")
        return []

@lru_cache(maxsize=32)
def generate_upcoming_vacations_report(days_ahead=30):
    """Генерация отчета о предстоящих отпусках"""
    try:
        from datetime import date, timedelta
        
        # Получаем текущую дату
        today = date.today()
        # Определяем дату через указанное количество дней
        future_date = today + timedelta(days=days_ahead)
        
        # Получаем отпуска, начинающиеся в ближайшие дни
        upcoming_vacations = Vacation.query.filter(
            Vacation.start_date >= today,
            Vacation.start_date <= future_date
        ).order_by(Vacation.start_date).all()
        
        report_data = []
        for vacation in upcoming_vacations:
            try:
                report_data.append({
                    'employee_name': vacation.employee.full_name,
                    'department': vacation.employee.department.name,
                    'position': vacation.employee.position.title,
                    'start_date': vacation.start_date,
                    'end_date': vacation.end_date,
                    'duration': (vacation.end_date - vacation.start_date).days + 1,
                    'type': vacation.type
                })
            except Exception as e:
                logger.error(f"Error processing vacation {vacation.id} for upcoming vacations report: {str(e)}")
                continue
        
        return report_data
    except Exception as e:
        logger.error(f"Error generating upcoming vacations report: {str(e)}")
        return []

# Enhanced caching functions with manual timeout tracking

# Global cache storage with timestamps
_cache_storage = {}

def _get_cache_key(func_name, *args, **kwargs):
    """Generate a cache key for a function call"""
    return f"{func_name}_{hash(str(args) + str(sorted(kwargs.items())))}"

def _is_cache_valid(cache_key, timeout):
    """Check if cache is still valid"""
    if cache_key not in _cache_storage:
        return False
    timestamp, _ = _cache_storage[cache_key]
    return (time.time() - timestamp) < timeout

def _set_cache(cache_key, data, timeout=300):
    """Set cache data with timeout"""
    _cache_storage[cache_key] = (time.time(), data)

def get_cached_employee_data(timeout=600):
    """Получение кэшированных данных о сотрудниках с таймаутом"""
    cache_key = _get_cache_key("get_cached_employee_data")
    if _is_cache_valid(cache_key, timeout):
        return _cache_storage[cache_key][1]
    
    try:
        employees = Employee.query.all()
        departments = Department.query.all()
        positions = Position.query.all()
        
        data = {
            'employees': employees,
            'departments': departments,
            'positions': positions
        }
        _set_cache(cache_key, data, timeout)
        return data
    except Exception as e:
        logger.error(f"Error getting cached employee data: {str(e)}")
        return {
            'employees': [],
            'departments': [],
            'positions': []
        }

def get_cached_vacation_data(timeout=600):
    """Получение кэшированных данных об отпусках с таймаутом"""
    cache_key = _get_cache_key("get_cached_vacation_data")
    if _is_cache_valid(cache_key, timeout):
        return _cache_storage[cache_key][1]
    
    try:
        vacations = Vacation.query.all()
        _set_cache(cache_key, vacations, timeout)
        return vacations
    except Exception as e:
        logger.error(f"Error getting cached vacation data: {str(e)}")
        return []

def get_cached_statistics(timeout=300):
    """Получение кэшированной статистики с таймаутом"""
    cache_key = _get_cache_key("get_cached_statistics")
    if _is_cache_valid(cache_key, timeout):
        return _cache_storage[cache_key][1]
    
    try:
        employee_stats = get_employee_statistics()
        vacation_stats = get_vacation_statistics()
        
        data = {
            'employee_stats': employee_stats,
            'vacation_stats': vacation_stats
        }
        _set_cache(cache_key, data, timeout)
        return data
    except Exception as e:
        logger.error(f"Error getting cached statistics: {str(e)}")
        return {
            'employee_stats': {},
            'vacation_stats': {}
        }

def invalidate_reports_cache():
    """Инвалидация кэша отчетов"""
    global _cache_storage
    _cache_storage.clear()
    # Clear lru_cache as well
    generate_employee_report.cache_clear()
    generate_department_report.cache_clear()
    generate_vacation_report.cache_clear()
    generate_hiring_report.cache_clear()
    get_employee_statistics.cache_clear()
    get_vacation_statistics.cache_clear()
    generate_vacation_calendar.cache_clear()
    generate_turnover_report.cache_clear()
    generate_performance_report.cache_clear()
    generate_salary_report.cache_clear()
    generate_employee_birthday_report.cache_clear()
    generate_upcoming_vacations_report.cache_clear()
    
    logger.info("Reports cache invalidated successfully")
    return True