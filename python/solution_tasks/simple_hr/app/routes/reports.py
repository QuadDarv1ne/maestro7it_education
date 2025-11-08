from flask import Blueprint, render_template, request, redirect, url_for, flash, Response
from flask_login import login_required
from app.models import Employee, Department, Position, Vacation, Order
from app.utils.reports import generate_employee_report, generate_department_report, generate_vacation_report, generate_hiring_report, export_report_to_csv, export_report_to_excel, get_employee_statistics, get_vacation_statistics, generate_vacation_calendar, generate_turnover_report, generate_performance_report, generate_salary_report
from app.utils.decorators import reports_access_required
from app import db
from datetime import datetime, date
import io
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Try to import pandas
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

bp = Blueprint('reports', __name__)

@bp.route('/')
@login_required
@reports_access_required
def generate_report():
    try:
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
            # Generate hiring report only if period is specified
            period_months = request.args.get('period_months', type=int)
            hiring_data = None
            if period_months:
                hiring_data = generate_hiring_report(period_months)
            return render_template('reports/hiring.html', hiring_data=hiring_data, period_months=period_months or 12)
        
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
        
        elif report_type == 'performance_report':
            # Generate performance report
            report_data = generate_performance_report()
            return render_template('reports/performance.html', report_data=report_data)
        
        elif report_type == 'salary_report':
            # Generate salary report
            report_data = generate_salary_report()
            return render_template('reports/salary.html', report_data=report_data)
        
        else:
            flash('Неверный тип отчета')
            return redirect(url_for('reports.generate_report'))
    except Exception as e:
        logger.error(f"Error in generate_report: {str(e)}")
        flash('Ошибка при генерации отчета')
        return redirect(url_for('reports.generate_report'))

@bp.route('/export')
@login_required
@reports_access_required
def export_report():
    try:
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
            
            # Create CSV
            output = io.StringIO()
            
            # Try to use pandas if available, otherwise use manual CSV creation
            try:
                import pandas as pd
                df = pd.DataFrame(data)
                df.to_csv(output, index=False, encoding='utf-8')
            except ImportError:
                # Manual CSV creation
                if data:
                    # Write header
                    headers = list(data[0].keys())
                    output.write(','.join(['"{}"'.format(h) for h in headers]) + '\n')
                    
                    # Write data rows
                    for row in data:
                        values = [str(row[h]) for h in headers]
                        output.write(','.join(['"{}"'.format(v) for v in values]) + '\n')
            
            csv_data = output.getvalue()
            
            return Response(
                csv_data,
                mimetype='text/csv',
                headers={'Content-Disposition': f'attachment; filename=employee_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'}
            )
        
        else:
            flash('Неверный тип отчета')
            return redirect(url_for('reports.generate_report'))
    except Exception as e:
        logger.error(f"Error in export_report: {str(e)}")
        flash('Ошибка при экспорте отчета')
        return redirect(url_for('reports.generate_report'))