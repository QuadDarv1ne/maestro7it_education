import pandas as pd
from app.models import Employee, Department, Position
from app import db
from datetime import datetime
import chardet

def detect_encoding(filepath):
    """Detect the encoding of a CSV file"""
    with open(filepath, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        return result['encoding']

def import_employees_from_csv(filepath):
    """Import employees from CSV file with error handling"""
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
        
        imported_count = 0
        
        for _, row in df.iterrows():
            try:
                # Check if employee already exists
                existing_emp = Employee.query.filter_by(email=row['email']).first()
                if existing_emp:
                    print(f"Сотрудник с email {row['email']} уже существует, пропущен")
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
                    print(f"Неверный формат даты для сотрудника {row['full_name']}, пропущен")
                    continue

                # Create employee
                emp = Employee(
                    full_name=row['full_name'],
                    email=row['email'],
                    employee_id=row['employee_id'],
                    hire_date=hire_date,
                    department_id=dept.id,
                    position_id=pos.id,
                    status='active'
                )
                db.session.add(emp)
                imported_count += 1
                
            except Exception as e:
                print(f"Ошибка при импорте сотрудника {row.get('full_name', 'Unknown')}: {str(e)}")
                db.session.rollback()
                continue
        
        db.session.commit()
        return imported_count
        
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Ошибка при импорте из CSV: {str(e)}")