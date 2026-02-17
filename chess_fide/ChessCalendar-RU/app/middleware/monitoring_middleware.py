"""
Middleware для автоматического мониторинга запросов
"""

from flask import request, g
from app.utils.unified_monitoring import performance_monitor


class MonitoringMiddleware:
    """Middleware для мониторинга производительности"""
    
    def __init__(self, app=None):
        self.app = app
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Инициализация middleware"""
        app.before_request(self.before_request)
        app.after_request(self.after_request)
    
    def before_request(self):
        """Вызывается перед каждым запросом"""
        performance_monitor.start_request()
    
    def after_request(self, response):
        """Вызывается после каждого запроса"""
        performance_monitor.finish_request(response.status_code)
        return response


# Глобальный экземпляр
monitoring_middleware = MonitoringMiddleware()
