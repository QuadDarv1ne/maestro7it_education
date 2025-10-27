from app import create_app, db
from app.models import User, Department, Position, Employee, Order, Vacation
from datetime import date

app = create_app()
app.app_context().push()

# Очистка (опционально)
db.drop_all()
db.create_all()

# Пользователи
admin = User(username='admin', role='admin')
admin.set_password('admin')
hr = User(username='hr', role='hr')
hr.set_password('hr')
db.session.add_all([admin, hr])

# Подразделения
depts = [Department(name=name) for name in ['IT', 'HR', 'Finance', 'Marketing', 'Support']]
db.session.add_all(depts)

# Должности
positions = [Position(title=title) for title in ['Developer', 'HR Manager', 'Accountant', 'Designer', 'Support Specialist', 'Team Lead', 'Analyst']]
db.session.add_all(positions)

db.session.commit()

# Сотрудники (30+)
employees = []
for i in range(1, 35):
    emp = Employee(
        full_name=f'Сотрудник {i}',
        email=f'user{i}@example.com',
        employee_id=f'ID{i:04}',
        hire_date=date(2023, 1, 15) if i % 2 else date(2024, 3, 10),
        department_id=(i % 5) + 1,
        position_id=(i % 7) + 1,
        status='active'
    )
    employees.append(emp)
db.session.add_all(employees)
db.session.commit()

# Приказы и отпуска — аналогично (по 10+ шт.)

print("Тестовые данные загружены!")