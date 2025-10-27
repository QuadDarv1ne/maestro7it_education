from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Department
from app.utils.audit import log_department_create, log_department_update, log_department_delete
from app import db

bp = Blueprint('departments', __name__)

@bp.route('/')
@login_required
def list_departments():
    departments = Department.query.all()
    return render_template('departments/list.html', departments=departments)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_department():
    if request.method == 'POST':
        name = request.form['name']
        
        # Check if department already exists
        existing_dept = Department.query.filter_by(name=name).first()
        if existing_dept:
            flash('Подразделение с таким названием уже существует')
            return redirect(url_for('departments.create_department'))
        
        # Create new department
        department = Department()
        department.name = name
        
        try:
            db.session.add(department)
            db.session.commit()
            # Логируем действие
            log_department_create(department.id, department.name, current_user.id)
            flash('Подразделение успешно добавлено')
            return redirect(url_for('departments.list_departments'))
        except Exception as e:
            db.session.rollback()
            flash('Ошибка при добавлении подразделения')
            return redirect(url_for('departments.create_department'))
    
    return render_template('departments/form.html')

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_department(id):
    department = Department.query.get_or_404(id)
    
    if request.method == 'POST':
        name = request.form['name']
        
        # Check if another department with the same name exists
        existing_dept = Department.query.filter_by(name=name).first()
        if existing_dept and existing_dept.id != id:
            flash('Подразделение с таким названием уже существует')
            return redirect(url_for('departments.edit_department', id=id))
        
        department.name = name
        
        try:
            db.session.commit()
            # Логируем действие
            log_department_update(department.id, department.name, current_user.id)
            flash('Подразделение успешно обновлено')
            return redirect(url_for('departments.list_departments'))
        except Exception as e:
            db.session.rollback()
            flash('Ошибка при обновлении подразделения')
            return redirect(url_for('departments.edit_department', id=id))
    
    return render_template('departments/form.html', department=department)

@bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_department(id):
    department = Department.query.get_or_404(id)
    
    # Check if department has employees
    if department.employees:
        flash('Невозможно удалить подразделение, так как в нем есть сотрудники')
        return redirect(url_for('departments.list_departments'))
    
    try:
        # Сохраняем данные для логирования
        dept_id = department.id
        dept_name = department.name
        db.session.delete(department)
        db.session.commit()
        # Логируем действие
        log_department_delete(dept_id, dept_name, current_user.id)
        flash('Подразделение успешно удалено')
    except Exception as e:
        db.session.rollback()
        flash('Ошибка при удалении подразделения')
    
    return redirect(url_for('departments.list_departments'))