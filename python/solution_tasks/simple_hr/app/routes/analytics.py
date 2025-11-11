from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models import Employee, Department, Position, Vacation, Order
from app.utils.analytics import (
    create_employee_distribution_chart, 
    create_employee_status_chart,
    create_hiring_trend_chart,
    create_vacation_analysis_chart,
    create_department_comparison_chart,
    create_turnover_chart,
    create_vacation_duration_chart,
    create_employee_performance_chart,
    create_interactive_dashboard_data,
    create_interactive_charts
)
from app.utils.vacation_reminders import get_vacation_statistics
from app import db
from datetime import datetime, date, timedelta
from functools import lru_cache
import logging

# Set up logging
logger = logging.getLogger(__name__)

bp = Blueprint('analytics', __name__)

# Cache timeout in seconds (5 minutes)
CACHE_TIMEOUT = 300

@lru_cache(maxsize=128)
def get_cached_employees():
    """Cache employees data"""
    return tuple(Employee.query.all())

@lru_cache(maxsize=32)
def get_cached_departments():
    """Cache departments data"""
    return tuple(Department.query.all())

@lru_cache(maxsize=32)
def get_cached_positions():
    """Cache positions data"""
    return tuple(Position.query.all())

@lru_cache(maxsize=64)
def get_cached_vacations():
    """Cache vacations data"""
    return tuple(Vacation.query.all())

@lru_cache(maxsize=32)
def get_cached_orders():
    """Cache orders data"""
    return tuple(Order.query.all())

@lru_cache(maxsize=16)
def get_cached_dashboard_data(employees_hash, departments_hash, positions_hash, vacations_hash):
    """Cache dashboard data with hash-based invalidation"""
    employees = get_cached_employees()
    departments = get_cached_departments()
    positions = get_cached_positions()
    vacations = get_cached_vacations()
    
    return create_interactive_dashboard_data(employees, departments, positions, vacations)

@lru_cache(maxsize=16)
def get_cached_interactive_charts(dashboard_data_hash, departments_hash, employees_hash, vacations_hash):
    """Cache interactive charts with hash-based invalidation"""
    employees = get_cached_employees()
    departments = get_cached_departments()
    positions = get_cached_positions()
    vacations = get_cached_vacations()
    
    # Recreate dashboard data for charts
    interactive_data = get_cached_dashboard_data(
        hash(employees), hash(departments), hash(positions), hash(vacations)
    )
    
    return create_interactive_charts(interactive_data, departments, employees, vacations)

def invalidate_cache():
    """Invalidate all cached data"""
    get_cached_employees.cache_clear()
    get_cached_departments.cache_clear()
    get_cached_positions.cache_clear()
    get_cached_vacations.cache_clear()
    get_cached_orders.cache_clear()
    get_cached_dashboard_data.cache_clear()
    get_cached_interactive_charts.cache_clear()

