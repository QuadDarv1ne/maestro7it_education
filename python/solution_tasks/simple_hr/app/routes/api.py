"""
REST API endpoints для Simple HR
"""
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import Employee, Department, Position, Vacation, Order, User
from app import db, limiter
from app.utils.decorators import admin_required
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

bp = Blueprint('api', __name__, url_prefix='/api/v1')


# Helper functions
def serialize_employee(employee):
    """Сериализация сотрудника в JSON"""
    return {
        'id': employee.id,
        'full_name': employee.full_name,
        'email': employee.email,
        'employee_id': employee.employee_id,
        'hire_date': employee.hire_date.isoformat() if employee.hire_date else None,
        'status': employee.status,
        'department': {
            'id': employee.department.id,
            'name': employee.department.name
        } if employee.department else None,
        'position': {
            'id': employee.position.id,
            'title': employee.position.title
        } if employee.position else None
    }


def serialize_department(department):
    """Сериализация отдела в JSON"""
    return {
        'id': department.id,
        'name': department.name,
        'employee_count': len(department.employees) if department.employees else 0
    }


def serialize_vacation(vacation):
    """Сериализация отпуска в JSON"""
    return {
        'id': vacation.id,
        'employee': {
            'id': vacation.employee.id,
            'full_name': vacation.employee.full_name
        } if vacation.employee else None,
        'start_date': vacation.start_date.isoformat() if vacation.start_date else None,
        'end_date': vacation.end_date.isoformat() if vacation.end_date else None,
        'type': vacation.type,
        'duration_days': (vacation.end_date - vacation.start_date).days + 1 if vacation.start_date and vacation.end_date else None
    }


