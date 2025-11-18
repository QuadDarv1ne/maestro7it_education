from flask import Blueprint, render_template
from flask_login import login_required
from app.models import Employee, Department, Position, Vacation, Order
from app import db, cache
from datetime import datetime, timedelta

bp = Blueprint('main', __name__)

@bp.route('/')
@login_required
@cache.cached(timeout=60)  # Cache for 1 minute
def index():
    # Get statistics
    employee_count = Employee.query.count()
    department_count = Department.query.count()
    position_count = Position.query.count()
    
    # Active employees count
    active_employees = Employee.query.filter_by(status='active').count()
    
    # Recent hires (last 30 days)
    thirty_days_ago = datetime.utcnow().date() - timedelta(days=30)
    recent_hires = Employee.query.filter(
        Employee.hire_date >= thirty_days_ago
    ).count()
    
    # Upcoming vacations (next 7 days)
    today = datetime.utcnow().date()
    week_later = today + timedelta(days=7)
    upcoming_vacations = Vacation.query.filter(
        Vacation.start_date >= today,
        Vacation.start_date <= week_later
    ).count()
    
    # Recent orders (last 10)
    recent_orders = Order.query.order_by(Order.date_issued.desc()).limit(10).all()
    
    # Get recent employees
    recent_employees = Employee.query.order_by(Employee.id.desc()).limit(5).all()
    
    # Department distribution
    departments_with_count = db.session.query(
        Department.name,
        db.func.count(Employee.id).label('count')
    ).join(Employee).group_by(Department.id, Department.name).all()
    
    return render_template('dashboard.html', 
                         employee_count=employee_count,
                         active_employees=active_employees,
                         department_count=department_count,
                         position_count=position_count,
                         recent_hires=recent_hires,
                         upcoming_vacations=upcoming_vacations,
                         recent_employees=recent_employees,
                         recent_orders=recent_orders,
                         departments_with_count=departments_with_count)