@bp.route('/')
@login_required
def dashboard():
    """Главная страница аналитики"""
    try:
        # Get cached data
        employees = get_cached_employees()
        departments = get_cached_departments()
        positions = get_cached_positions()
        vacations = get_cached_vacations()
        
        # Create hash for cache invalidation
        employees_hash = hash(employees)
        departments_hash = hash(departments)
        positions_hash = hash(positions)
        vacations_hash = hash(vacations)
        
        # Get cached dashboard data
        interactive_data = get_cached_dashboard_data(
            employees_hash, departments_hash, positions_hash, vacations_hash
        )
        
        # Get cached interactive charts
        interactive_charts = get_cached_interactive_charts(
            hash(str(interactive_data)), departments_hash, employees_hash, vacations_hash
        )
        
        # Calculate additional metrics
        from datetime import date, timedelta
        
        # Employees on vacation today
        today = date.today()
        employees_on_vacation = Vacation.query.filter(
            Vacation.start_date <= today,
            Vacation.end_date >= today
        ).count()
        
        # Employees starting vacation today
        employees_starting_vacation = Vacation.query.filter(
            Vacation.start_date == today
        ).count()
        
        # Employees ending vacation today
        employees_ending_vacation = Vacation.query.filter(
            Vacation.end_date == today
        ).count()
        
        # Recent hires (last 30 days)
        thirty_days_ago = today - timedelta(days=30)
        recent_hires = Employee.query.filter(
            Employee.hire_date >= thirty_days_ago
        ).count()
        
        # Add to interactive_data
        interactive_data_dict = dict(interactive_data) if hasattr(interactive_data, '_asdict') else interactive_data
        interactive_data_dict['employees_on_vacation'] = employees_on_vacation
        interactive_data_dict['employees_starting_vacation'] = employees_starting_vacation
        interactive_data_dict['employees_ending_vacation'] = employees_ending_vacation
        interactive_data_dict['recent_hires'] = recent_hires
        
        return render_template('analytics/dashboard.html', 
                             interactive_data=interactive_data_dict,
                             interactive_charts=interactive_charts)
    except Exception as e:
        logger.error(f"Error in analytics dashboard: {str(e)}")
        flash('Ошибка при загрузке аналитики', 'error')
        return redirect(url_for('main.index'))

@bp.route('/employee_statistics')
@login_required
def employee_statistics():
    """Статистика по сотрудникам"""
    try:
        # Get cached data
        employees = get_cached_employees()
        departments = get_cached_departments()
        positions = get_cached_positions()
        
        # Calculate statistics from cached data
        total_employees = len(employees)
        active_employees = len([e for e in employees if e.status == 'active'])
        dismissed_employees = len([e for e in employees if e.status == 'dismissed'])
        
        # Статистика по подразделениям
        department_stats = []
        for dept in departments:
            dept_count = len([e for e in employees if e.department_id == dept.id])
            department_stats.append({
                'name': dept.name,
                'count': dept_count
            })
        
        # Статистика по должностям
        position_stats = []
        for pos in positions:
            pos_count = len([e for e in employees if e.position_id == pos.id])
            position_stats.append({
                'title': pos.title,
                'count': pos_count
            })
        
        # Создаем графики
        distribution_chart = create_employee_distribution_chart(tuple(tuple(d.items()) for d in department_stats))
        status_chart = create_employee_status_chart(active_employees, dismissed_employees)
        department_comparison_chart = create_department_comparison_chart(departments, employees)
        turnover_chart = create_turnover_chart(employees)
        
        return render_template('analytics/employee_statistics.html',
                             total_employees=total_employees,
                             active_employees=active_employees,
                             dismissed_employees=dismissed_employees,
                             department_stats=department_stats,
                             position_stats=position_stats,
                             distribution_chart=distribution_chart,
                             status_chart=status_chart,
                             department_comparison_chart=department_comparison_chart,
                             turnover_chart=turnover_chart)
    except Exception as e:
        logger.error(f"Error in employee statistics: {str(e)}")
        flash('Ошибка при загрузке статистики по сотрудникам', 'error')
        return redirect(url_for('analytics.dashboard'))

@bp.route('/hiring_trends')
@login_required
def hiring_trends():
    """Анализ тенденций найма"""
    try:
        # Get cached employees
        employees = get_cached_employees()
        
        # Создаем график тенденций найма
        hiring_trend_chart = create_hiring_trend_chart(employees)
        
        # Подготавливаем данные для таблицы
        hiring_data = []
        for emp in employees:
            hiring_data.append({
                'full_name': emp.full_name,
                'department': emp.department.name if emp.department else 'Не указано',
                'position': emp.position.title if emp.position else 'Не указана',
                'hire_date': emp.hire_date
            })
        
        # Сортируем по дате приема на работу
        hiring_data.sort(key=lambda x: x['hire_date'], reverse=True)
        
        return render_template('analytics/hiring_trends.html',
                             hiring_trend_chart=hiring_trend_chart,
                             hiring_data=hiring_data)
    except Exception as e:
        logger.error(f"Error in hiring trends: {str(e)}")
        flash('Ошибка при загрузке тенденций найма', 'error')
        return redirect(url_for('analytics.dashboard'))

