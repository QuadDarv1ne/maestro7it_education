from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.models import Vacation, Employee
from app.forms import VacationForm
from app.utils.notifications import notify_vacation_created
from app.utils.audit import log_vacation_create
from app.utils.excel_pdf_export import ExcelExporter
from app import db
from datetime import datetime, date, timedelta
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
        from datetime import timedelta
        today = date.today()
        year = request.args.get('year', type=int, default=today.year)
        month = request.args.get('month', type=int, default=today.month)
        
        # Get all vacations for the selected month
        start_date = date(year, month, 1)
        end_date = date(year, month, monthrange(year, month)[1])
        
        # Загружаем отпуска с подгрузкой связанных сотрудников
        vacations = Vacation.query.options(
            db.joinedload(Vacation.employee)
        ).filter(
            Vacation.start_date <= end_date,
            Vacation.end_date >= start_date,
            Vacation.status == 'approved'  # Показываем только одобренные отпуска
        ).all()
        
        logger.info(f"Found {len(vacations)} approved vacations for {year}-{month:02d}")
        
        # Create a dictionary to store vacations by date
        vacation_calendar = {}
        for vacation in vacations:
            current_date = max(vacation.start_date, start_date)
            end_range = min(vacation.end_date, end_date)
            
            # Используем timedelta вместо fromordinal
            while current_date <= end_range:
                if current_date not in vacation_calendar:
                    vacation_calendar[current_date] = []
                vacation_calendar[current_date].append(vacation)
                current_date = current_date + timedelta(days=1)
        
        logger.info(f"Calendar has {len(vacation_calendar)} days with vacations")
        
        return render_template('vacations/calendar.html', 
                             vacation_calendar=vacation_calendar,
                             year=year, 
                             month=month,
                             start_date=start_date,
                             end_date=end_date,
                             date=date)  # Pass the date function to the template
    except Exception as e:
        logger.error(f"Error loading vacation calendar: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        flash('Ошибка при загрузке календаря отпусков', 'error')
        return redirect(url_for('main.index'))

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_vacation():
    form = VacationForm()
    try:
        # Log form initialization
        logger.debug(f"Vacation form initialized with {len(form.employee_id.choices)} employee choices")
        
        if form.validate_on_submit():
            # Create new vacation
            vacation = Vacation()
            vacation.employee_id = form.employee_id.data
            vacation.start_date = form.start_date.data
            vacation.end_date = form.end_date.data
            vacation.type = form.type.data
            vacation.status = 'approved'  # Автоматически одобряем для отображения в календаре
            
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
        
        # Log form choices for debugging
        logger.debug(f"Employee choices in form: {form.employee_id.choices}")
        logger.debug(f"Number of employee choices: {len(form.employee_id.choices)}")
        
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

@bp.route('/debug/calendar-data')
@login_required
def debug_calendar_data():
    """Debug endpoint to check vacation data"""
    try:
        today = date.today()
        year = request.args.get('year', type=int, default=today.year)
        month = request.args.get('month', type=int, default=today.month)
        
        start_date = date(year, month, 1)
        end_date = date(year, month, monthrange(year, month)[1])
        
        # Все отпуска
        all_vacations = Vacation.query.filter(
            Vacation.start_date <= end_date,
            Vacation.end_date >= start_date
        ).all()
        
        # Одобренные отпуска
        approved_vacations = Vacation.query.filter(
            Vacation.start_date <= end_date,
            Vacation.end_date >= start_date,
            Vacation.status == 'approved'
        ).all()
        
        result = {
            'period': f'{year}-{month:02d}',
            'date_range': f'{start_date} to {end_date}',
            'total_vacations': len(all_vacations),
            'approved_vacations': len(approved_vacations),
            'all_vacation_details': [],
            'approved_vacation_details': []
        }
        
        for v in all_vacations:
            result['all_vacation_details'].append({
                'id': v.id,
                'employee': v.employee.full_name if v.employee else 'Unknown',
                'start_date': str(v.start_date),
                'end_date': str(v.end_date),
                'status': v.status,
                'type': v.type
            })
        
        for v in approved_vacations:
            result['approved_vacation_details'].append({
                'id': v.id,
                'employee': v.employee.full_name if v.employee else 'Unknown',
                'start_date': str(v.start_date),
                'end_date': str(v.end_date),
                'type': v.type
            })
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:id>/approve', methods=['POST'])
@login_required
def approve_vacation(id):
    """Одобрить отпуск"""
    try:
        vacation = Vacation.query.get_or_404(id)
        vacation.approve()
        db.session.commit()
        
        # Уведомление сотруднику
        if vacation.employee:
            flash(f'Отпуск для {vacation.employee.full_name} одобрен', 'success')
        
        return redirect(request.referrer or url_for('vacations.list_vacations'))
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error approving vacation {id}: {str(e)}")
        flash('Ошибка при одобрении отпуска', 'error')
        return redirect(url_for('vacations.list_vacations'))

@bp.route('/<int:id>/reject', methods=['POST'])
@login_required
def reject_vacation(id):
    """Отклонить отпуск"""
    try:
        vacation = Vacation.query.get_or_404(id)
        notes = request.form.get('notes', '')
        vacation.reject(notes)
        db.session.commit()
        
        # Уведомление сотруднику
        if vacation.employee:
            flash(f'Отпуск для {vacation.employee.full_name} отклонен', 'warning')
        
        return redirect(request.referrer or url_for('vacations.list_vacations'))
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error rejecting vacation {id}: {str(e)}")
        flash('Ошибка при отклонении отпуска', 'error')
        return redirect(url_for('vacations.list_vacations'))

@bp.route('/export/excel')
@login_required
def export_vacations_excel():
    """Экспорт отпусков в Excel"""
    try:
        vacations = Vacation.query.all()
        return ExcelExporter.export_vacations(vacations)
    except Exception as e:
        logger.error(f"Error exporting vacations to Excel: {str(e)}")
        flash(f'Ошибка при экспорте в Excel: {str(e)}', 'error')
        return redirect(url_for('vacations.list_vacations'))