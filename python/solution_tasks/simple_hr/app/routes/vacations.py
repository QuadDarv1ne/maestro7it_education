from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Vacation, Employee
from app.forms import VacationForm
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
    form = VacationForm()
    if form.validate_on_submit():
        # Create new vacation
        vacation = Vacation()
        vacation.employee_id = form.employee_id.data
        vacation.start_date = form.start_date.data
        vacation.end_date = form.end_date.data
        vacation.type = form.type.data
        
        try:
            db.session.add(vacation)
            db.session.commit()
            # Отправляем уведомление
            employee = Employee.query.get(form.employee_id.data)
            if employee:
                vacation_type_name = {
                    'paid': 'оплачиваемый',
                    'unpaid': 'неоплачиваемый',
                    'sick': 'больничный'
                }.get(form.type.data, 'отпуск')
                notify_vacation_created(current_user.id, employee.full_name, vacation_type_name, form.start_date.data)
                # Логируем действие
                log_vacation_create(vacation.id, employee.full_name, form.type.data, form.start_date.data.strftime('%d.%m.%Y') if form.start_date.data else '', current_user.id)
            flash('Отпуск успешно добавлен')
            return redirect(url_for('vacations.list_vacations'))
        except Exception as e:
            db.session.rollback()
            flash('Ошибка при добавлении отпуска')
            return render_template('vacations/form.html', form=form)
    
    return render_template('vacations/form.html', form=form)

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_vacation(id):
    vacation = Vacation.query.get_or_404(id)
    form = VacationForm(obj=vacation)
    
    if form.validate_on_submit():
        vacation.employee_id = form.employee_id.data
        vacation.start_date = form.start_date.data
        vacation.end_date = form.end_date.data
        vacation.type = form.type.data
        
        try:
            db.session.commit()
            flash('Отпуск успешно обновлен')
            return redirect(url_for('vacations.list_vacations'))
        except Exception as e:
            db.session.rollback()
            flash('Ошибка при обновлении отпуска')
            return render_template('vacations/form.html', form=form, vacation=vacation)
    
    return render_template('vacations/form.html', form=form, vacation=vacation)

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