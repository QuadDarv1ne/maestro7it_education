from app import create_app, db
from app.models import Employee
from app.forms import VacationForm

app = create_app()

with app.app_context():
    print("Detailed employee loading test...")
    
    # Check all employees and their status
    employees = Employee.query.all()
    print(f"Total employees in database: {len(employees)}")
    
    active_count = 0
    for emp in employees:
        print(f"  ID: {emp.id}, Name: {emp.full_name}, Status: {emp.status}, Email: {emp.email}")
        if emp.status == 'active':
            active_count += 1
    
    print(f"Active employees: {active_count}")
    
    # Test form creation within request context
    with app.test_request_context():
        form = VacationForm()
        print(f"\nForm employee choices count: {len(form.employee_id.choices)}")
        print("Form employee choices:")
        for choice in form.employee_id.choices:
            print(f"  {choice}")
        
        # Test form rendering
        print("\nForm rendering test:")
        try:
            rendered = form.employee_id()
            print("Employee field rendered successfully")
            print(f"Rendered HTML snippet: {rendered[:100]}...")
        except Exception as e:
            print(f"Error rendering employee field: {e}")