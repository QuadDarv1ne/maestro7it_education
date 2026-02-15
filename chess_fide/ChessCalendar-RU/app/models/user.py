from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import re
import bleach


class User(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_regular_user = db.Column(db.Boolean, default=True)  # Regular users who can subscribe to notifications
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime, index=True)
    is_active = db.Column(db.Boolean, default=True, index=True)
    api_key = db.Column(db.String(64), unique=True, nullable=True, index=True)
    
    # Composite indexes for common query patterns
    __table_args__ = (
        db.Index('idx_username_active', 'username', 'is_active'),
        db.Index('idx_email_active', 'email', 'is_active'),
        db.Index('idx_created_active', 'created_at', 'is_active'),
    )

    def __init__(self, username, email, password, is_admin=False, is_regular_user=True):
        self.username = username
        self.email = email
        self.set_password(password)
        self.is_admin = is_admin
        self.is_regular_user = is_regular_user
        self.generate_api_key()

    def set_password(self, password):
        """Установить хэш пароля"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Проверить пароль"""
        return check_password_hash(self.password_hash, password)

    def generate_api_key(self):
        """Сгенерировать API ключ"""
        self.api_key = secrets.token_urlsafe(32)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_admin': self.is_admin,
            'is_regular_user': self.is_regular_user,
            'created_at': self.created_at.isoformat(),
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'is_active': self.is_active
        }

    def __repr__(self):
        return f'<User {self.username}>'
    
    def validate(self):
        """Валидация данных пользователя"""
        errors = []
        
        # Sanitize inputs
        self.sanitize_fields()
        
        # Проверка имени пользователя
        if not self.username or len(self.username.strip()) == 0:
            errors.append("Имя пользователя не может быть пустым")
        elif len(self.username) > 80:
            errors.append("Имя пользователя слишком длинное (максимум 80 символов)")
        elif not re.match(r'^[A-Za-z0-9_-]+$', self.username):
            errors.append("Имя пользователя может содержать только буквы, цифры, дефисы и подчеркивания")
        
        # Проверка email
        if not self.email or len(self.email.strip()) == 0:
            errors.append("Email не может быть пустым")
        elif len(self.email) > 120:
            errors.append("Email слишком длинный (максимум 120 символов)")
        elif not re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', self.email):
            errors.append("Недопустимый формат email")
        
        # Проверка API ключа
        if self.api_key and len(self.api_key) > 64:
            errors.append("API ключ слишком длинный (максимум 64 символа)")
        
        return errors
    
    def sanitize_fields(self):
        """Sanitize input fields to prevent XSS"""
        if self.username:
            self.username = bleach.clean(self.username, strip=True)
        if self.email:
            self.email = bleach.clean(self.email, strip=True)