@bp.route('/vacation_analysis')
@login_required
def vacation_analysis():
    """Анализ отпусков"""
    try:
        # Get cached data
        vacations = get_cached_vacations()
        employees = get_cached_employees()
        
        # Create employee lookup dictionary for performance
        employee_dict = {emp.id: emp for emp in employees}
        
        # Создаем графики анализа отпусков
        vacation_chart = create_vacation_analysis_chart(vacations)
        vacation_duration_chart = create_vacation_duration_chart(vacations)
        employee_performance_chart = create_employee_performance_chart(employees, vacations)
        
        # Подготавливаем данные для таблицы
        vacation_data = []
        for vacation in vacations:
            # Get employee from cache
            employee = employee_dict.get(vacation.employee_id)
            if not employee:
                continue
                
            # Определяем тип отпуска
            vacation_type_names = {
                'paid': 'Оплачиваемый',
                'unpaid': 'Неоплачиваемый',
                'sick': 'Больничный'
            }
            vacation_type = vacation_type_names.get(vacation.type, 'Другое')
            
            vacation_data.append({
                'employee_name': employee.full_name,
                'department': employee.department.name if employee.department else 'Не указано',
                'start_date': vacation.start_date,
                'end_date': vacation.end_date,
                'duration': (vacation.end_date - vacation.start_date).days + 1,
                'type': vacation_type
            })
        
        # Сортируем по дате начала отпуска
        vacation_data.sort(key=lambda x: x['start_date'], reverse=True)
        
        return render_template('analytics/vacation_analysis.html',
                             vacation_chart=vacation_chart,
                             vacation_duration_chart=vacation_duration_chart,
                             employee_performance_chart=employee_performance_chart,
                             vacation_data=vacation_data)
    except Exception as e:
        logger.error(f"Error in vacation analysis: {str(e)}")
        flash('Ошибка при загрузке анализа отпусков', 'error')
        return redirect(url_for('analytics.dashboard'))

@bp.route('/export_report')
@login_required
def export_report():
    """Экспорт аналитических отчетов"""
    try:
        report_type = request.args.get('type', 'summary')
        
        # Generate report data based on type
        if report_type == 'summary':
            # Get all employees for summary report
            employees = Employee.query.all()
            
            # Create CSV data
            import io
            import csv
            output = io.StringIO()
            writer = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            
            # Write header
            writer.writerow(['ФИО', 'Email', 'Табельный номер', 'Подразделение', 'Должность', 'Дата приема', 'Статус'])
            
            # Write data rows
            for emp in employees:
                hire_date_str = emp.hire_date.strftime("%d.%m.%Y") if emp.hire_date else ''
                writer.writerow([
                    emp.full_name,
                    emp.email,
                    emp.employee_id,
                    emp.department.name if emp.department else '',
                    emp.position.title if emp.position else '',
                    hire_date_str,
                    emp.status
                ])
            
            csv_data = output.getvalue()
            
            # Return CSV response
            from flask import Response
            return Response(
                csv_data,
                mimetype='text/csv',
                headers={'Content-Disposition': 'attachment; filename=employee_summary_report.csv'}
            )
        else:
            flash('Неверный тип отчета', 'error')
            return redirect(url_for('analytics.dashboard'))
    except Exception as e:
        logger.error(f"Error in export report: {str(e)}")
        flash('Ошибка при экспорте отчета', 'error')
        return redirect(url_for('analytics.dashboard'))

# Add cache invalidation when data changes
def on_model_change():
    """Call this function when any model data changes to invalidate cache"""
    invalidate_cache()