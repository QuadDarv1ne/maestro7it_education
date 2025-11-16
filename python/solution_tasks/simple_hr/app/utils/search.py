"""
Advanced search utilities for employees
"""
from app.models import Employee, Department, Position
from sqlalchemy import or_, and_, func
from datetime import datetime, timedelta

class EmployeeSearchEngine:
    """Advanced search and filtering for employees"""
    
    def __init__(self, query=None):
        self.query = query or Employee.query
        self.filters = []
    
    def search_text(self, text):
        """Full-text search across multiple fields"""
        if not text:
            return self
        
        search_filter = f"%{text}%"
        self.filters.append(
            or_(
                Employee.full_name.ilike(search_filter),
                Employee.email.ilike(search_filter),
                Employee.employee_id.ilike(search_filter),
                Employee.phone.ilike(search_filter) if hasattr(Employee, 'phone') else False
            )
        )
        return self
    
    def filter_by_department(self, department_id=None, department_name=None):
        """Filter by department ID or name"""
        if department_id:
            self.filters.append(Employee.department_id == department_id)
        elif department_name:
            dept = Department.query.filter(
                Department.name.ilike(f"%{department_name}%")
            ).first()
            if dept:
                self.filters.append(Employee.department_id == dept.id)
        return self
    
    def filter_by_position(self, position_id=None, position_title=None):
        """Filter by position ID or title"""
        if position_id:
            self.filters.append(Employee.position_id == position_id)
        elif position_title:
            pos = Position.query.filter(
                Position.title.ilike(f"%{position_title}%")
            ).first()
            if pos:
                self.filters.append(Employee.position_id == pos.id)
        return self
    
    def filter_by_status(self, status):
        """Filter by employment status"""
        if status:
            self.filters.append(Employee.status == status)
        return self
    
    def filter_by_hire_date_range(self, start_date=None, end_date=None):
        """Filter by hire date range"""
        if start_date:
            self.filters.append(Employee.hire_date >= start_date)
        if end_date:
            self.filters.append(Employee.hire_date <= end_date)
        return self
    
    def filter_by_hire_year(self, year):
        """Filter by hire year"""
        if year:
            start_date = datetime(year, 1, 1).date()
            end_date = datetime(year, 12, 31).date()
            self.filters.append(and_(
                Employee.hire_date >= start_date,
                Employee.hire_date <= end_date
            ))
        return self
    
    def filter_recently_hired(self, days=30):
        """Filter employees hired in the last N days"""
        cutoff_date = (datetime.now() - timedelta(days=days)).date()
        self.filters.append(Employee.hire_date >= cutoff_date)
        return self
    
    def filter_long_term_employees(self, years=5):
        """Filter employees with tenure >= N years"""
        cutoff_date = (datetime.now() - timedelta(days=years*365)).date()
        self.filters.append(Employee.hire_date <= cutoff_date)
        return self
    
    def sort_by(self, field='full_name', order='asc'):
        """Sort results by field"""
        if hasattr(Employee, field):
            attr = getattr(Employee, field)
            if order.lower() == 'desc':
                self.query = self.query.order_by(attr.desc())
            else:
                self.query = self.query.order_by(attr.asc())
        return self
    
    def execute(self, page=1, per_page=20):
        """Execute search and return paginated results"""
        if self.filters:
            self.query = self.query.filter(and_(*self.filters))
        
        return self.query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
    
    def count(self):
        """Return count of matching employees"""
        if self.filters:
            self.query = self.query.filter(and_(*self.filters))
        return self.query.count()
    
    def get_statistics(self):
        """Get statistics about search results"""
        if self.filters:
            filtered_query = self.query.filter(and_(*self.filters))
        else:
            filtered_query = self.query
        
        total_count = filtered_query.count()
        
        # Group by status
        status_stats = {}
        for status in ['active', 'inactive', 'on_leave']:
            count = filtered_query.filter(Employee.status == status).count()
            status_stats[status] = count
        
        # Group by department
        department_stats = db.session.query(
            Department.name,
            func.count(Employee.id)
        ).join(
            Employee, Employee.department_id == Department.id
        ).filter(
            *self.filters if self.filters else []
        ).group_by(
            Department.name
        ).all()
        
        return {
            'total': total_count,
            'by_status': status_stats,
            'by_department': dict(department_stats)
        }


def search_employees(
    text=None,
    department_id=None,
    position_id=None,
    status=None,
    hire_year=None,
    start_date=None,
    end_date=None,
    sort_by='full_name',
    sort_order='asc',
    page=1,
    per_page=20
):
    """
    Convenience function for advanced employee search
    
    Args:
        text: Search text for full-text search
        department_id: Filter by department ID
        position_id: Filter by position ID
        status: Filter by employment status
        hire_year: Filter by hire year
        start_date: Filter hire date >= start_date
        end_date: Filter hire date <= end_date
        sort_by: Field to sort by
        sort_order: 'asc' or 'desc'
        page: Page number for pagination
        per_page: Items per page
    
    Returns:
        Paginated query results
    """
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
    if start_date or end_date:
        engine.filter_by_hire_date_range(start_date, end_date)
    
    engine.sort_by(sort_by, sort_order)
    
    return engine.execute(page, per_page)
