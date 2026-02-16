"""
Улучшенная система безопасности и аутентификации
"""
import hashlib
import secrets
import time
from datetime import datetime, timedelta
from functools import wraps
from typing import Optional, Dict, Any
import logging
from flask import request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

logger = logging.getLogger(__name__)

# Argon2 для более безопасного хеширования паролей
ph = PasswordHasher(
    time_cost=2,
    memory_cost=65536,
    parallelism=2,
    hash_len=32,
    salt_len=16
)


class PasswordManager:
    """Менеджер паролей с Argon2"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Хеширование пароля с использованием Argon2
        
        Args:
            password: Пароль в открытом виде
        
        Returns:
            Хеш пароля
        """
        try:
            return ph.hash(password)
        except Exception as e:
            logger.error(f"Password hashing error: {e}")
            # Fallback на werkzeug
            return generate_password_hash(password, method='pbkdf2:sha256')
    
    @staticmethod
    def verify_password(password_hash: str, password: str) -> bool:
        """
        Проверка пароля
        
        Args:
            password_hash: Хеш пароля
            password: Пароль в открытом виде
        
        Returns:
            True если пароль верный
        """
        try:
            # Пробуем Argon2
            ph.verify(password_hash, password)
            
            # Проверяем, нужно ли обновить хеш
            if ph.check_needs_rehash(password_hash):
                logger.info("Password hash needs rehashing")
            
            return True
        except VerifyMismatchError:
            return False
        except Exception:
            # Fallback на werkzeug
            return check_password_hash(password_hash, password)
    
    @staticmethod
    def validate_password_strength(password: str) -> tuple[bool, str]:
        """
        Проверка надежности пароля
        
        Args:
            password: Пароль для проверки
        
        Returns:
            (is_valid, error_message)
        """
        if len(password) < 8:
            return False, "Пароль должен содержать минимум 8 символов"
        
        if len(password) > 128:
            return False, "Пароль слишком длинный (максимум 128 символов)"
        
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
        
        if not (has_upper and has_lower and has_digit):
            return False, "Пароль должен содержать заглавные и строчные буквы, цифры"
        
        # Проверка на распространенные пароли
        common_passwords = ['password', '12345678', 'qwerty', 'admin', 'letmein']
        if password.lower() in common_passwords:
            return False, "Пароль слишком простой"
        
        return True, ""


class RateLimiter:
    """Rate limiting для защиты от брутфорса"""
    
    def __init__(self, redis_client=None):
        self.redis = redis_client
        self.memory_store = {}  # Fallback если Redis недоступен
    
    def is_rate_limited(self, key: str, max_attempts: int = 5, 
                       window: int = 300) -> tuple[bool, int]:
        """
        Проверка rate limit
        
        Args:
            key: Ключ (например, IP или username)
            max_attempts: Максимум попыток
            window: Окно времени в секундах
        
        Returns:
            (is_limited, remaining_attempts)
        """
        if self.redis:
            return self._check_redis(key, max_attempts, window)
        else:
            return self._check_memory(key, max_attempts, window)
    
    def _check_redis(self, key: str, max_attempts: int, 
                    window: int) -> tuple[bool, int]:
        """Проверка через Redis"""
        try:
            rate_key = f"rate_limit:{key}"
            current = self.redis.get(rate_key)
            
            if current is None:
                self.redis.setex(rate_key, window, 1)
                return False, max_attempts - 1
            
            current = int(current)
            if current >= max_attempts:
                ttl = self.redis.ttl(rate_key)
                logger.warning(f"Rate limit exceeded for {key}, TTL: {ttl}s")
                return True, 0
            
            self.redis.incr(rate_key)
            return False, max_attempts - current - 1
        
        except Exception as e:
            logger.error(f"Redis rate limit error: {e}")
            return self._check_memory(key, max_attempts, window)
    
    def _check_memory(self, key: str, max_attempts: int, 
                     window: int) -> tuple[bool, int]:
        """Проверка через память (fallback)"""
        now = time.time()
        
        if key not in self.memory_store:
            self.memory_store[key] = {'count': 1, 'reset_at': now + window}
            return False, max_attempts - 1
        
        data = self.memory_store[key]
        
        # Сброс если окно истекло
        if now > data['reset_at']:
            self.memory_store[key] = {'count': 1, 'reset_at': now + window}
            return False, max_attempts - 1
        
        if data['count'] >= max_attempts:
            return True, 0
        
        data['count'] += 1
        return False, max_attempts - data['count']
    
    def reset(self, key: str):
        """Сброс счетчика"""
        if self.redis:
            self.redis.delete(f"rate_limit:{key}")
        else:
            self.memory_store.pop(key, None)


