try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

from app.models import Employee, Department, Position
from app import db
from datetime import datetime
import chardet
import csv
import logging

# Set up logging
logger = logging.getLogger(__name__)

def detect_encoding(filepath):
    """Detect the encoding of a CSV file"""
    try:
        with open(filepath, 'rb') as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            return result['encoding']
    except Exception as e:
        logger.error(f"Error detecting encoding: {str(e)}")
        # Fallback to utf-8
        return 'utf-8'

def import_employees_from_csv_fallback(filepath):
    """Import employees from CSV file using standard CSV module"""
    report = {
        'imported': 0,
        'skipped': 0,
        'errors': [],
        'details': [],
        'progress': 0  # Add progress tracking
    }
    
    try:
        # Detect encoding
        encoding = detect_encoding(filepath)
        logger.info(f"Detected encoding: {encoding}")
        
        # Read CSV file to get total rows for progress tracking
        with open(filepath, 'r', encoding=encoding) as f:
            total_rows = sum(1 for line in f) - 1  # Subtract 1 for header
        
        # Read CSV file
        with open(filepath, 'r', encoding=encoding) as f:
            reader = csv.DictReader(f)
            
            # Validate required columns
            required_columns = ['full_name', 'email', 'employee_id', 'hire_date', 'department', 'position']
            fieldnames = reader.fieldnames if reader.fieldnames else []
            missing_columns = [col for col in required_columns if col not in fieldnames]
            
            if missing_columns:
                raise ValueError(f"Отсутствуют обязательные столбцы: {', '.join(missing_columns)}")
            
            # Batch processing for better performance
            batch_size = 100
            batch = []
            processed_rows = 0
            
            for index, row in enumerate(reader):
                try:
                    processed_rows += 1
                    # Update progress
                    report['progress'] = int((processed_rows / total_rows) * 100) if total_rows > 0 else 0
                    
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
                    if not row['full_name'] or not row['email'] or not row['employee_id']:
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
                    
                    batch.append(emp)
                    report['imported'] += 1
                    report['details'].append(f"Строка {index+1}: Импортирован сотрудник {row['full_name']}")
                    
                    # Process batch
                    if len(batch) >= batch_size:
                        db.session.add_all(batch)
                        batch = []
                        
                except Exception as e:
                    error_msg = f"Строка {index+1}: Ошибка при импорте сотрудника {row.get('full_name', 'Unknown')}: {str(e)}"
                    report['errors'].append(error_msg)
                    report['details'].append(error_msg)
                    logger.error(error_msg)
                    continue
            
            # Process remaining batch
            if batch:
                db.session.add_all(batch)
        
        db.session.commit()
        report['progress'] = 100  # Complete
        logger.info(f"CSV import completed: {report['imported']} imported, {report['skipped']} skipped, {len(report['errors'])} errors")
        return report
        
    except Exception as e:
        db.session.rollback()
        error_msg = f"Ошибка при импорте из CSV: {str(e)}"
        logger.error(error_msg)
        report['progress'] = -1  # Error state
        raise Exception(error_msg)

def import_employees_from_csv(filepath):
    """Import employees from CSV file with error handling"""
    report = {
        'imported': 0,
        'skipped': 0,
        'errors': [],
        'details': [],
        'progress': 0  # Add progress tracking
    }
    
    if not PANDAS_AVAILABLE:
        # Fallback to standard CSV module
        logger.info("Pandas not available, using fallback CSV import")
        return import_employees_from_csv_fallback(filepath)
    
    try:
        import pandas as pd
        # Detect encoding
        encoding = detect_encoding(filepath)
        logger.info(f"Detected encoding: {encoding}")
        
        # Read CSV file
        df = pd.read_csv(filepath, encoding=encoding)
        
        # Validate required columns
        required_columns = ['full_name', 'email', 'employee_id', 'hire_date', 'department', 'position']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            raise ValueError(f"Отсутствуют обязательные столбцы: {', '.join(missing_columns)}")
        
        # Batch processing for better performance
        batch_size = 100
        batch = []
        total_rows = len(df)
        
        for index, row in df.iterrows():
            try:
                # Update progress
                report['progress'] = int(((index + 1) / total_rows) * 100)
                
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
                if not row['full_name'] or not row['email'] or not row['employee_id']:
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
                
                batch.append(emp)
                report['imported'] += 1
                report['details'].append(f"Строка {index+1}: Импортирован сотрудник {row['full_name']}")
                
                # Process batch
                if len(batch) >= batch_size:
                    db.session.add_all(batch)
                    batch = []
                    
            except Exception as e:
                error_msg = f"Строка {index+1}: Ошибка при импорте сотрудника {row.get('full_name', 'Unknown')}: {str(e)}"
                report['errors'].append(error_msg)
                report['details'].append(error_msg)
                logger.error(error_msg)
                continue
        
        # Process remaining batch
        if batch:
            db.session.add_all(batch)
        
        db.session.commit()
        report['progress'] = 100  # Complete
        logger.info(f"CSV import completed: {report['imported']} imported, {report['skipped']} skipped, {len(report['errors'])} errors")
        return report
        
    except Exception as e:
        db.session.rollback()
        error_msg = f"Ошибка при импорте из CSV: {str(e)}"
        logger.error(error_msg)
        report['progress'] = -1  # Error state
        raise Exception(error_msg)