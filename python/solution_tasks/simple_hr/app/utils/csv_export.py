import pandas as pd
from app.models import Employee, Department, Position
from app import db
import io

def export_employees_to_csv(encoding='utf-8'):
    """Export all employees to CSV format with specified encoding"""
    employees = Employee.query.all()
    
    # Create DataFrame
    data = []
    for emp in employees:
        data.append({
            'employee_id': emp.employee_id,
            'full_name': emp.full_name,
            'email': emp.email,
            'department': emp.department.name,
            'position': emp.position.title,
            'hire_date': emp.hire_date.strftime('%Y-%m-%d'),
            'status': emp.status
        })
    
    df = pd.DataFrame(data)
    return df

def export_employees_to_csv_string(encoding='utf-8'):
    """Export all employees to CSV string with specified encoding"""
    df = export_employees_to_csv()
    output = io.StringIO()
    df.to_csv(output, index=False, encoding=encoding)
    return output.getvalue()

def export_departments_to_csv():
    """Export all departments to CSV format"""
    departments = Department.query.all()
    
    # Create DataFrame
    data = []
    for dept in departments:
        data.append({
            'id': dept.id,
            'name': dept.name,
            'employee_count': len(dept.employees)
        })
    
    df = pd.DataFrame(data)
    return df

def export_positions_to_csv():
    """Export all positions to CSV format"""
    positions = Position.query.all()
    
    # Create DataFrame
    data = []
    for pos in positions:
        data.append({
            'id': pos.id,
            'title': pos.title,
            'employee_count': len(pos.employees)
        })
    
    df = pd.DataFrame(data)
    return df