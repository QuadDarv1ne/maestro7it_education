from app import create_app, db
from app.models import Employee
from app.forms import VacationForm

app = create_app()

with app.app_context():
    print("Testing employee loading...")

    # Check if there are employees in the database
    employees = Employee.query.all()
    print(f"Total employees: {len(employees)}")

    # Check active employees
    active_employees = Employee.query.filter_by(status='active').all()
    print(f"Active employees: {len(active_employees)}")

    # Check if we can create a form and load choices
    with app.test_request_context():
        form = VacationForm()
        print(f"Employee choices in form: {len(form.employee_id.choices)}")
        print("Employee choices:")
        for choice in form.employee_id.choices:
            print(f"  {choice}")

    # Check if there are any departments or positions
    from app.models import Department, Position
    depts = Department.query.all()
    print(f"Departments: {len(depts)}")

    positions = Position.query.all()
    print(f"Positions: {len(positions)}")