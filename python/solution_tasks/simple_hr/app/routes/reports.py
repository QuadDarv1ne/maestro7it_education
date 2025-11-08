from flask import Blueprint, render_template, request, redirect, url_for, flash, Response
from flask_login import login_required
from app.models import Employee, Department, Position, Vacation, Order
from app.utils.reports import generate_employee_report, generate_department_report, generate_vacation_report, generate_hiring_report, export_report_to_csv, export_report_to_excel, get_employee_statistics, get_vacation_statistics, generate_vacation_calendar, generate_turnover_report
from app.utils.decorators import reports_access_required
from app import db
from datetime import datetime, date
import pandas as pd
import io

bp = Blueprint('reports', __name__)

@bp.route('/')
@login_required
@reports_access_required
def generate_report():
    # Get report parameters
    report_type = request.args.get('type', 'index')
    
    # If no specific report type requested, show report index
    if report_type == 'index':
        return render_template('reports/index.html')
    department_id = request.args.get('department_id', type=int)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Base query
    query = db.session.query(Employee)
    
    # Filter by department if specified
    if department_id:
        query = query.filter(Employee.department_id == department_id)
    
    # Get data based on report type
    if report_type == 'employees':
        employees = query.all()
        departments = Department.query.all()
        return render_template('reports/employees.html', employees=employees, departments=departments, selected_department=department_id)
    
    elif report_type == 'vacations':
        # Build vacation query
        vacation_query = Vacation.query
        
        # Filter by date range if specified
        if start_date:
            vacation_query = vacation_query.filter(Vacation.start_date >= datetime.strptime(start_date, '%Y-%m-%d').date())
        if end_date:
            vacation_query = vacation_query.filter(Vacation.end_date <= datetime.strptime(end_date, '%Y-%m-%d').date())
        
        vacations = vacation_query.all()
        departments = Department.query.all()
        return render_template('reports/vacations.html', vacations=vacations, departments=departments, 
                             selected_department=department_id, start_date=start_date, end_date=end_date)
    
    elif report_type == 'departments':
        departments = Department.query.all()
        return render_template('reports/departments.html', departments=departments)
    
    elif report_type == 'employee_statistics':
        # Get statistics using utility functions
        stats = get_employee_statistics()
        return render_template('reports/statistics.html', **stats)
    
    elif report_type == 'vacation_statistics':
        # Get vacation statistics
        stats = get_vacation_statistics()
        return render_template('reports/vacation_statistics.html', **stats)
    
    elif report_type == 'hiring_report':
        # Generate hiring report
        period_months = request.args.get('period_months', 12, type=int)
        hiring_data = generate_hiring_report(period_months)
        return render_template('reports/hiring.html', hiring_data=hiring_data, period_months=period_months)
    
    elif report_type == 'detailed_employee_report':
        # Generate detailed employee report
        report_data = generate_employee_report()
        return render_template('reports/detailed_employees.html', report_data=report_data)
    
    elif report_type == 'department_report':
        # Generate department report
        report_data = generate_department_report()
        return render_template('reports/department_report.html', report_data=report_data)
    
    elif report_type == 'vacation_calendar':
        # Generate vacation calendar for a month
        year = request.args.get('year', type=int)
        month = request.args.get('month', type=int)
        
        # If no year/month specified, use current month
        if not year or not month:
            from datetime import date
            today = date.today()
            year = today.year
            month = today.month
        
        calendar_data = generate_vacation_calendar(year, month)
        
        # Get month name in Russian
        month_names = {
            1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель',
            5: 'Май', 6: 'Июнь', 7: 'Июль', 8: 'Август',
            9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь'
        }
        
        return render_template('reports/vacation_calendar.html', 
                             calendar_data=calendar_data,
                             year=year,
                             month=month,
                             month_name=month_names.get(month, ''))
    
    elif report_type == 'turnover_report':
        # Generate turnover report
        period_days = request.args.get('period_days', 365, type=int)
        turnover_data = generate_turnover_report(period_days)
        return render_template('reports/turnover.html', 
                             turnover_data=turnover_data,
                             period_days=period_days)
    
    else:
        flash('Неверный тип отчета')
        return redirect(url_for('reports.generate_report'))

