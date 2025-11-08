import pandas as pd
from app.models import Employee, Department, Position
from app import db
from datetime import datetime
import chardet
import io

def detect_encoding(filepath):
    """Detect the encoding of a CSV file"""
    with open(filepath, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        return result['encoding']

def import_employees_from_csv(filepath):
    """Import employees from CSV file with error handling"""
    report = {
        'imported': 0,
        'skipped': 0,
        'errors': [],
        'details': []
    }
    
    try:
        # Detect encoding
        encoding = detect_encoding(filepath)
        
        # Read CSV file
        df = pd.read_csv(filepath, encoding=encoding)
        
        # Validate required columns
        required_columns = ['full_name', 'email', 'employee_id', 'hire_date', 'department', 'position']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            raise ValueError(f"Отсутствуют обязательные столбцы: {', '.join(missing_columns)}")
        
        for index, row in df.iterrows():
            try:
                # Check if employee already exists by email or employee_id
                existing_emp = Employee.query.filter(
                    db.or_(
                        Employee.email == row['email'],
                        Employee.employee_id == row['employee_id']
                    )
                ).first()
                
                if existing_emp:
                    if existing_emp.email == row['email']:
                        report['skipped'] += 1
                        report['details'].append(f"Строка {index+1}: Сотрудник с email {row['email']} уже существует, пропущен")
                    else:
                        report['skipped'] += 1
                        report['details'].append(f"Строка {index+1}: Сотрудник с табельным номером {row['employee_id']} уже существует, пропущен")
                    continue
                
                # Validate required fields
                if pd.isna(row['full_name']) or pd.isna(row['email']) or pd.isna(row['employee_id']):
                    report['errors'].append(f"Строка {index+1}: Отсутствуют обязательные данные")
                    continue
                
                # Get or create department
                dept = Department.query.filter_by(name=row['department']).first()
                if not dept:
                    dept = Department(name=row['department'])
                    db.session.add(dept)
                    db.session.flush()  # Get ID without committing

                # Get or create position
                pos = Position.query.filter_by(title=row['position']).first()
                if not pos:
                    pos = Position(title=row['position'])
                    db.session.add(pos)
                    db.session.flush()  # Get ID without committing

                # Parse date
                try:
                    hire_date = datetime.strptime(str(row['hire_date']), '%Y-%m-%d').date()
                except ValueError:
                    report['errors'].append(f"Строка {index+1}: Неверный формат даты для сотрудника {row['full_name']}, пропущен")
                    continue

                # Create employee
                emp = Employee()
                emp.full_name = row['full_name']
                emp.email = row['email']
                emp.employee_id = row['employee_id']
                emp.hire_date = hire_date
                emp.department_id = dept.id
                emp.position_id = pos.id
                emp.status = 'active'
                
                db.session.add(emp)
                report['imported'] += 1
                report['details'].append(f"Строка {index+1}: Импортирован сотрудник {row['full_name']}")
                
            except Exception as e:
                error_msg = f"Строка {index+1}: Ошибка при импорте сотрудника {row.get('full_name', 'Unknown')}: {str(e)}"
                report['errors'].append(error_msg)
                report['details'].append(error_msg)
                continue
        
        db.session.commit()
        return report
        
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Ошибка при импорте из CSV: {str(e)}")

def import_employees_from_csv_string(csv_string):
    """Import employees from CSV string with error handling"""
    report = {
        'imported': 0,
        'skipped': 0,
        'errors': [],
        'details': []
    }
    
    try:
        # Read CSV from string
        df = pd.read_csv(io.StringIO(csv_string))
        
        # Validate required columns
        required_columns = ['full_name', 'email', 'employee_id', 'hire_date', 'department', 'position']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            raise ValueError(f"Отсутствуют обязательные столбцы: {', '.join(missing_columns)}")
        
        for index, row in df.iterrows():
            try:
                # Check if employee already exists
                existing_emp = Employee.query.filter_by(email=row['email']).first()
                if existing_emp:
                    report['skipped'] += 1
                    report['details'].append(f"Строка {index+1}: Сотрудник с email {row['email']} уже существует, пропущен")
                    continue
                
                # Validate required fields
                if pd.isna(row['full_name']) or pd.isna(row['email']) or pd.isna(row['employee_id']):
                    report['errors'].append(f"Строка {index+1}: Отсутствуют обязательные данные")
                    continue
                
                # Get or create department
                dept = Department.query.filter_by(name=row['department']).first()
                if not dept:
                    dept = Department(name=row['department'])
                    db.session.add(dept)
                    db.session.flush()  # Get ID without committing

                # Get or create position
                pos = Position.query.filter_by(title=row['position']).first()
                if not pos:
                    pos = Position(title=row['position'])
                    db.session.add(pos)
                    db.session.flush()  # Get ID without committing

                # Parse date
                try:
                    hire_date = datetime.strptime(str(row['hire_date']), '%Y-%m-%d').date()
                except ValueError:
                    report['errors'].append(f"Строка {index+1}: Неверный формат даты для сотрудника {row['full_name']}, пропущен")
                    continue

                # Create employee
                emp = Employee()
                emp.full_name = row['full_name']
                emp.email = row['email']
                emp.employee_id = row['employee_id']
                emp.hire_date = hire_date
                emp.department_id = dept.id
                emp.position_id = pos.id
                emp.status = 'active'
                
                db.session.add(emp)
                report['imported'] += 1
                report['details'].append(f"Строка {index+1}: Импортирован сотрудник {row['full_name']}")
                
            except Exception as e:
                error_msg = f"Строка {index+1}: Ошибка при импорте сотрудника {row.get('full_name', 'Unknown')}: {str(e)}"
                report['errors'].append(error_msg)
                report['details'].append(error_msg)
                continue
        
        db.session.commit()
        return report
        
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Ошибка при импорте из CSV: {str(e)}")