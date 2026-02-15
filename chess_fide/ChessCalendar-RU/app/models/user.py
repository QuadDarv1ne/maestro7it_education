from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import secrets


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_regular_user = db.Column(db.Boolean, default=True)  # Regular users who can subscribe to notifications
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    api_key = db.Column(db.String(64), unique=True, nullable=True, index=True)

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