@bp.route('/export')
@login_required
@reports_access_required
def export_report():
    # Get report parameters
    report_type = request.args.get('type', 'employees')
    department_id = request.args.get('department_id', type=int)
    
    # Base query
    query = db.session.query(Employee)
    
    # Filter by department if specified
    if department_id:
        query = query.filter(Employee.department_id == department_id)
    
    # Generate report based on type
    if report_type == 'employees':
        # Join with Department and Position to access related data
        employees = db.session.query(Employee, Department, Position)\
            .join(Department, Employee.department_id == Department.id)\
            .join(Position, Employee.position_id == Position.id)\
            .all()
        
        # Create DataFrame
        data = []
        for emp, dept, pos in employees:
            data.append({
                'Табельный номер': emp.employee_id,
                'ФИО': emp.full_name,
                'Email': emp.email,
                'Подразделение': dept.name,
                'Должность': pos.title,
                'Дата приема': emp.hire_date.strftime('%d.%m.%Y'),
                'Статус': emp.status
            })
        
        df = pd.DataFrame(data)
        
        # Create CSV
        output = io.StringIO()
        df.to_csv(output, index=False, encoding='utf-8')
        csv_data = output.getvalue()
        
        # Return CSV response
        return Response(
            csv_data,
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment; filename=employees_report.csv'}
        )
    
    elif report_type == 'hiring_report':
        # Get period parameter
        period_months = request.args.get('period_months', 12, type=int)
        
        # Generate hiring report data
        hiring_data = generate_hiring_report(period_months)
        
        # Create DataFrame
        data = []
        for month_data in hiring_data:
            for emp in month_data['employees']:
                data.append({
                    'Месяц': month_data['month'],
                    'ФИО': emp['name'],
                    'Подразделение': emp['department'],
                    'Должность': emp['position'],
                    'Дата приема': emp['hire_date'].strftime('%d.%m.%Y')
                })
        
        df = pd.DataFrame(data)
        
        # Create CSV
        output = io.StringIO()
        df.to_csv(output, index=False, encoding='utf-8')
        csv_data = output.getvalue()
        
        # Return CSV response
        return Response(
            csv_data,
            mimetype='text/csv',
            headers={'Content-Disposition': f'attachment; filename=hiring_report_{period_months}_months.csv'}
        )
    
    elif report_type == 'vacation_calendar':
        # Get year and month parameters
        year = request.args.get('year', type=int)
        month = request.args.get('month', type=int)
        
        # If no year/month specified, use current month
        if not year or not month:
            from datetime import date
            today = date.today()
            year = today.year
            month = today.month
        
        # Generate vacation calendar data
        calendar_data = generate_vacation_calendar(year, month)
        
        # Create DataFrame
        data = []
        for day_data in calendar_data:
            if day_data['vacations']:
                for vacation in day_data['vacations']:
                    data.append({
                        'Дата': day_data['date'].strftime('%d.%m.%Y'),
                        'Сотрудник': vacation['employee_name'],
                        'Подразделение': vacation['department'],
                        'Должность': vacation['position'],
                        'Тип отпуска': vacation['type']
                    })
            else:
                data.append({
                    'Дата': day_data['date'].strftime('%d.%m.%Y'),
                    'Сотрудник': '',
                    'Подразделение': '',
                    'Должность': '',
                    'Тип отпуска': 'Нет отпусков'
                })
        
        df = pd.DataFrame(data)
        
        # Create CSV
        output = io.StringIO()
        df.to_csv(output, index=False, encoding='utf-8')
        csv_data = output.getvalue()
        
        # Return CSV response
        from calendar import month_name
        month_names_ru = {
            1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель',
            5: 'Май', 6: 'Июнь', 7: 'Июль', 8: 'Август',
            9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь'
        }
        
        return Response(
            csv_data,
            mimetype='text/csv',
            headers={'Content-Disposition': f'attachment; filename=vacation_calendar_{year}_{month}_{month_names_ru.get(month, month)}.csv'}
        )
    
    elif report_type == 'turnover_report':
        # Get period parameter
        period_days = request.args.get('period_days', 365, type=int)
        
        # Generate turnover report data
        turnover_data = generate_turnover_report(period_days)
        
        # Create DataFrame
        data = []
        for month_data in turnover_data:
            # Add hired employees
            for emp in month_data['hired_employees']:
                data.append({
                    'Месяц': month_data['month'],
                    'Тип': 'Принят',
                    'Сотрудник': emp['name'],
                    'Подразделение': emp['department'],
                    'Должность': emp['position'],
                    'Дата': emp['hire_date'].strftime('%d.%m.%Y')
                })
            
            # Add dismissed employees
            for emp in month_data['dismissed_employees']:
                data.append({
                    'Месяц': month_data['month'],
                    'Тип': 'Уволен',
                    'Сотрудник': emp['employee_name'],
                    'Подразделение': emp['department'],
                    'Должность': emp['position'],
                    'Дата': emp['dismissal_date'].strftime('%d.%m.%Y')
                })
        
        df = pd.DataFrame(data)
        
        # Create CSV
        output = io.StringIO()
        df.to_csv(output, index=False, encoding='utf-8')
        csv_data = output.getvalue()
        
        # Return CSV response
        return Response(
            csv_data,
            mimetype='text/csv',
            headers={'Content-Disposition': f'attachment; filename=turnover_report_{period_days}_days.csv'}
        )
    
    else:
        flash('Неверный тип отчета для экспорта')
        return redirect(url_for('reports.generate_report'))