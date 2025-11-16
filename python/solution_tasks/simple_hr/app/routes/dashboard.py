"""
Маршруты для интерактивного дашборда
"""
from flask import Blueprint, render_template, jsonify
from flask_login import login_required
from app.models import Employee, Department, Position, Vacation
from app import db, cache
from sqlalchemy import func, extract
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

bp = Blueprint('dashboard', __name__)

@bp.route('/')
@login_required
def index():
    """Главная страница дашборда"""
    try:
        # Получаем базовую статистику
        total_employees = Employee.query.filter_by(status='active').count()
        total_departments = Department.query.count()
        total_positions = Position.query.count()
        
        # Отпуска
        active_vacations = Vacation.query.filter(
            Vacation.start_date <= datetime.now().date(),
            Vacation.end_date >= datetime.now().date(),
            Vacation.status == 'approved'
        ).count()
        
        pending_vacations = Vacation.query.filter_by(status='pending').count()
        
        return render_template('dashboard/index.html',
                             total_employees=total_employees,
                             total_departments=total_departments,
                             total_positions=total_positions,
                             active_vacations=active_vacations,
                             pending_vacations=pending_vacations)
    except Exception as e:
        logger.error(f"Error loading dashboard: {str(e)}")
        return render_template('dashboard/index.html',
                             total_employees=0,
                             total_departments=0,
                             total_positions=0,
                             active_vacations=0,
                             pending_vacations=0)

@bp.route('/api/employees-by-department')
@login_required
@cache.cached(timeout=300, key_prefix='dashboard_employees_by_department')
def employees_by_department():
    """API: Распределение сотрудников по подразделениям"""
    try:
        data = db.session.query(
            Department.name,
            func.count(Employee.id).label('count')
        ).join(Employee, Employee.department_id == Department.id)\
         .filter(Employee.status == 'active')\
         .group_by(Department.id, Department.name)\
         .all()
        
        return jsonify({
            'labels': [row[0] for row in data],
            'data': [row[1] for row in data]
        })
    except Exception as e:
        logger.error(f"Error getting employees by department: {str(e)}")
        return jsonify({'labels': [], 'data': []})

@bp.route('/api/employees-by-position')
@login_required
def employees_by_position():
    """API: Распределение сотрудников по должностям"""
    try:
        data = db.session.query(
            Position.title,
            func.count(Employee.id).label('count')
        ).join(Employee, Employee.position_id == Position.id)\
         .filter(Employee.status == 'active')\
         .group_by(Position.id, Position.title)\
         .order_by(func.count(Employee.id).desc())\
         .limit(10)\
         .all()
        
        return jsonify({
            'labels': [row[0] for row in data],
            'data': [row[1] for row in data]
        })
    except Exception as e:
        logger.error(f"Error getting employees by position: {str(e)}")
        return jsonify({'labels': [], 'data': []})

@bp.route('/api/hiring-trends')
@login_required
@cache.cached(timeout=600, key_prefix='dashboard_hiring_trends')
def hiring_trends():
    """API: Тренды найма по месяцам (последние 12 месяцев)"""
    try:
        # Последние 12 месяцев
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=365)
        
        # Группируем по месяцам
        data = db.session.query(
            extract('year', Employee.hire_date).label('year'),
            extract('month', Employee.hire_date).label('month'),
            func.count(Employee.id).label('count')
        ).filter(
            Employee.hire_date >= start_date,
            Employee.hire_date <= end_date
        ).group_by('year', 'month')\
         .order_by('year', 'month')\
         .all()
        
        # Форматируем данные
        labels = []
        counts = []
        
        months = ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 
                 'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек']
        
        for row in data:
            year = int(row[0])
            month = int(row[1])
            count = row[2]
            
            labels.append(f"{months[month-1]} {year}")
            counts.append(count)
        
        return jsonify({
            'labels': labels,
            'data': counts
        })
    except Exception as e:
        logger.error(f"Error getting hiring trends: {str(e)}")
        return jsonify({'labels': [], 'data': []})

@bp.route('/api/vacation-statistics')
@login_required
def vacation_statistics():
    """API: Статистика отпусков по типам"""
    try:
        # Получаем количество отпусков по типам
        data = db.session.query(
            Vacation.type,
            func.count(Vacation.id).label('count')
        ).filter(
            Vacation.status == 'approved'
        ).group_by(Vacation.type)\
         .all()
        
        # Перевод типов отпусков
        vacation_types = {
            'paid': 'Оплачиваемый',
            'unpaid': 'Неоплачиваемый',
            'sick': 'Больничный'
        }
        
        labels = [vacation_types.get(row[0], row[0]) for row in data]
        counts = [row[1] for row in data]
        
        return jsonify({
            'labels': labels,
            'data': counts
        })
    except Exception as e:
        logger.error(f"Error getting vacation statistics: {str(e)}")
        return jsonify({'labels': [], 'data': []})

@bp.route('/api/vacation-status-distribution')
@login_required
def vacation_status_distribution():
    """API: Распределение отпусков по статусам"""
    try:
        data = db.session.query(
            Vacation.status,
            func.count(Vacation.id).label('count')
        ).group_by(Vacation.status)\
         .all()
        
        status_types = {
            'pending': 'Ожидает',
            'approved': 'Одобрен',
            'rejected': 'Отклонен'
        }
        
        labels = [status_types.get(row[0], row[0]) for row in data]
        counts = [row[1] for row in data]
        
        return jsonify({
            'labels': labels,
            'data': counts
        })
    except Exception as e:
        logger.error(f"Error getting vacation status distribution: {str(e)}")
        return jsonify({'labels': [], 'data': []})

@bp.route('/api/employee-status-distribution')
@login_required
def employee_status_distribution():
    """API: Распределение сотрудников по статусам"""
    try:
        data = db.session.query(
            Employee.status,
            func.count(Employee.id).label('count')
        ).group_by(Employee.status)\
         .all()
        
        status_types = {
            'active': 'Активные',
            'inactive': 'Уволенные'
        }
        
        labels = [status_types.get(row[0], row[0]) for row in data]
        counts = [row[1] for row in data]
        
        return jsonify({
            'labels': labels,
            'data': counts
        })
    except Exception as e:
        logger.error(f"Error getting employee status distribution: {str(e)}")
        return jsonify({'labels': [], 'data': []})
