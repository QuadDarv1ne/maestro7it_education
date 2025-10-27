from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from datetime import datetime, timedelta
import secrets

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'admin' or 'hr'
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Поля для восстановления пароля
    reset_token = db.Column(db.String(100), unique=True, nullable=True)
    reset_token_expires = db.Column(db.DateTime, nullable=True)

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
        if self.reset_token == token and self.reset_token_expires > datetime.utcnow():
            return True
        return False
    
    def reset_password(self, new_password):
        """Сброс пароля"""
        self.set_password(new_password)
        self.reset_token = None
        self.reset_token_expires = None

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    employees = db.relationship('Employee', backref='department', lazy=True)

class Position(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    employees = db.relationship('Employee', backref='position', lazy=True)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    employee_id = db.Column(db.String(50), unique=True, nullable=False)  # табельный номер
    hire_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='active')  # active, dismissed
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    position_id = db.Column(db.Integer, db.ForeignKey('position.id'), nullable=False)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # hire, transfer, dismissal
    date_issued = db.Column(db.Date, nullable=False)
    new_department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=True)
    new_position_id = db.Column(db.Integer, db.ForeignKey('position.id'), nullable=True)

class Vacation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    type = db.Column(db.String(20), nullable=False)  # paid, unpaid, sick