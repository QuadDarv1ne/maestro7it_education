from app import create_app, db
from app.models import User, Department, Position, Employee, Order, Vacation
from datetime import date

app = create_app()
app.app_context().push()

# Очистка (опционально)
db.drop_all()
db.create_all()

# Пользователи
admin = User()
admin.username = 'admin'
admin.email = 'admin@example.com'
admin.role = 'admin'
admin.set_password('admin')

hr = User()
hr.username = 'hr'
hr.email = 'hr@example.com'
hr.role = 'hr'
hr.set_password('hr')

db.session.add(admin)
db.session.add(hr)

# Подразделения
depts = []
for name in ['IT', 'HR', 'Finance', 'Marketing', 'Support']:
    dept = Department()
    dept.name = name
    depts.append(dept)
db.session.add_all(depts)

# Должности
positions = []
for title in ['Developer', 'HR Manager', 'Accountant', 'Designer', 'Support Specialist', 'Team Lead', 'Analyst']:
    pos = Position()
    pos.title = title
    positions.append(pos)
db.session.add_all(positions)

db.session.commit()

# Сотрудники (30+)
employees = []
for i in range(1, 35):
    emp = Employee()
    emp.full_name = f'Сотрудник {i}'
    emp.email = f'user{i}@example.com'
    emp.employee_id = f'ID{i:04}'
    emp.hire_date = date(2023, 1, 15) if i % 2 else date(2024, 3, 10)
    emp.department_id = (i % 5) + 1
    emp.position_id = (i % 7) + 1
    emp.status = 'active'
    employees.append(emp)
db.session.add_all(employees)
db.session.commit()

# Приказы и отпуска — аналогично (по 10+ шт.)

print("Тестовые данные загружены!")