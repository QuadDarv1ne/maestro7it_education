from app import create_app
from app.forms import VacationForm

app = create_app()
with app.app_context():
    form = VacationForm()
    print('Number of employee choices:', len(form.employee_id.choices))
    print('First few choices:', list(form.employee_id.choices)[:3])