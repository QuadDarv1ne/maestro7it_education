from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Employee, Department, Position
from app.forms import EmployeeForm, EmployeeSearchForm
from app.utils.notifications import notify_employee_created, notify_employee_updated
from app.utils.audit import log_employee_create, log_employee_update, log_employee_delete
from app.utils.csv_import import import_employees_from_csv
from app import db
import os
from sqlalchemy import or_
import logging

# Set up logging
logger = logging.getLogger(__name__)

bp = Blueprint('employees', __name__)

@bp.route('/')
@login_required
def list_employees():
    try:
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
                or_(
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
        
        # Create search form
        search_form = EmployeeSearchForm()
        search_form.department_id.data = department_id
        search_form.position_id.data = position_id
        search_form.status.data = status
        search_form.search.data = search
        
        return render_template('employees/list.html', 
                             employees=employees,
                             departments=departments,
                             positions=positions,
                             current_department=department_id,
                             current_position=position_id,
                             current_status=status,
                             current_search=search,
                             search_form=search_form)
    except Exception as e:
        logger.error(f"Error in list_employees: {str(e)}")
        flash('Ошибка при загрузке списка сотрудников', 'error')
        return redirect(url_for('main.index'))

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_employee():
    form = EmployeeForm()
    try:
        if form.validate_on_submit():
            try:
                # Check if employee already exists
                existing_employee = Employee.query.filter_by(email=form.email.data).first()
                if existing_employee:
                    flash('Сотрудник с таким email уже существует', 'error')
                    return render_template('employees/form.html', form=form)
                
                # Create new employee
                employee = Employee()
                employee.full_name = form.full_name.data.strip() if form.full_name.data is not None else ""
                employee.email = form.email.data.strip().lower() if form.email.data is not None else ""
                employee.employee_id = form.employee_id.data.strip() if form.employee_id.data is not None else ""
                employee.hire_date = form.hire_date.data
                employee.department_id = form.department_id.data if form.department_id.data is not None else 0
                employee.position_id = form.position_id.data if form.position_id.data is not None else 0
                employee.status = form.status.data
                
                db.session.add(employee)
                db.session.commit()
                # Отправляем уведомление
                notify_employee_created(current_user.id, employee.full_name)
                # Логируем действие
                log_employee_create(employee.id, employee.full_name, current_user.id)
                flash('Сотрудник успешно добавлен', 'success')
                return redirect(url_for('employees.list_employees'))
            except Exception as e:
                db.session.rollback()
                logger.error(f"Error creating employee: {str(e)}")
                flash(f'Ошибка при добавлении сотрудника: {str(e)}', 'error')
                return render_template('employees/form.html', form=form)
        elif request.method == 'POST':
            # Form validation failed - let's check what data was submitted
            logger.info(f"Form validation failed. Form data: {request.form}")
            flash('Пожалуйста, исправьте ошибки в форме', 'error')
        
        return render_template('employees/form.html', form=form)
    except Exception as e:
        logger.error(f"Error in create_employee route: {str(e)}")
        flash('Ошибка при создании сотрудника', 'error')
        return render_template('employees/form.html', form=form)

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_employee(id):
    try:
        employee = Employee.query.get_or_404(id)
        form = EmployeeForm(obj=employee)
        
        # Set original values for validation
        form.original_email = employee.email
        form.original_employee_id = employee.employee_id
        
        if form.validate_on_submit():
            try:
                # Update employee data
                employee.full_name = form.full_name.data.strip() if form.full_name.data is not None else employee.full_name
                employee.email = form.email.data.strip().lower() if form.email.data is not None else employee.email
                employee.employee_id = form.employee_id.data.strip() if form.employee_id.data is not None else employee.employee_id
                employee.hire_date = form.hire_date.data
                employee.department_id = form.department_id.data if form.department_id.data is not None else employee.department_id
                employee.position_id = form.position_id.data if form.position_id.data is not None else employee.position_id
                employee.status = form.status.data
                
                db.session.commit()
                # Отправляем уведомление
                notify_employee_updated(current_user.id, employee.full_name)
                # Логируем действие
                log_employee_update(employee.id, employee.full_name, current_user.id)
                flash('Сотрудник успешно обновлен', 'success')
                return redirect(url_for('employees.list_employees'))
            except Exception as e:
                db.session.rollback()
                logger.error(f"Error updating employee {id}: {str(e)}")
                flash(f'Ошибка при обновлении сотрудника: {str(e)}', 'error')
                return render_template('employees/form.html', form=form, employee=employee)
        elif request.method == 'POST':
            # Form validation failed
            flash('Пожалуйста, исправьте ошибки в форме', 'error')
        
        return render_template('employees/form.html', form=form, employee=employee)
    except Exception as e:
        logger.error(f"Error in edit_employee {id}: {str(e)}")
        flash('Ошибка при редактировании сотрудника', 'error')
        return redirect(url_for('employees.list_employees'))

@bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_employee(id):
    try:
        employee = Employee.query.get_or_404(id)
        
        # Сохраняем имя сотрудника для логирования
        employee_name = employee.full_name
        employee_id = employee.id
        db.session.delete(employee)
        db.session.commit()
        # Логируем действие
        log_employee_delete(employee_id, employee_name, current_user.id)
        flash('Сотрудник успешно удален', 'success')
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting employee {id}: {str(e)}")
        flash(f'Ошибка при удалении сотрудника: {str(e)}', 'error')
    
    return redirect(url_for('employees.list_employees'))

@bp.route('/import', methods=['GET', 'POST'])
@login_required
def import_employees():
    if request.method == 'POST':
        try:
            # Check if file was uploaded
            if 'file' not in request.files:
                flash('Файл не выбран', 'error')
                return redirect(request.url)
            
            file = request.files['file']
            
            # Check if file was selected
            if file.filename == '':
                flash('Файл не выбран', 'error')
                return redirect(request.url)
            
            # Check if file is CSV
            if not file.filename or not file.filename.endswith('.csv'):
                flash('Пожалуйста, загрузите файл в формате CSV', 'error')
                return redirect(request.url)
            
            # Save file temporarily
            filepath = os.path.join('temp_import.csv')
            file.save(filepath)
            
            try:
                # Import employees
                report = import_employees_from_csv(filepath)
                
                # Remove temporary file
                os.remove(filepath)
                
                # Show import results
                flash(f'Импорт завершен: {report["imported"]} импортировано, {report["skipped"]} пропущено, {len(report["errors"])} ошибок', 'info')
                return render_template('employees/import_results.html', report=report)
                
            except Exception as e:
                # Remove temporary file if exists
                if os.path.exists(filepath):
                    os.remove(filepath)
                logger.error(f"Error importing employees: {str(e)}")
                flash(f'Ошибка при импорте: {str(e)}', 'error')
                return redirect(url_for('employees.import_employees'))
        except Exception as e:
            logger.error(f"Error in import_employees POST: {str(e)}")
            flash('Ошибка при импорте сотрудников', 'error')
            return redirect(url_for('employees.import_employees'))
    
    return render_template('employees/import.html')

@bp.route('/details/<int:id>')
@login_required
def employee_details(id):
    """Просмотр деталей сотрудника"""
    try:
        employee = Employee.query.get_or_404(id)
        return render_template('employees/details.html', employee=employee)
    except Exception as e:
        logger.error(f"Error in employee_details {id}: {str(e)}")
        flash('Ошибка при загрузке информации о сотруднике', 'error')
        return redirect(url_for('employees.list_employees'))