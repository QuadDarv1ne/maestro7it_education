from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models import Employee, Department, Position, Vacation, Order
from app.utils.analytics import (
    create_employee_distribution_chart, 
    create_employee_status_chart,
    create_hiring_trend_chart,
    create_vacation_analysis_chart,
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

@bp.route('/')
@login_required
def dashboard():
    """Главная страница аналитики"""
    try:
        # Получаем все данные
        employees = Employee.query.all()
        departments = Department.query.all()
        positions = Position.query.all()
        vacations = Vacation.query.all()
        orders = Order.query.all()
        
        # Создаем интерактивные данные для дашборда
        interactive_data = create_interactive_dashboard_data(employees, departments, positions, vacations)
        
        # Создаем интерактивные графики с дополнительными данными
        interactive_charts = create_interactive_charts(interactive_data, departments, employees, vacations)
        
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
        interactive_data['employees_on_vacation'] = employees_on_vacation
        interactive_data['employees_starting_vacation'] = employees_starting_vacation
        interactive_data['employees_ending_vacation'] = employees_ending_vacation
        interactive_data['recent_hires'] = recent_hires
        
        return render_template('analytics/dashboard.html', 
                             interactive_data=interactive_data,
                             interactive_charts=interactive_charts)
    except Exception as e:
        logger.error(f"Error in analytics dashboard: {str(e)}")
        flash('Ошибка при загрузке аналитики')
        return redirect(url_for('main.index'))

@bp.route('/employee_statistics')
@login_required
def employee_statistics():
    """Статистика по сотрудникам"""
    try:
        # Получаем статистику
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
        
        # Создаем графики
        distribution_chart = create_employee_distribution_chart(tuple(tuple(d.items()) for d in department_stats))
        status_chart = create_employee_status_chart(active_employees, dismissed_employees)
        
        return render_template('analytics/employee_statistics.html',
                             total_employees=total_employees,
                             active_employees=active_employees,
                             dismissed_employees=dismissed_employees,
                             department_stats=department_stats,
                             position_stats=position_stats,
                             distribution_chart=distribution_chart,
                             status_chart=status_chart)
    except Exception as e:
        logger.error(f"Error in employee statistics: {str(e)}")
        flash('Ошибка при загрузке статистики по сотрудникам')
        return redirect(url_for('analytics.dashboard'))

@bp.route('/hiring_trends')
@login_required
def hiring_trends():
    """Анализ тенденций найма"""
    try:
        employees = Employee.query.all()
        
        # Создаем график тенденций найма
        hiring_trend_chart = create_hiring_trend_chart(tuple(employees))
        
        # Подготавливаем данные для таблицы
        hiring_data = []
        for emp in employees:
            hiring_data.append({
                'full_name': emp.full_name,
                'department': emp.department.name,
                'position': emp.position.title,
                'hire_date': emp.hire_date
            })
        
        # Сортируем по дате приема на работу
        hiring_data.sort(key=lambda x: x['hire_date'], reverse=True)
        
        return render_template('analytics/hiring_trends.html',
                             hiring_trend_chart=hiring_trend_chart,
                             hiring_data=hiring_data)
    except Exception as e:
        logger.error(f"Error in hiring trends: {str(e)}")
        flash('Ошибка при загрузке тенденций найма')
        return redirect(url_for('analytics.dashboard'))

@bp.route('/vacation_analysis')
@login_required
def vacation_analysis():
    """Анализ отпусков"""
    try:
        # Получаем все отпуска
        vacations = Vacation.query.all()
        
        # Создаем график анализа отпусков
        vacation_chart = create_vacation_analysis_chart(tuple(vacations))
        
        # Подготавливаем данные для таблицы
        vacation_data = []
        for vacation in vacations:
            # Определяем тип отпуска
            if vacation.type == 'paid':
                vacation_type = 'Оплачиваемый'
            elif vacation.type == 'unpaid':
                vacation_type = 'Неоплачиваемый'
            elif vacation.type == 'sick':
                vacation_type = 'Больничный'
            else:
                vacation_type = 'Другое'
            
            vacation_data.append({
                'employee_name': vacation.employee.full_name,
                'department': vacation.employee.department.name,
                'start_date': vacation.start_date,
                'end_date': vacation.end_date,
                'duration': (vacation.end_date - vacation.start_date).days + 1,
                'type': vacation_type
            })
        
        # Сортируем по дате начала отпуска
        vacation_data.sort(key=lambda x: x['start_date'], reverse=True)
        
        return render_template('analytics/vacation_analysis.html',
                             vacation_chart=vacation_chart,
                             vacation_data=vacation_data)
    except Exception as e:
        logger.error(f"Error in vacation analysis: {str(e)}")
        flash('Ошибка при загрузке анализа отпусков')
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
            output = io.StringIO()
            
            # Write header
            output.write('ФИО,Email,Табельный номер,Подразделение,Должность,Дата приема,Статус\n')
            
            # Write data rows
            for emp in employees:
                output.write(f'{emp.full_name},{emp.email},{emp.employee_id},{emp.department.name},{emp.position.title},{emp.hire_date.strftime("%d.%m.%Y")},{emp.status}\n')
            
            csv_data = output.getvalue()
            
            # Return CSV response
            from flask import Response
            return Response(
                csv_data,
                mimetype='text/csv',
                headers={'Content-Disposition': 'attachment; filename=employee_summary_report.csv'}
            )
        else:
            flash('Неверный тип отчета')
            return redirect(url_for('analytics.dashboard'))
    except Exception as e:
        logger.error(f"Error in export report: {str(e)}")
        flash('Ошибка при экспорте отчета')
        return redirect(url_for('analytics.dashboard'))