import pandas as pd
from app.models import Employee, Department, Position
from app import db
from datetime import datetime

def import_employees_from_csv(filepath):
    df = pd.read_csv(filepath)
    for _, row in df.iterrows():
        dept = Department.query.filter_by(name=row['department']).first()
        if not dept:
            dept = Department(name=row['department'])
            db.session.add(dept)
            db.session.commit()

        pos = Position.query.filter_by(title=row['position']).first()
        if not pos:
            pos = Position(title=row['position'])
            db.session.add(pos)
            db.session.commit()

        emp = Employee(
            full_name=row['full_name'],
            email=row['email'],
            employee_id=row['employee_id'],
            hire_date=datetime.strptime(row['hire_date'], '%Y-%m-%d').date(),
            department_id=dept.id,
            position_id=pos.id,
            status='active'
        )
        db.session.add(emp)
    db.session.commit()