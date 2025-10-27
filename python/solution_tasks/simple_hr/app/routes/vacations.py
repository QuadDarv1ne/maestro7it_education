from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Vacation, Employee
from app.utils.notifications import notify_vacation_created
from app.utils.audit import log_vacation_create
from app import db
from datetime import datetime

bp = Blueprint('vacations', __name__)

@bp.route('/')
@login_required
def list_vacations():
    vacations = Vacation.query.all()
    return render_template('vacations/list.html', vacations=vacations)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_vacation():
    if request.method == 'POST':
        employee_id = request.form['employee_id']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        vacation_type = request.form['type']
        
        # Validate dates
        start = datetime.strptime(start_date, '%Y-%m-%d').date()
        end = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        if start >= end:
            flash('Дата окончания должна быть позже даты начала')
            return redirect(url_for('vacations.create_vacation'))
        
        # Create new vacation
        vacation = Vacation()
        vacation.employee_id = employee_id
        vacation.start_date = start
        vacation.end_date = end
        vacation.type = vacation_type
        
        try:
            db.session.add(vacation)
            db.session.commit()
            # Отправляем уведомление
            employee = Employee.query.get(employee_id)
            if employee:
                vacation_type_name = {
                    'paid': 'оплачиваемый',
                    'unpaid': 'неоплачиваемый',
                    'sick': 'больничный'
                }.get(vacation_type, 'отпуск')
                notify_vacation_created(current_user.id, employee.full_name, vacation_type_name, start)
                # Логируем действие
                log_vacation_create(vacation.id, employee.full_name, vacation_type, start.strftime('%d.%m.%Y'), current_user.id)
            flash('Отпуск успешно добавлен')
            return redirect(url_for('vacations.list_vacations'))
        except Exception as e:
            db.session.rollback()
            flash('Ошибка при добавлении отпуска')
            return redirect(url_for('vacations.create_vacation'))
    
    employees = Employee.query.all()
    return render_template('vacations/form.html', employees=employees)

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_vacation(id):
    vacation = Vacation.query.get_or_404(id)
    
    if request.method == 'POST':
        vacation.employee_id = request.form['employee_id']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        vacation.type = request.form['type']
        
        # Validate dates
        start = datetime.strptime(start_date, '%Y-%m-%d').date()
        end = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        if start >= end:
            flash('Дата окончания должна быть позже даты начала')
            return redirect(url_for('vacations.edit_vacation', id=id))
        
        vacation.start_date = start
        vacation.end_date = end
        
        try:
            db.session.commit()
            flash('Отпуск успешно обновлен')
            return redirect(url_for('vacations.list_vacations'))
        except Exception as e:
            db.session.rollback()
            flash('Ошибка при обновлении отпуска')
            return redirect(url_for('vacations.edit_vacation', id=id))
    
    employees = Employee.query.all()
    return render_template('vacations/form.html', vacation=vacation, employees=employees)

@bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_vacation(id):
    vacation = Vacation.query.get_or_404(id)
    
    try:
        db.session.delete(vacation)
        db.session.commit()
        flash('Отпуск успешно удален')
    except Exception as e:
        db.session.rollback()
        flash('Ошибка при удалении отпуска')
    
    return redirect(url_for('vacations.list_vacations'))