# Employees API
@bp.route('/employees', methods=['GET'])
@login_required
@limiter.limit("100 per hour")
def get_employees():
    """Получить список всех сотрудников"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        status = request.args.get('status', None)
        department_id = request.args.get('department_id', None, type=int)
        
        # Ограничение per_page
        per_page = min(per_page, 100)
        
        query = Employee.query
        
        if status:
            query = query.filter_by(status=status)
        if department_id:
            query = query.filter_by(department_id=department_id)
        
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'success': True,
            'data': [serialize_employee(emp) for emp in pagination.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'pages': pagination.pages,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        }), 200
    except Exception as e:
        logger.error(f"Error fetching employees: {str(e)}")
        return jsonify({'success': False, 'error': 'Internal server error'}), 500


@bp.route('/employees/<int:id>', methods=['GET'])
@login_required
@limiter.limit("100 per hour")
def get_employee(id):
    """Получить информацию о конкретном сотруднике"""
    try:
        employee = Employee.query.get_or_404(id)
        return jsonify({
            'success': True,
            'data': serialize_employee(employee)
        }), 200
    except Exception as e:
        logger.error(f"Error fetching employee {id}: {str(e)}")
        return jsonify({'success': False, 'error': 'Employee not found'}), 404


@bp.route('/employees', methods=['POST'])
@login_required
@limiter.limit("20 per hour")
def create_employee():
    """Создать нового сотрудника"""
    try:
        data = request.get_json()
        
        # Валидация
        required_fields = ['full_name', 'email', 'employee_id', 'hire_date', 'department_id', 'position_id']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Missing required field: {field}'}), 400
        
        # Проверка на дубликаты
        if Employee.query.filter_by(email=data['email']).first():
            return jsonify({'success': False, 'error': 'Email already exists'}), 400
        
        if Employee.query.filter_by(employee_id=data['employee_id']).first():
            return jsonify({'success': False, 'error': 'Employee ID already exists'}), 400
        
        # Создание сотрудника
        employee = Employee(
            full_name=data['full_name'],
            email=data['email'],
            employee_id=data['employee_id'],
            hire_date=datetime.fromisoformat(data['hire_date']),
            department_id=data['department_id'],
            position_id=data['position_id'],
            status=data.get('status', 'active')
        )
        
        db.session.add(employee)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Employee created successfully',
            'data': serialize_employee(employee)
        }), 201
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating employee: {str(e)}")
        return jsonify({'success': False, 'error': 'Failed to create employee'}), 500


@bp.route('/employees/<int:id>', methods=['PUT'])
@login_required
@limiter.limit("50 per hour")
def update_employee(id):
    """Обновить информацию о сотруднике"""
    try:
        employee = Employee.query.get_or_404(id)
        data = request.get_json()
        
        # Обновление полей
        if 'full_name' in data:
            employee.full_name = data['full_name']
        if 'email' in data:
            # Проверка на дубликат email
            existing = Employee.query.filter_by(email=data['email']).first()
            if existing and existing.id != id:
                return jsonify({'success': False, 'error': 'Email already exists'}), 400
            employee.email = data['email']
        if 'status' in data:
            employee.status = data['status']
        if 'department_id' in data:
            employee.department_id = data['department_id']
        if 'position_id' in data:
            employee.position_id = data['position_id']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Employee updated successfully',
            'data': serialize_employee(employee)
        }), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating employee {id}: {str(e)}")
        return jsonify({'success': False, 'error': 'Failed to update employee'}), 500


@bp.route('/employees/<int:id>', methods=['DELETE'])
@login_required
@admin_required
@limiter.limit("10 per hour")
def delete_employee(id):
    """Удалить сотрудника"""
    try:
        employee = Employee.query.get_or_404(id)
        db.session.delete(employee)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Employee deleted successfully'
        }), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting employee {id}: {str(e)}")
        return jsonify({'success': False, 'error': 'Failed to delete employee'}), 500


# Departments API
@bp.route('/departments', methods=['GET'])
@login_required
@limiter.limit("100 per hour")
def get_departments():
    """Получить список всех отделов"""
    try:
        departments = Department.query.all()
        return jsonify({
            'success': True,
            'data': [serialize_department(dept) for dept in departments]
        }), 200
    except Exception as e:
        logger.error(f"Error fetching departments: {str(e)}")
        return jsonify({'success': False, 'error': 'Internal server error'}), 500


@bp.route('/departments/<int:id>', methods=['GET'])
@login_required
@limiter.limit("100 per hour")
def get_department(id):
    """Получить информацию об отделе"""
    try:
        department = Department.query.get_or_404(id)
        return jsonify({
            'success': True,
            'data': serialize_department(department)
        }), 200
    except Exception as e:
        logger.error(f"Error fetching department {id}: {str(e)}")
        return jsonify({'success': False, 'error': 'Department not found'}), 404


# Vacations API
@bp.route('/vacations', methods=['GET'])
@login_required
@limiter.limit("100 per hour")
def get_vacations():
    """Получить список отпусков"""
    try:
        employee_id = request.args.get('employee_id', None, type=int)
        vacation_type = request.args.get('type', None)
        
        query = Vacation.query
        
        if employee_id:
            query = query.filter_by(employee_id=employee_id)
        if vacation_type:
            query = query.filter_by(type=vacation_type)
        
        vacations = query.all()
        
        return jsonify({
            'success': True,
            'data': [serialize_vacation(vac) for vac in vacations]
        }), 200
    except Exception as e:
        logger.error(f"Error fetching vacations: {str(e)}")
        return jsonify({'success': False, 'error': 'Internal server error'}), 500


# Statistics API
@bp.route('/statistics', methods=['GET'])
@login_required
@limiter.limit("50 per hour")
def get_statistics():
    """Получить общую статистику"""
    try:
        stats = {
            'employees': {
                'total': Employee.query.count(),
                'active': Employee.query.filter_by(status='active').count(),
                'dismissed': Employee.query.filter_by(status='dismissed').count()
            },
            'departments': {
                'total': Department.query.count()
            },
            'positions': {
                'total': Position.query.count()
            },
            'vacations': {
                'total': Vacation.query.count(),
                'paid': Vacation.query.filter_by(type='paid').count(),
                'unpaid': Vacation.query.filter_by(type='unpaid').count(),
                'sick': Vacation.query.filter_by(type='sick').count()
            }
        }
        
        return jsonify({
            'success': True,
            'data': stats
        }), 200
    except Exception as e:
        logger.error(f"Error fetching statistics: {str(e)}")
        return jsonify({'success': False, 'error': 'Internal server error'}), 500


# Error handlers
@bp.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'error': 'Resource not found'}), 404


@bp.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'success': False, 'error': 'Internal server error'}), 500
