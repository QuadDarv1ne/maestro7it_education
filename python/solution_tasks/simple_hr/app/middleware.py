"""
Middleware для мониторинга производительности приложения
"""
from flask import request, g
from time import time
import logging
from functools import wraps

logger = logging.getLogger(__name__)

class PerformanceMonitoring:
    """Middleware для отслеживания времени выполнения запросов"""
    
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        """Инициализация middleware"""
        app.before_request(self.before_request)
        app.after_request(self.after_request)
    
    @staticmethod
    def before_request():
        """Сохранить время начала запроса"""
        g.start_time = time()
        g.request_id = f"{request.remote_addr}_{int(time() * 1000)}"
    
    @staticmethod
    def after_request(response):
        """Логировать время выполнения запроса"""
        if hasattr(g, 'start_time'):
            elapsed = time() - g.start_time
            
            # Логируем медленные запросы (> 1 секунды)
            if elapsed > 1.0:
                logger.warning(
                    f"[{g.request_id}] Slow request: {request.method} {request.path} "
                    f"took {elapsed:.2f}s | User: {getattr(g, 'current_user', 'Anonymous')}"
                )
            
            # Добавляем заголовки с информацией о производительности
            response.headers['X-Request-Duration'] = f"{elapsed:.4f}s"
            response.headers['X-Request-ID'] = g.request_id
        
        return response


class RequestLogger:
    """Middleware для логирования всех запросов"""
    
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        """Инициализация middleware"""
        app.before_request(self.log_request)
        app.after_request(self.log_response)
        app.teardown_request(self.log_teardown)
    
    @staticmethod
    def log_request():
        """Логировать входящий запрос"""
        logger.info(
            f"[{g.request_id}] Request: {request.method} {request.path} "
            f"from {request.remote_addr} | User-Agent: {request.user_agent}"
        )
        
        # Логируем параметры запроса (без конфиденциальных данных)
        if request.args:
            safe_args = {k: v for k, v in request.args.items() if k not in ['password', 'token']}
            if safe_args:
                logger.debug(f"[{g.request_id}] Query params: {safe_args}")
    
    @staticmethod
    def log_response(response):
        """Логировать ответ"""
        status_code = response.status_code
        log_level = logging.INFO
        
        # Определяем уровень логирования по статус коду
        if status_code >= 500:
            log_level = logging.ERROR
        elif status_code >= 400:
            log_level = logging.WARNING
        
        logger.log(
            log_level,
            f"[{g.request_id}] Response: {status_code} for "
            f"{request.method} {request.path} | Size: {response.content_length or 0} bytes"
        )
        return response
    
    @staticmethod
    def log_teardown(exception=None):
        """Логировать ошибки при завершении запроса"""
        if exception is not None:
            logger.error(
                f"[{g.request_id}] Request teardown error: {exception}",
                exc_info=True
            )


class SecurityHeaders:
    """Middleware для добавления заголовков безопасности"""
    
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        """Инициализация middleware"""
        app.after_request(self.add_security_headers)
    
    @staticmethod
    def add_security_headers(response):
        """Добавить заголовки безопасности"""
        # Защита от XSS
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        
        # Content Security Policy
        response.headers['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "img-src 'self' data: https:; "
            "font-src 'self' data: https://cdn.jsdelivr.net;"
        )
        
        # Strict Transport Security (только для HTTPS)
        if request.is_secure:
            response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        
        return response


class RateLimiting:
    """Middleware для ограничения частоты запросов"""
    
    def __init__(self, app=None, max_requests=100, window=60):
        self.app = app
        self.max_requests = max_requests  # Максимум запросов
        self.window = window  # Временное окно в секундах
        self.requests = {}  # IP -> [(timestamp, count)]
        
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        """Инициализация middleware"""
        app.before_request(self.check_rate_limit)
    
    def check_rate_limit(self):
        """Проверить лимит запросов"""
        from flask import abort
        
        ip = request.remote_addr
        now = time()
        
        # Очищаем старые записи
        if ip in self.requests:
            self.requests[ip] = [
                (timestamp, count) for timestamp, count in self.requests[ip]
                if now - timestamp < self.window
            ]
        else:
            self.requests[ip] = []
        
        # Подсчитываем количество запросов
        total_requests = sum(count for _, count in self.requests[ip])
        
        if total_requests >= self.max_requests:
            logger.warning(f"Rate limit exceeded for IP: {ip}")
            abort(429)  # Too Many Requests
        
        # Добавляем текущий запрос
        self.requests[ip].append((now, 1))


def log_sql_queries(app):
    """Логирование SQL запросов"""
    from sqlalchemy import event
    from sqlalchemy.engine import Engine
    
    @event.listens_for(Engine, "before_cursor_execute")
    def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        conn.info.setdefault('query_start_time', []).append(time())
        if app.debug:
            logger.debug(f"SQL Query: {statement}")
    
    @event.listens_for(Engine, "after_cursor_execute")
    def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        total_time = time() - conn.info['query_start_time'].pop()
        if total_time > 0.1:  # Логируем медленные запросы (> 100ms)
            logger.warning(f"Slow SQL query ({total_time:.4f}s): {statement[:200]}")


def setup_middleware(app):
    """Настройка всех middleware"""
    # Основные middleware
    PerformanceMonitoring(app)
    SecurityHeaders(app)
    
    # RequestLogger только в production или при включенном логировании
    if not app.debug or app.config.get('ENABLE_REQUEST_LOGGING', False):
        RequestLogger(app)
    
    # Rate limiting в production
    if not app.debug:
        RateLimiting(app, max_requests=100, window=60)
    
    # SQL query logging
    if app.debug or app.config.get('ENABLE_SQL_LOGGING', False):
        log_sql_queries(app)
