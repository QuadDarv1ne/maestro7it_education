from app import db
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import re
import bleach
import logging

logger = logging.getLogger(__name__)

# Попытка импорта Argon2, fallback на werkzeug
try:
    from argon2 import PasswordHasher
    from argon2.exceptions import VerifyMismatchError, InvalidHash
    ph = PasswordHasher(
        time_cost=2,
        memory_cost=65536,
        parallelism=2,
        hash_len=32,
        salt_len=16
    )
    USE_ARGON2 = True
    logger.info("Using Argon2 for password hashing")
except ImportError:
    USE_ARGON2 = False
    logger.warning("Argon2 not available, using werkzeug password hashing")


class User(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_regular_user = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime, index=True)
    is_active = db.Column(db.Boolean, default=True, index=True)
    api_key = db.Column(db.String(64), unique=True, nullable=True, index=True)
    failed_login_attempts = db.Column(db.Integer, default=0)
    locked_until = db.Column(db.DateTime)
    password_reset_token = db.Column(db.String(100), unique=True)
    password_reset_expires = db.Column(db.DateTime)
    # Новые поля для безопасности
    two_factor_secret = db.Column(db.String(64), nullable=True)
    two_factor_enabled = db.Column(db.Boolean, default=False)
    password_changed_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Composite indexes for common query patterns
    __table_args__ = (
        db.Index('idx_username_active', 'username', 'is_active'),
        db.Index('idx_email_active', 'email', 'is_active'),
        db.Index('idx_created_active', 'created_at', 'is_active'),
        db.Index('idx_failed_login', 'failed_login_attempts', 'locked_until'),
    )

    def __init__(self, username, email, password, is_admin=False, is_regular_user=True):
        self.username = username
        self.email = email
        self.set_password(password)
        self.is_admin = is_admin
        self.is_regular_user = is_regular_user
        self.generate_api_key()

    def set_password(self, password):
        """Установить хэш пароля с использованием Argon2 или werkzeug"""
        # Validate password strength
        is_valid, error_msg = self.validate_password_strength(password)
        if not is_valid:
            raise ValueError(error_msg)
        
        if USE_ARGON2:
            try:
                self.password_hash = ph.hash(password)
                logger.info(f"Password hashed with Argon2 for user {self.username}")
            except Exception as e:
                logger.error(f"Argon2 hashing failed: {e}, falling back to werkzeug")
                self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')
        else:
            self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')
        
        self.password_changed_at = datetime.utcnow()

    def check_password(self, password):
        """Проверить пароль с автоматической миграцией на Argon2"""
        # Check if account is locked
        if self.is_locked():
            logger.warning(f"Login attempt for locked account: {self.username}")
            return False
        
        is_valid = False
        
        # Попытка проверки с Argon2
        if USE_ARGON2 and self.password_hash.startswith('$argon2'):
            try:
                ph.verify(self.password_hash, password)
                is_valid = True
                
                # Проверка, нужно ли обновить хеш
                if ph.check_needs_rehash(self.password_hash):
                    logger.info(f"Rehashing password for user {self.username}")
                    self.password_hash = ph.hash(password)
                    self.password_changed_at = datetime.utcnow()
                    
            except (VerifyMismatchError, InvalidHash):
                is_valid = False
        else:
            # Fallback на werkzeug или миграция со старого хеша
            is_valid = check_password_hash(self.password_hash, password)
            
            # Автоматическая миграция на Argon2
            if is_valid and USE_ARGON2 and not self.password_hash.startswith('$argon2'):
                logger.info(f"Migrating password hash to Argon2 for user {self.username}")
                self.password_hash = ph.hash(password)
                self.password_changed_at = datetime.utcnow()
        
        if is_valid:
            # Reset failed attempts on successful login
            self.failed_login_attempts = 0
            self.locked_until = None
            self.last_login = datetime.utcnow()
            logger.info(f"Successful login for user {self.username}")
        else:
            # Increment failed attempts
            self.failed_login_attempts += 1
            logger.warning(f"Failed login attempt {self.failed_login_attempts} for user {self.username}")
            
            # Lock account after 5 failed attempts
            if self.failed_login_attempts >= 5:
                self.locked_until = datetime.utcnow() + timedelta(minutes=30)
                logger.warning(f"Account locked for user {self.username} until {self.locked_until}")
        
        return is_valid
    
    def is_locked(self):
        """Check if account is currently locked"""
        from datetime import datetime
        if self.locked_until and datetime.utcnow() < self.locked_until:
            return True
        elif self.locked_until and datetime.utcnow() >= self.locked_until:
            # Unlock account if lock period has expired
            self.failed_login_attempts = 0
            self.locked_until = None
        return False
    
    def validate_password_strength(self, password):
        """Validate password meets security requirements"""
        if len(password) < 8:
            return False, "Пароль должен содержать минимум 8 символов"
        if len(password) > 128:
            return False, "Пароль слишком длинный (максимум 128 символов)"
        if not re.search(r'[A-Z]', password):
            return False, "Пароль должен содержать хотя бы одну заглавную букву"
        if not re.search(r'[a-z]', password):
            return False, "Пароль должен содержать хотя бы одну строчную букву"
        if not re.search(r'\d', password):
            return False, "Пароль должен содержать хотя бы одну цифру"
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False, "Пароль должен содержать хотя бы один специальный символ"
        
        # Проверка на распространенные пароли
        common_passwords = ['password', '12345678', 'qwerty', 'admin', 'letmein', 'password123']
        if password.lower() in common_passwords:
            return False, "Пароль слишком простой, используйте более сложный"
        
        return True, ""

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