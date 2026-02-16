"""
Middleware для улучшенной безопасности приложения
"""
from flask import request, jsonify, g
from functools import wraps
import time
import logging
from datetime import datetime, timedelta
from collections import defaultdict
import re

logger = logging.getLogger(__name__)


class SecurityMiddleware:
    """Middleware для обработки событий безопасности"""
    
    def __init__(self, app=None):
        self.app = app
        self.suspicious_patterns = [
            r'<script',
            r'javascript:',
            r'onerror=',
            r'onload=',
            r'\.\./\.\.',
            r'union.*select',
            r'drop.*table',
        ]
        self.rate_limits = defaultdict(list)
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Инициализация middleware"""
        app.before_request(self.before_request)
        app.after_request(self.after_request)
        logger.info("Security middleware initialized")
    
    def before_request(self):
        """Обработка запроса перед выполнением"""
        g.start_time = time.time()
        
        # Проверка на подозрительные паттерны
        if self.check_suspicious_patterns():
            logger.warning(f"Suspicious pattern detected from {request.remote_addr}")
            return jsonify({
                'error': 'Suspicious request detected',
                'message': 'Your request has been blocked for security reasons'
            }), 403
        
        # Проверка rate limiting
        if not self.check_rate_limit():
            logger.warning(f"Rate limit exceeded for {request.remote_addr}")
            return jsonify({
                'error': 'Rate limit exceeded',
                'message': 'Too many requests. Please try again later.'
            }), 429
    
    def after_request(self, response):
        """Обработка ответа после выполнения"""
        # Добавление заголовков безопасности
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Логирование времени выполнения
        if hasattr(g, 'start_time'):
            elapsed = time.time() - g.start_time
            if elapsed > 1.0:  # Медленные запросы
                logger.warning(
                    f"Slow request: {request.method} {request.path} "
                    f"took {elapsed:.2f}s from {request.remote_addr}"
                )
        
        return response
    
    def check_suspicious_patterns(self):
        """Проверка на подозрительные паттерны в запросе"""
        # Проверка URL
        url = request.url.lower()
        for pattern in self.suspicious_patterns:
            if re.search(pattern, url, re.IGNORECASE):
                return True
        
        # Проверка параметров
        for key, value in request.args.items():
            if isinstance(value, str):
                for pattern in self.suspicious_patterns:
                    if re.search(pattern, value, re.IGNORECASE):
                        return True
        
        # Проверка тела запроса (если JSON)
        if request.is_json:
            try:
                data = str(request.get_json())
                for pattern in self.suspicious_patterns:
                    if re.search(pattern, data, re.IGNORECASE):
                        return True
            except:
                pass
        
        return False
    
    def check_rate_limit(self):
        """Проверка rate limiting"""
        ip = request.remote_addr
        now = datetime.now()
        
        # Очистка старых записей
        self.rate_limits[ip] = [
            timestamp for timestamp in self.rate_limits[ip]
            if now - timestamp < timedelta(minutes=1)
        ]
        
        # Проверка лимита (100 запросов в минуту)
        if len(self.rate_limits[ip]) >= 100:
            return False
        
        # Добавление текущего запроса
        self.rate_limits[ip].append(now)
        return True


def require_api_key(f):
    """Декоратор для проверки API ключа"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        
        if not api_key:
            return jsonify({
                'error': 'API key required',
                'message': 'Please provide an API key in X-API-Key header'
            }), 401
        
        # Проверка API ключа в базе данных
        from app.models.user import User
        user = User.query.filter_by(api_key=api_key, is_active=True).first()
        
        if not user:
            logger.warning(f"Invalid API key attempt from {request.remote_addr}")
            return jsonify({
                'error': 'Invalid API key',
                'message': 'The provided API key is invalid or inactive'
            }), 401
        
        # Сохранение пользователя в контексте
        g.current_user = user
        
        return f(*args, **kwargs)
    
    return decorated_function


def require_admin(f):
    """Декоратор для проверки прав администратора"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not hasattr(g, 'current_user'):
            return jsonify({
                'error': 'Authentication required',
                'message': 'Please authenticate first'
            }), 401
        
        if not g.current_user.is_admin:
            logger.warning(
                f"Unauthorized admin access attempt by user {g.current_user.id} "
                f"from {request.remote_addr}"
            )
            return jsonify({
                'error': 'Admin access required',
                'message': 'You do not have permission to access this resource'
            }), 403
        
        return f(*args, **kwargs)
    
    return decorated_function


class AuditLogger:
    """Логирование событий аудита"""
    
    @staticmethod
    def log_event(user_id, action, resource, resource_id=None, details=None):
        """Логирование события аудита"""
        from app.models.audit_log import AuditLog
        from app import db
        
        try:
            log_entry = AuditLog(
                user_id=user_id,
                action=action,
                resource=resource,
                resource_id=resource_id,
                details=details,
                ip_address=request.remote_addr,
                user_agent=request.headers.get('User-Agent', '')[:255]
            )
            
            db.session.add(log_entry)
            db.session.commit()
            
            logger.info(
                f"Audit: user={user_id} action={action} "
                f"resource={resource} id={resource_id}"
            )
        except Exception as e:
            logger.error(f"Failed to log audit event: {e}")
            db.session.rollback()
    
    @staticmethod
    def log_security_event(level, event_type, details):
        """Логирование события безопасности"""
        logger.log(
            logging.WARNING if level == 'medium' else logging.ERROR,
            f"Security event: {event_type} - {details} from {request.remote_addr}"
        )


# Глобальный экземпляр
security_middleware = SecurityMiddleware()
audit_logger = AuditLogger()
