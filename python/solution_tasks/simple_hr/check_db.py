from app import create_app, db
from app.models import Department, Position

app = create_app()
with app.app_context():
    print('Departments:', Department.query.count())
    print('Positions:', Position.query.count())
    
    # List departments
    print("\nDepartments:")
    for dept in Department.query.all():
        print(f"  {dept.id}: {dept.name}")
    
    # List positions
    print("\nPositions:")
    for pos in Position.query.all():
        print(f"  {pos.id}: {pos.title}")