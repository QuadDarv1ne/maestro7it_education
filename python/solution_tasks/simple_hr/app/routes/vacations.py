from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Vacation, Employee
from app.forms import VacationForm
from app.utils.notifications import notify_vacation_created
from app.utils.audit import log_vacation_create
from app import db
from datetime import datetime, date
from calendar import monthrange
import logging

# Set up logging
logger = logging.getLogger(__name__)

bp = Blueprint('vacations', __name__)

@bp.route('/')
@login_required
def list_vacations():
    try:
        vacations = Vacation.query.all()
        return render_template('vacations/list.html', vacations=vacations)
    except Exception as e:
        logger.error(f"Error loading vacations list: {str(e)}")
        flash('Ошибка при загрузке списка отпусков', 'error')
        return redirect(url_for('main.index'))

@bp.route('/calendar')
@login_required
def vacation_calendar():
    try:
        # Get month and year from query parameters, default to current month
        today = date.today()
        year = request.args.get('year', type=int, default=today.year)
        month = request.args.get('month', type=int, default=today.month)
        
        # Get all vacations for the selected month
        start_date = date(year, month, 1)
        end_date = date(year, month, monthrange(year, month)[1])
        
        vacations = Vacation.query.filter(
            Vacation.start_date <= end_date,
            Vacation.end_date >= start_date
        ).all()
        
        # Create a dictionary to store vacations by date
        vacation_calendar = {}
        for vacation in vacations:
            current_date = max(vacation.start_date, start_date)
            end_range = min(vacation.end_date, end_date)
            
            while current_date <= end_range:
                if current_date not in vacation_calendar:
                    vacation_calendar[current_date] = []
                vacation_calendar[current_date].append(vacation)
                current_date = date.fromordinal(current_date.toordinal() + 1)
        
        return render_template('vacations/calendar.html', 
                             vacation_calendar=vacation_calendar,
                             year=year, 
                             month=month,
                             start_date=start_date,
                             end_date=end_date,
                             date=date)  # Pass the date function to the template
    except Exception as e:
        logger.error(f"Error loading vacation calendar: {str(e)}")
        flash('Ошибка при загрузке календаря отпусков', 'error')
        return redirect(url_for('main.index'))

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_vacation():
    form = VacationForm()
    try:
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
                flash('Отпуск успешно добавлен', 'success')
                return redirect(url_for('vacations.list_vacations'))
            except Exception as e:
                db.session.rollback()
                logger.error(f"Error saving vacation: {str(e)}")
                flash('Ошибка при добавлении отпуска', 'error')
                return render_template('vacations/form.html', form=form)
        
        # If form is not submitted or validation failed, render the form
        return render_template('vacations/form.html', form=form)
    except Exception as e:
        logger.error(f"Error in create_vacation route: {str(e)}")
        flash('Ошибка при создании отпуска', 'error')
        return render_template('vacations/form.html', form=form)

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_vacation(id):
    try:
        vacation = Vacation.query.get_or_404(id)
        form = VacationForm(vacation_id=id, obj=vacation)
        
        if form.validate_on_submit():
            vacation.employee_id = form.employee_id.data
            vacation.start_date = form.start_date.data
            vacation.end_date = form.end_date.data
            vacation.type = form.type.data
            
            try:
                db.session.commit()
                flash('Отпуск успешно обновлен', 'success')
                return redirect(url_for('vacations.list_vacations'))
            except Exception as e:
                db.session.rollback()
                logger.error(f"Error updating vacation {id}: {str(e)}")
                flash('Ошибка при обновлении отпуска', 'error')
                return render_template('vacations/form.html', form=form, vacation=vacation)
        
        return render_template('vacations/form.html', form=form, vacation=vacation)
    except Exception as e:
        logger.error(f"Error in edit_vacation {id}: {str(e)}")
        flash('Ошибка при редактировании отпуска', 'error')
        return redirect(url_for('vacations.list_vacations'))

@bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_vacation(id):
    try:
        vacation = Vacation.query.get_or_404(id)
        
        try:
            db.session.delete(vacation)
            db.session.commit()
            flash('Отпуск успешно удален', 'success')
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error deleting vacation {id}: {str(e)}")
            flash('Ошибка при удалении отпуска', 'error')
    except Exception as e:
        logger.error(f"Error in delete_vacation {id}: {str(e)}")
        flash('Ошибка при удалении отпуска', 'error')
    
    return redirect(url_for('vacations.list_vacations'))