class JWTManager:
    """Менеджер JWT токенов"""
    
    @staticmethod
    def generate_token(user_id: int, username: str, is_admin: bool = False,
                      expires_in: int = 3600) -> str:
        """
        Генерация JWT токена
        
        Args:
            user_id: ID пользователя
            username: Имя пользователя
            is_admin: Флаг администратора
            expires_in: Время жизни в секундах
        
        Returns:
            JWT токен
        """
        payload = {
            'user_id': user_id,
            'username': username,
            'is_admin': is_admin,
            'exp': datetime.utcnow() + timedelta(seconds=expires_in),
            'iat': datetime.utcnow(),
            'jti': secrets.token_urlsafe(16)  # JWT ID для отзыва
        }
        
        secret = current_app.config.get('SECRET_KEY')
        return jwt.encode(payload, secret, algorithm='HS256')
    
    @staticmethod
    def generate_refresh_token(user_id: int) -> str:
        """
        Генерация refresh токена
        
        Args:
            user_id: ID пользователя
        
        Returns:
            Refresh токен
        """
        payload = {
            'user_id': user_id,
            'type': 'refresh',
            'exp': datetime.utcnow() + timedelta(days=30),
            'iat': datetime.utcnow(),
            'jti': secrets.token_urlsafe(16)
        }
        
        secret = current_app.config.get('SECRET_KEY')
        return jwt.encode(payload, secret, algorithm='HS256')
    
    @staticmethod
    def verify_token(token: str) -> Optional[Dict[str, Any]]:
        """
        Проверка JWT токена
        
        Args:
            token: JWT токен
        
        Returns:
            Payload токена или None
        """
        try:
            secret = current_app.config.get('SECRET_KEY')
            payload = jwt.decode(token, secret, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("Token expired")
            return None
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid token: {e}")
            return None
    
    @staticmethod
    def is_token_revoked(jti: str, redis_client=None) -> bool:
        """
        Проверка, отозван ли токен
        
        Args:
            jti: JWT ID
            redis_client: Redis клиент
        
        Returns:
            True если токен отозван
        """
        if not redis_client:
            return False
        
        try:
            return redis_client.exists(f"revoked_token:{jti}") > 0
        except Exception as e:
            logger.error(f"Token revocation check error: {e}")
            return False
    
    @staticmethod
    def revoke_token(jti: str, expires_in: int, redis_client=None):
        """
        Отозвать токен
        
        Args:
            jti: JWT ID
            expires_in: Время до истечения токена
            redis_client: Redis клиент
        """
        if not redis_client:
            logger.warning("Cannot revoke token: Redis not available")
            return
        
        try:
            redis_client.setex(f"revoked_token:{jti}", expires_in, "1")
            logger.info(f"Token revoked: {jti}")
        except Exception as e:
            logger.error(f"Token revocation error: {e}")


class TwoFactorAuth:
    """Двухфакторная аутентификация (TOTP)"""
    
    @staticmethod
    def generate_secret() -> str:
        """Генерация секрета для 2FA"""
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def generate_qr_code_url(username: str, secret: str, 
                            issuer: str = "Chess Calendar RU") -> str:
        """
        Генерация URL для QR кода
        
        Args:
            username: Имя пользователя
            secret: Секрет 2FA
            issuer: Название приложения
        
        Returns:
            otpauth:// URL
        """
        import urllib.parse
        
        params = {
            'secret': secret,
            'issuer': issuer,
            'algorithm': 'SHA1',
            'digits': 6,
            'period': 30
        }
        
        query = urllib.parse.urlencode(params)
        return f"otpauth://totp/{issuer}:{username}?{query}"
    
    @staticmethod
    def verify_totp(secret: str, token: str, window: int = 1) -> bool:
        """
        Проверка TOTP кода
        
        Args:
            secret: Секрет 2FA
            token: Код от пользователя
            window: Окно времени (количество периодов)
        
        Returns:
            True если код верный
        """
        try:
            import pyotp
            totp = pyotp.TOTP(secret)
            return totp.verify(token, valid_window=window)
        except ImportError:
            logger.error("pyotp not installed, 2FA unavailable")
            return False
        except Exception as e:
            logger.error(f"TOTP verification error: {e}")
            return False


class AuditLogger:
    """Логирование административных действий"""
    
    def __init__(self, db):
        self.db = db
    
    def log_action(self, user_id: int, action: str, resource: str,
                   resource_id: Optional[int] = None, 
                   details: Optional[Dict] = None,
                   ip_address: Optional[str] = None):
        """
        Логирование действия
        
        Args:
            user_id: ID пользователя
            action: Действие (create, update, delete, login, etc.)
            resource: Ресурс (tournament, user, etc.)
            resource_id: ID ресурса
            details: Дополнительные детали
            ip_address: IP адрес
        """
        from app.models.audit_log import AuditLog
        
        log_entry = AuditLog(
            user_id=user_id,
            action=action,
            resource=resource,
            resource_id=resource_id,
            details=details,
            ip_address=ip_address or request.remote_addr,
            user_agent=request.headers.get('User-Agent'),
            timestamp=datetime.utcnow()
        )
        
        self.db.session.add(log_entry)
        self.db.session.commit()
        
        logger.info(f"Audit: user={user_id} action={action} resource={resource} id={resource_id}")
    
    def get_user_actions(self, user_id: int, limit: int = 100):
        """Получить действия пользователя"""
        from app.models.audit_log import AuditLog
        
        return AuditLog.query.filter_by(user_id=user_id)\
            .order_by(AuditLog.timestamp.desc())\
            .limit(limit)\
            .all()
    
    def get_resource_history(self, resource: str, resource_id: int):
        """Получить историю ресурса"""
        from app.models.audit_log import AuditLog
        
        return AuditLog.query.filter_by(
            resource=resource,
            resource_id=resource_id
        ).order_by(AuditLog.timestamp.desc()).all()


# Декораторы
def require_auth(f):
    """Декоратор для требования аутентификации"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'error': 'No token provided'}), 401
        
        if token.startswith('Bearer '):
            token = token[7:]
        
        payload = JWTManager.verify_token(token)
        if not payload:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        # Проверка отзыва токена
        from app.utils.cache_manager import cache_manager
        if JWTManager.is_token_revoked(payload.get('jti'), cache_manager.redis_client):
            return jsonify({'error': 'Token has been revoked'}), 401
        
        # Добавляем данные пользователя в request
        request.current_user = payload
        
        return f(*args, **kwargs)
    return decorated_function


def require_admin(f):
    """Декоратор для требования прав администратора"""
    @wraps(f)
    @require_auth
    def decorated_function(*args, **kwargs):
        if not request.current_user.get('is_admin'):
            return jsonify({'error': 'Admin access required'}), 403
        
        return f(*args, **kwargs)
    return decorated_function


def rate_limit(max_attempts: int = 5, window: int = 300):
    """
    Декоратор для rate limiting
    
    Args:
        max_attempts: Максимум попыток
        window: Окно времени в секундах
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            from app.utils.cache_manager import cache_manager
            
            # Используем IP адрес как ключ
            key = request.remote_addr
            
            limiter = RateLimiter(cache_manager.redis_client)
            is_limited, remaining = limiter.is_rate_limited(key, max_attempts, window)
            
            if is_limited:
                return jsonify({
                    'error': 'Too many requests',
                    'retry_after': window
                }), 429
            
            # Добавляем заголовки rate limit
            response = f(*args, **kwargs)
            if isinstance(response, tuple):
                response_obj, status_code = response[0], response[1]
            else:
                response_obj, status_code = response, 200
            
            if hasattr(response_obj, 'headers'):
                response_obj.headers['X-RateLimit-Limit'] = str(max_attempts)
                response_obj.headers['X-RateLimit-Remaining'] = str(remaining)
            
            return response_obj, status_code
        
        return decorated_function
    return decorator


def audit_log(action: str, resource: str):
    """
    Декоратор для автоматического логирования действий
    
    Args:
        action: Действие
        resource: Ресурс
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            from app import db
            
            # Выполняем функцию
            result = f(*args, **kwargs)
            
            # Логируем действие
            if hasattr(request, 'current_user'):
                user_id = request.current_user.get('user_id')
                resource_id = kwargs.get('id') or kwargs.get('tournament_id') or kwargs.get('user_id')
                
                audit_logger = AuditLogger(db)
                audit_logger.log_action(
                    user_id=user_id,
                    action=action,
                    resource=resource,
                    resource_id=resource_id
                )
            
            return result
        
        return decorated_function
    return decorator
