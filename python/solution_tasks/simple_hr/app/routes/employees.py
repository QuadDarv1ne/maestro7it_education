from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Employee, Department, Position
from app.forms import EmployeeForm
from app.utils.notifications import notify_employee_created, notify_employee_updated
from app.utils.audit import log_employee_create, log_employee_update, log_employee_delete
from app import db

bp = Blueprint('employees', __name__)

@bp.route('/')
@login_required
def list_employees():
    # Получаем параметры пагинации и фильтрации
    page = request.args.get('page', 1, type=int)
    department_id = request.args.get('department_id', type=int)
    position_id = request.args.get('position_id', type=int)
    status = request.args.get('status', type=str)
    search = request.args.get('search', type=str)
    
    # Базовый запрос
    query = Employee.query
    
    # Применяем фильтры
    if department_id:
        query = query.filter(Employee.department_id == department_id)
    
    if position_id:
        query = query.filter(Employee.position_id == position_id)
    
    if status:
        query = query.filter(Employee.status == status)
    
    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            db.or_(
                Employee.full_name.like(search_filter),
                Employee.email.like(search_filter),
                Employee.employee_id.like(search_filter)
            )
        )
    
    # Пагинация
    employees = query.paginate(page=page, per_page=10, error_out=False)
    
    # Получаем все подразделения и должности для фильтров
    departments = Department.query.all()
    positions = Position.query.all()
    
    return render_template('employees/list.html', 
                         employees=employees,
                         departments=departments,
                         positions=positions,
                         current_department=department_id,
                         current_position=position_id,
                         current_status=status,
                         current_search=search)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_employee():
    form = EmployeeForm()
    if form.validate_on_submit():
        # Check if employee already exists
        existing_employee = Employee.query.filter_by(email=form.email.data).first()
        if existing_employee:
            flash('Сотрудник с таким email уже существует')
            return render_template('employees/form.html', form=form)
        
        # Create new employee
        employee = Employee()
        employee.full_name = form.full_name.data
        employee.email = form.email.data
        employee.employee_id = form.employee_id.data
        employee.hire_date = form.hire_date.data
        employee.department_id = form.department_id.data
        employee.position_id = form.position_id.data
        employee.status = form.status.data
        
        try:
            db.session.add(employee)
            db.session.commit()
            # Отправляем уведомление
            notify_employee_created(current_user.id, employee.full_name)
            flash('Сотрудник успешно добавлен')
            return redirect(url_for('employees.list_employees'))
        except Exception as e:
            db.session.rollback()
            flash('Ошибка при добавлении сотрудника')
            return render_template('employees/form.html', form=form)
    
    return render_template('employees/form.html', form=form)

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_employee(id):
    employee = Employee.query.get_or_404(id)
    form = EmployeeForm(obj=employee)
    
    if form.validate_on_submit():
        # Update employee data
        employee.full_name = form.full_name.data
        employee.email = form.email.data
        employee.employee_id = form.employee_id.data
        employee.hire_date = form.hire_date.data
        employee.department_id = form.department_id.data
        employee.position_id = form.position_id.data
        employee.status = form.status.data
        
        try:
            db.session.commit()
            # Отправляем уведомление
            notify_employee_updated(current_user.id, employee.full_name)
            flash('Сотрудник успешно обновлен')
            return redirect(url_for('employees.list_employees'))
        except Exception as e:
            db.session.rollback()
            flash('Ошибка при обновлении сотрудника')
            return render_template('employees/form.html', form=form, employee=employee)
    
    return render_template('employees/form.html', form=form, employee=employee)

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