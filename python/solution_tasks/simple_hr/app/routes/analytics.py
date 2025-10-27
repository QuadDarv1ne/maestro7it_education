from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models import Employee, Department, Position, Vacation
from app.utils.analytics import (
    create_employee_distribution_chart, 
    create_employee_status_chart,
    create_hiring_trend_chart,
    create_vacation_analysis_chart,
    create_interactive_dashboard_data,
    create_interactive_charts
)
from app import db
from datetime import datetime, date

bp = Blueprint('analytics', __name__)

@bp.route('/')
@login_required
def dashboard():
    """Главная страница аналитики"""
    # Получаем все данные
    employees = Employee.query.all()
    departments = Department.query.all()
    positions = Position.query.all()
    vacations = Vacation.query.all()
    
    # Создаем интерактивные данные для дашборда
    interactive_data = create_interactive_dashboard_data(employees, departments, positions, vacations)
    
    # Создаем интерактивные графики
    interactive_charts = create_interactive_charts(interactive_data)
    
    return render_template('analytics/dashboard.html', 
                         interactive_data=interactive_data,
                         interactive_charts=interactive_charts)

@bp.route('/employee_statistics')
@login_required
def employee_statistics():
    """Статистика по сотрудникам"""
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
    distribution_chart = create_employee_distribution_chart(department_stats)
    status_chart = create_employee_status_chart(active_employees, dismissed_employees)
    
    return render_template('analytics/employee_statistics.html',
                         total_employees=total_employees,
                         active_employees=active_employees,
                         dismissed_employees=dismissed_employees,
                         department_stats=department_stats,
                         position_stats=position_stats,
                         distribution_chart=distribution_chart,
                         status_chart=status_chart)

@bp.route('/hiring_trends')
@login_required
def hiring_trends():
    """Анализ тенденций найма"""
    employees = Employee.query.all()
    
    # Создаем график тенденций найма
    hiring_trend_chart = create_hiring_trend_chart(employees)
    
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

@bp.route('/vacation_analysis')
@login_required
def vacation_analysis():
    """Анализ отпусков"""
    # Получаем все отпуска
    vacations = Vacation.query.all()
    
    # Создаем график анализа отпусков
    vacation_chart = create_vacation_analysis_chart(vacations)
    
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

@bp.route('/export_report')
@login_required
def export_report():
    """Экспорт аналитических отчетов"""
    report_type = request.args.get('type', 'summary')
    
    # Здесь будет реализация экспорта отчетов
    flash('Функция экспорта отчетов будет реализована в следующих версиях')
    return redirect(url_for('analytics.dashboard'))