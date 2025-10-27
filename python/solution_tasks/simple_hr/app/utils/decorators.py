from functools import wraps
from flask import abort
from flask_login import current_user

def admin_required(f):
    """Декоратор для проверки прав администратора"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            abort(403)  # Доступ запрещен
        return f(*args, **kwargs)
    return decorated_function

def hr_required(f):
    """Декоратор для проверки прав HR"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not (current_user.is_admin() or current_user.is_hr()):
            abort(403)  # Доступ запрещен
        return f(*args, **kwargs)
    return decorated_function

def reports_access_required(f):
    """Декоратор для проверки доступа к отчетам"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.can_access_reports():
            abort(403)  # Доступ запрещен
        return f(*args, **kwargs)
    return decorated_function

def employee_management_required(f):
    """Декоратор для проверки прав на управление сотрудниками"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.can_manage_employees():
            abort(403)  # Доступ запрещен
        return f(*args, **kwargs)
    return decorated_function

def department_management_required(f):
    """Декоратор для проверки прав на управление подразделениями"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.can_manage_departments():
            abort(403)  # Доступ запрещен
        return f(*args, **kwargs)
    return decorated_function

def position_management_required(f):
    """Декоратор для проверки прав на управление должностями"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.can_manage_positions():
            abort(403)  # Доступ запрещен
        return f(*args, **kwargs)
    return decorated_function

def vacation_management_required(f):
    """Декоратор для проверки прав на управление отпусками"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.can_manage_vacations():
            abort(403)  # Доступ запрещен
        return f(*args, **kwargs)
    return decorated_function

def backup_access_required(f):
    """Декоратор для проверки прав на резервное копирование"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.can_backup_data():
            abort(403)  # Доступ запрещен
        return f(*args, **kwargs)
    return decorated_function