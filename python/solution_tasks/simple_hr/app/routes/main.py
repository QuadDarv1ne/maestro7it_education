from flask import Blueprint, render_template
from flask_login import login_required
from app.models import Employee, Department, Position
from app import db

bp = Blueprint('main', __name__)

@bp.route('/')
@login_required
def index():
    # Get statistics
    employee_count = Employee.query.count()
    department_count = Department.query.count()
    position_count = Position.query.count()
    
    # Get recent employees
    recent_employees = Employee.query.order_by(Employee.id.desc()).limit(5).all()
    
    return render_template('dashboard.html', 
                         employee_count=employee_count,
                         department_count=department_count,
                         position_count=position_count,
                         recent_employees=recent_employees)