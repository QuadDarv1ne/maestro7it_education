"""
Middleware для мониторинга производительности приложения
"""
from flask import request, g
from time import time
import logging

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
    
    @staticmethod
    def after_request(response):
        """Логировать время выполнения запроса"""
        if hasattr(g, 'start_time'):
            elapsed = time() - g.start_time
            
            # Логируем медленные запросы (> 1 секунды)
            if elapsed > 1.0:
                logger.warning(
                    f"Slow request: {request.method} {request.path} "
                    f"took {elapsed:.2f}s"
                )
            
            # Добавляем заголовок с временем выполнения
            response.headers['X-Request-Duration'] = f"{elapsed:.4f}s"
        
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
    
    @staticmethod
    def log_request():
        """Логировать входящий запрос"""
        logger.info(
            f"Request: {request.method} {request.path} "
            f"from {request.remote_addr}"
        )
    
    @staticmethod
    def log_response(response):
        """Логировать ответ"""
        logger.info(
            f"Response: {response.status_code} for "
            f"{request.method} {request.path}"
        )
        return response


def setup_middleware(app):
    """Настройка всех middleware"""
    PerformanceMonitoring(app)
    
    # RequestLogger только в production
    if not app.debug:
        RequestLogger(app)
