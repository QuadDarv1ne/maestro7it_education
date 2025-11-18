from flask import Blueprint, render_template, current_app
from flask_login import login_required, current_user
from app.models import Employee, Department, Position, Vacation, Order, Notification
from app import db, cache
from datetime import datetime, timedelta
from sqlalchemy import func

bp = Blueprint('main', __name__)

@bp.route('/')
@login_required
@cache.cached(timeout=60)  # Cache for 1 minute
def index():
    # Get statistics
    employee_count = Employee.query.filter_by(status='active').count()
    department_count = Department.query.count()
    position_count = Position.query.count()
    
    # Current vacations
    today = datetime.utcnow().date()
    vacation_count = Vacation.query.filter(
        Vacation.start_date <= today,
        Vacation.end_date >= today,
        Vacation.status == 'approved'
    ).count()
    
    # Birthdays in next 30 days (simulated)
    birthday_count = 0  # TODO: Add birth_date field to Employee model
    
    # Orders count
    order_count = Order.query.count()
    
    # Get recent employees (last 10)
    recent_employees = Employee.query.order_by(Employee.id.desc()).limit(10).all()
    
    # Get recent notifications for current user (last 5)
    recent_notifications = Notification.query.filter_by(
        user_id=current_user.id
    ).order_by(Notification.created_at.desc()).limit(5).all()
    
    # Activity data for chart (new employees per day for last 30 days)
    # Note: Using hire_date as proxy for created_at since Employee model doesn't have created_at
    activity_labels = []
    activity_data = []
    for i in range(29, -1, -1):
        date = today - timedelta(days=i)
        next_date = date + timedelta(days=1)
        count = Employee.query.filter(
            Employee.hire_date >= date,
            Employee.hire_date < next_date
        ).count()
        activity_labels.append(date.strftime('%d.%m'))
        activity_data.append(count)
    
    # Current date formatted in Russian
    months_ru = {
        1: 'января', 2: 'февраля', 3: 'марта', 4: 'апреля',
        5: 'мая', 6: 'июня', 7: 'июля', 8: 'августа',
        9: 'сентября', 10: 'октября', 11: 'ноября', 12: 'декабря'
    }
    current_date = f"{today.day} {months_ru[today.month]} {today.year} г."
    
    return render_template('dashboard.html',
                         employee_count=employee_count,
                         department_count=department_count,
                         position_count=position_count,
                         vacation_count=vacation_count,
                         birthday_count=birthday_count,
                         order_count=order_count,
                         recent_employees=recent_employees,
                         recent_notifications=recent_notifications,
                         activity_labels=activity_labels,
                         activity_data=activity_data,
                         current_date=current_date)

@bp.route('/animations-demo')
@login_required
def animations_demo():
    """Demo page for loading animations and skeletons"""
    return render_template('animations_demo.html')
@bp.route('/features-demo')
@login_required
def features_demo():
    ""Demo page for new features""
    return render_template('features_demo.html')
