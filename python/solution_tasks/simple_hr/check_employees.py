from app import create_app, db
from app.models import Employee

app = create_app()
with app.app_context():
    print(f'Number of employees: {Employee.query.count()}')
    employees = Employee.query.limit(5).all()
    for emp in employees:
        print(f'{emp.id}: {emp.full_name} ({emp.email})')