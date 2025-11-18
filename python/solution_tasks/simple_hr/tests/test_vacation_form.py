from flask import Flask, render_template_string
from app import create_app
from app.forms import VacationForm

# Create a simple test app
test_app = Flask(__name__)
test_app.config['SECRET_KEY'] = 'test-key'

@test_app.route('/test-form')
def test_form():
    form = VacationForm()
    return f"""
    <h1>Test Vacation Form</h1>
    <p>Number of employee choices: {len(form.employee_id.choices)}</p>
    <p>First few choices: {list(form.employee_id.choices)[:3]}</p>
    <form method="POST">
        {{ form.hidden_tag() }}
        <div>
            {{ form.employee_id.label }}
            {{ form.employee_id() }}
        </div>
        <div>
            {{ form.type.label }}
            {{ form.type() }}
        </div>
        <div>
            {{ form.start_date.label }}
            {{ form.start_date() }}
        </div>
        <div>
            {{ form.end_date.label }}
            {{ form.end_date() }}
        </div>
        <div>
            {{ form.submit() }}
        </div>
    </form>
    """

if __name__ == '__main__':
    test_app.run(debug=True, port=5001)