from flask import Blueprint, render_template, request, redirect, url_for, flash, Response
from flask_login import login_required
from app.models import Employee, Department, Position, Vacation, Order
from app import db
from datetime import datetime, date
import pandas as pd
import io

bp = Blueprint('reports', __name__)

@bp.route('/')
@login_required
def generate_report():
    # Get report parameters
    report_type = request.args.get('type', 'employees')
    department_id = request.args.get('department_id', type=int)
    
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
        # Get vacations for current month
        today = date.today()
        start_date = date(today.year, today.month, 1)
        if today.month == 12:
            end_date = date(today.year + 1, 1, 1)
        else:
            end_date = date(today.year, today.month + 1, 1)
        
        vacations = Vacation.query.filter(
            Vacation.start_date >= start_date,
            Vacation.start_date < end_date
        ).all()
        
        return render_template('reports/vacations.html', vacations=vacations)
    
    elif report_type == 'departments':
        departments = Department.query.all()
        return render_template('reports/departments.html', departments=departments)
    
    else:
        flash('Неверный тип отчета')
        return redirect(url_for('reports.generate_report'))

@bp.route('/export')
@login_required
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
        employees = query.all()
        
        # Create DataFrame
        data = []
        for emp in employees:
            data.append({
                'Табельный номер': emp.employee_id,
                'ФИО': emp.full_name,
                'Email': emp.email,
                'Подразделение': emp.department.name,
                'Должность': emp.position.title,
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
    
    else:
        flash('Неверный тип отчета для экспорта')
        return redirect(url_for('reports.generate_report'))