"""
REST API с документацией Swagger
"""
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import Employee, Department, Position, Vacation
from app import db
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

bp = Blueprint('api', __name__, url_prefix='/api/v1')

# Swagger/OpenAPI документация
@bp.route('/swagger.json')
def swagger_spec():
    """Спецификация OpenAPI/Swagger"""
    spec = {
        "openapi": "3.0.0",
        "info": {
            "title": "Simple HR API",
            "description": "REST API для системы управления персоналом",
            "version": "1.0.0",
            "contact": {
                "name": "Maestro7IT",
                "url": "https://school-maestro7it.ru"
            }
        },
        "servers": [
            {
                "url": "/api/v1",
                "description": "API версии 1"
            }
        ],
        "paths": {
            "/employees": {
                "get": {
                    "summary": "Получить список сотрудников",
                    "tags": ["Employees"],
                    "parameters": [
                        {
                            "name": "page",
                            "in": "query",
                            "schema": {"type": "integer", "default": 1}
                        },
                        {
                            "name": "per_page",
                            "in": "query",
                            "schema": {"type": "integer", "default": 20}
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Список сотрудников",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "employees": {"type": "array"},
                                            "total": {"type": "integer"},
                                            "page": {"type": "integer"}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "components": {
            "securitySchemes": {
                "cookieAuth": {
                    "type": "apiKey",
                    "in": "cookie",
                    "name": "session"
                }
            }
        },
        "security": [{"cookieAuth": []}]
    }
    return jsonify(spec)

@bp.route('/employees', methods=['GET'])
@login_required
def get_employees():
    """
    Получить список сотрудников
    ---
    Параметры:
    - page: номер страницы (по умолчанию 1)
    - per_page: количество на странице (по умолчанию 20)
    - status: фильтр по статусу (active/inactive)
    - department_id: фильтр по подразделению
    """
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        status = request.args.get('status', type=str)
        department_id = request.args.get('department_id', type=int)
        
        query = Employee.query
        
        if status:
            query = query.filter_by(status=status)
        if department_id:
            query = query.filter_by(department_id=department_id)
        
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        employees = [{
            'id': emp.id,
            'employee_id': emp.employee_id,
            'full_name': emp.full_name,
            'email': emp.email,
            'hire_date': emp.hire_date.isoformat() if emp.hire_date else None,
            'status': emp.status,
            'department': emp.department.name if emp.department else None,
            'position': emp.position.title if emp.position else None
        } for emp in pagination.items]
        
        return jsonify({
            'employees': employees,
            'total': pagination.total,
            'page': pagination.page,
            'pages': pagination.pages,
            'per_page': pagination.per_page
        })
    except Exception as e:
        logger.error(f"Error in get_employees API: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/employees/<int:id>', methods=['GET'])
@login_required
def get_employee(id):
    """Получить информацию о сотруднике по ID"""
    try:
        employee = Employee.query.get_or_404(id)
        return jsonify({
            'id': employee.id,
            'employee_id': employee.employee_id,
            'full_name': employee.full_name,
            'email': employee.email,
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
        })
    except Exception as e:
        logger.error(f"Error in get_employee API: {str(e)}")
        return jsonify({'error': str(e)}), 404

@bp.route('/departments', methods=['GET'])
@login_required
def get_departments():
    """Получить список всех подразделений"""
    try:
        departments = Department.query.all()
        return jsonify({
            'departments': [{
                'id': dept.id,
                'name': dept.name,
                'description': dept.description,
                'employee_count': len(dept.employees) if dept.employees else 0
            } for dept in departments]
        })
    except Exception as e:
        logger.error(f"Error in get_departments API: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/positions', methods=['GET'])
@login_required
def get_positions():
    """Получить список всех должностей"""
    try:
        positions = Position.query.all()
        return jsonify({
            'positions': [{
                'id': pos.id,
                'title': pos.title,
                'description': pos.description,
                'employee_count': len(pos.employees) if pos.employees else 0
            } for pos in positions]
        })
    except Exception as e:
        logger.error(f"Error in get_positions API: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/vacations', methods=['GET'])
@login_required
def get_vacations():
    """Получить список отпусков"""
    try:
        status = request.args.get('status', type=str)
        employee_id = request.args.get('employee_id', type=int)
        
        query = Vacation.query
        
        if status:
            query = query.filter_by(status=status)
        if employee_id:
            query = query.filter_by(employee_id=employee_id)
        
        vacations = query.all()
        
        return jsonify({
            'vacations': [{
                'id': vac.id,
                'employee': vac.employee.full_name if vac.employee else None,
                'type': vac.type,
                'start_date': vac.start_date.isoformat() if vac.start_date else None,
                'end_date': vac.end_date.isoformat() if vac.end_date else None,
                'duration': vac.duration_days() if hasattr(vac, 'duration_days') else 0,
                'status': vac.status,
                'notes': vac.notes if hasattr(vac, 'notes') else None
            } for vac in vacations]
        })
    except Exception as e:
        logger.error(f"Error in get_vacations API: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/statistics', methods=['GET'])
@login_required
def get_statistics():
    """Получить общую статистику системы"""
    try:
        stats = {
            'employees': {
                'total': Employee.query.count(),
                'active': Employee.query.filter_by(status='active').count(),
                'inactive': Employee.query.filter_by(status='inactive').count()
            },
            'departments': {
                'total': Department.query.count()
            },
            'positions': {
                'total': Position.query.count()
            },
            'vacations': {
                'total': Vacation.query.count(),
                'pending': Vacation.query.filter_by(status='pending').count(),
                'approved': Vacation.query.filter_by(status='approved').count(),
                'rejected': Vacation.query.filter_by(status='rejected').count()
            }
        }
        return jsonify(stats)
    except Exception as e:
        logger.error(f"Error in get_statistics API: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/health', methods=['GET'])
def health_check():
    """Проверка работоспособности API"""
    try:
        # Проверяем подключение к БД
        db.session.execute(db.text('SELECT 1'))
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'database': 'connected'
        })
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'timestamp': datetime.now().isoformat(),
            'error': str(e)
        }), 500
