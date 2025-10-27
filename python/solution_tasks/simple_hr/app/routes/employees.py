from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models import Employee, Department, Position
from app import db

bp = Blueprint('employees', __name__)

@bp.route('/')
@login_required
def list_employees():
    employees = Employee.query.all()
    return render_template('employees/list.html', employees=employees)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_employee():
    if request.method == 'POST':
        # Get form data
        full_name = request.form['full_name']
        email = request.form['email']
        employee_id = request.form['employee_id']
        hire_date = request.form['hire_date']
        department_id = request.form['department_id']
        position_id = request.form['position_id']
        
        # Check if employee already exists
        existing_employee = Employee.query.filter_by(email=email).first()
        if existing_employee:
            flash('Сотрудник с таким email уже существует')
            return redirect(url_for('employees.create_employee'))
        
        # Create new employee
        employee = Employee(
            full_name=full_name,
            email=email,
            employee_id=employee_id,
            hire_date=hire_date,
            department_id=department_id,
            position_id=position_id,
            status='active'
        )
        
        try:
            db.session.add(employee)
            db.session.commit()
            flash('Сотрудник успешно добавлен')
            return redirect(url_for('employees.list_employees'))
        except Exception as e:
            db.session.rollback()
            flash('Ошибка при добавлении сотрудника')
            return redirect(url_for('employees.create_employee'))
    
    departments = Department.query.all()
    positions = Position.query.all()
    return render_template('employees/form.html', departments=departments, positions=positions)

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_employee(id):
    employee = Employee.query.get_or_404(id)
    
    if request.method == 'POST':
        # Update employee data
        employee.full_name = request.form['full_name']
        employee.email = request.form['email']
        employee.employee_id = request.form['employee_id']
        employee.hire_date = request.form['hire_date']
        employee.department_id = request.form['department_id']
        employee.position_id = request.form['position_id']
        
        try:
            db.session.commit()
            flash('Сотрудник успешно обновлен')
            return redirect(url_for('employees.list_employees'))
        except Exception as e:
            db.session.rollback()
            flash('Ошибка при обновлении сотрудника')
            return redirect(url_for('employees.edit_employee', id=id))
    
    departments = Department.query.all()
    positions = Position.query.all()
    return render_template('employees/form.html', employee=employee, departments=departments, positions=positions)

@bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_employee(id):
    employee = Employee.query.get_or_404(id)
    
    try:
        db.session.delete(employee)
        db.session.commit()
        flash('Сотрудник успешно удален')
    except Exception as e:
        db.session.rollback()
        flash('Ошибка при удалении сотрудника')
    
    return redirect(url_for('employees.list_employees'))