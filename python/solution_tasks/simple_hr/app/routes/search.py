from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from app.utils.search import EmployeeSearchEngine, search_employees
from app.models import Department, Position
from app import db

bp = Blueprint('search', __name__, url_prefix='/search')

@bp.route('/employees')
@login_required
def advanced_search():
    """Advanced employee search page"""
    departments = Department.query.all()
    positions = Position.query.all()
    
    return render_template('search/advanced.html',
                         departments=departments,
                         positions=positions)

@bp.route('/employees/api', methods=['GET', 'POST'])
@login_required
def api_search():
    """API endpoint for advanced search"""
    # Get search parameters
    text = request.args.get('text') or request.form.get('text')
    department_id = request.args.get('department_id', type=int)
    position_id = request.args.get('position_id', type=int)
    status = request.args.get('status')
    hire_year = request.args.get('hire_year', type=int)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    sort_by = request.args.get('sort_by', 'full_name')
    sort_order = request.args.get('sort_order', 'asc')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    # Parse dates
    if start_date:
        from datetime import datetime
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    if end_date:
        from datetime import datetime
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    
    # Execute search
    results = search_employees(
        text=text,
        department_id=department_id,
        position_id=position_id,
        status=status,
        hire_year=hire_year,
        start_date=start_date,
        end_date=end_date,
        sort_by=sort_by,
        sort_order=sort_order,
        page=page,
        per_page=per_page
    )
    
    # Get statistics
    engine = EmployeeSearchEngine()
    if text:
        engine.search_text(text)
    if department_id:
        engine.filter_by_department(department_id=department_id)
    if position_id:
        engine.filter_by_position(position_id=position_id)
    if status:
        engine.filter_by_status(status)
    if hire_year:
        engine.filter_by_hire_year(hire_year)
    
    stats = engine.get_statistics()
    
    # Format response
    employees_data = []
    for emp in results.items:
        employees_data.append({
            'id': emp.id,
            'full_name': emp.full_name,
            'email': emp.email,
            'employee_id': emp.employee_id,
            'department': emp.department.name if emp.department else None,
            'position': emp.position.title if emp.position else None,
            'status': emp.status,
            'hire_date': emp.hire_date.isoformat() if emp.hire_date else None
        })
    
    return jsonify({
        'employees': employees_data,
        'pagination': {
            'page': results.page,
            'per_page': results.per_page,
            'total': results.total,
            'pages': results.pages,
            'has_next': results.has_next,
            'has_prev': results.has_prev
        },
        'statistics': stats
    })

@bp.route('/autocomplete')
@login_required
def autocomplete():
    """Autocomplete endpoint for search suggestions"""
    query = request.args.get('q', '')
    field = request.args.get('field', 'full_name')
    limit = request.args.get('limit', 10, type=int)
    
    if not query or len(query) < 2:
        return jsonify([])
    
    from app.models import Employee
    
    if field == 'full_name':
        results = db.session.query(Employee.full_name).filter(
            Employee.full_name.ilike(f'%{query}%')
        ).distinct().limit(limit).all()
    elif field == 'email':
        results = db.session.query(Employee.email).filter(
            Employee.email.ilike(f'%{query}%')
        ).distinct().limit(limit).all()
    elif field == 'employee_id':
        results = db.session.query(Employee.employee_id).filter(
            Employee.employee_id.ilike(f'%{query}%')
        ).distinct().limit(limit).all()
    else:
        return jsonify([])
    
    suggestions = [r[0] for r in results if r[0]]
    return jsonify(suggestions)
