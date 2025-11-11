from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from datetime import datetime, timedelta
import secrets

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, index=True)  # 'admin' or 'hr'
    active = db.Column(db.Boolean, default=True, nullable=False, name='is_active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    last_login = db.Column(db.DateTime, index=True)
    
    # Поля для восстановления пароля
    reset_token = db.Column(db.String(100), unique=True, nullable=True)
    reset_token_expires = db.Column(db.DateTime, nullable=True)
    
    # Index for faster queries
    __table_args__ = (
        db.Index('idx_user_role_active', 'role', 'is_active'),
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def generate_reset_token(self):
        """Генерация токена для восстановления пароля"""
        self.reset_token = secrets.token_urlsafe(32)
        self.reset_token_expires = datetime.utcnow() + timedelta(hours=1)
        return self.reset_token
    
    def verify_reset_token(self, token):
        """Проверка токена для восстановления пароля"""
        if self.reset_token == token and self.reset_token_expires and self.reset_token_expires > datetime.utcnow():
            return True
        return False
    
    def reset_password(self, new_password):
        """Сброс пароля"""
        self.set_password(new_password)
        self.reset_token = None
        self.reset_token_expires = None
    
    def is_admin(self):
        return self.role == 'admin'
    
    def is_hr(self):
        return self.role == 'hr'
    
    def can_access_reports(self):
        return self.role in ['admin', 'hr']
    
    def can_manage_employees(self):
        return self.role in ['admin', 'hr']
    
    def can_manage_departments(self):
        return self.role in ['admin', 'hr']
    
    def can_manage_positions(self):
        return self.role in ['admin', 'hr']
    
    def can_manage_vacations(self):
        return self.role in ['admin', 'hr']
    
    def can_backup_data(self):
        return self.role == 'admin'

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    employees = db.relationship('Employee', backref='department', lazy=True)

class Position(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False, index=True)
    employees = db.relationship('Employee', backref='position', lazy=True)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    employee_id = db.Column(db.String(50), unique=True, nullable=False, index=True)  # табельный номер
    hire_date = db.Column(db.Date, nullable=False, index=True)
    status = db.Column(db.String(20), default='active', index=True)  # active, dismissed
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False, index=True)
    position_id = db.Column(db.Integer, db.ForeignKey('position.id'), nullable=False, index=True)
    
    # Index for faster queries
    __table_args__ = (
        db.Index('idx_employee_status_department', 'status', 'department_id'),
        db.Index('idx_employee_hire_date_status', 'hire_date', 'status'),
    )

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False, index=True)
    type = db.Column(db.String(20), nullable=False, index=True)  # hire, transfer, dismissal
    date_issued = db.Column(db.Date, nullable=False, index=True)
    new_department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=True)
    new_position_id = db.Column(db.Integer, db.ForeignKey('position.id'), nullable=True)
    
    # Relationships
    employee = db.relationship('Employee', backref=db.backref('orders', lazy=True))
    new_department = db.relationship('Department', foreign_keys=[new_department_id])
    new_position = db.relationship('Position', foreign_keys=[new_position_id])
    
    # Index for faster queries
    __table_args__ = (
        db.Index('idx_order_employee_type', 'employee_id', 'type'),
        db.Index('idx_order_date_type', 'date_issued', 'type'),
    )

class Vacation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False, index=True)
    start_date = db.Column(db.Date, nullable=False, index=True)
    end_date = db.Column(db.Date, nullable=False, index=True)
    type = db.Column(db.String(20), nullable=False, index=True)  # paid, unpaid, sick
    
    # Relationship
    employee = db.relationship('Employee', backref=db.backref('vacations', lazy=True))
    
    # Index for faster queries
    __table_args__ = (
        db.Index('idx_vacation_employee_dates', 'employee_id', 'start_date', 'end_date'),
        db.Index('idx_vacation_dates_type', 'start_date', 'end_date', 'type'),
    )

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    user = db.relationship('User', backref=db.backref('notifications', lazy=True))
    
    # Index for faster queries
    __table_args__ = (
        db.Index('idx_notification_user_read', 'user_id', 'is_read'),
    )

class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    action = db.Column(db.String(100), nullable=False, index=True)  # create, update, delete, login, etc.
    entity_type = db.Column(db.String(50), nullable=False, index=True)  # employee, department, etc.
    entity_id = db.Column(db.Integer, nullable=True, index=True)
    description = db.Column(db.Text, nullable=True)
    ip_address = db.Column(db.String(45), nullable=True, index=True)  # IPv4 or IPv6
    user_agent = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    user = db.relationship('User', backref=db.backref('audit_logs', lazy=True))
    
    # Index for faster queries
    __table_args__ = (
        db.Index('idx_audit_user_action', 'user_id', 'action'),
        db.Index('idx_audit_entity_type_id', 'entity_type', 'entity_id'),
        db.Index('idx_audit_created_at', 'created_at'),
    )