"""
Middleware для отслеживания запросов с correlation ID
"""
import uuid
import logging
from functools import wraps
from flask import request, g, has_request_context
from typing import Optional

logger = logging.getLogger(__name__)

class RequestCorrelationMiddleware:
    """Middleware для добавления correlation ID к каждому запросу"""
    
    def __init__(self, app=None):
        self.app = app
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Инициализация middleware с Flask приложением"""
        self.app = app
        
        # Регистрация before_request handler
        @app.before_request
        def before_request():
            self._set_correlation_id()
        
        # Регистрация after_request handler
        @app.after_request
        def after_request(response):
            return self._add_correlation_header(response)
        
        logger.info("Middleware корреляции запросов инициализирован")
    
    def _set_correlation_id(self):
        """Установка correlation ID для текущего запроса"""
        if has_request_context():
            # Попытка получить correlation ID из заголовков
            correlation_id = request.headers.get('X-Correlation-ID')
            
            if not correlation_id:
                # Генерация нового correlation ID если не предоставлен
                correlation_id = str(uuid.uuid4())
            
            # Сохранение в глобальном контексте
            g.correlation_id = correlation_id
            
            # Добавление в логгер
            self._add_correlation_to_logging()
    
    def _add_correlation_to_logging(self):
        """Добавление correlation ID к логированию"""
        class CorrelationIdFilter(logging.Filter):
            def filter(self, record):
                if has_request_context() and hasattr(g, 'correlation_id'):
                    record.correlation_id = g.correlation_id
                else:
                    record.correlation_id = 'no-request'
                return True
        
        # Добавление фильтра ко всем логгерам
        root_logger = logging.getLogger()
        correlation_filter = CorrelationIdFilter()
        
        # Избежание дублирования фильтров
        if not any(isinstance(f, CorrelationIdFilter) for f in root_logger.filters):
            root_logger.addFilter(correlation_filter)
    
    def _add_correlation_header(self, response):
        """Добавление correlation ID в заголовки ответа"""
        if has_request_context() and hasattr(g, 'correlation_id'):
            response.headers['X-Correlation-ID'] = g.correlation_id
        return response
    
    def get_current_correlation_id(self) -> Optional[str]:
        """Получение текущего correlation ID"""
        if has_request_context() and hasattr(g, 'correlation_id'):
            return g.correlation_id
        return None

def with_correlation_id(f):
    """Декоратор для добавления correlation ID к функциям"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        correlation_id = None
        if has_request_context():
            correlation_id = getattr(g, 'correlation_id', None)
        
        # Добавление correlation ID в kwargs если он есть
        if correlation_id and 'correlation_id' not in kwargs:
            kwargs['correlation_id'] = correlation_id
            
        return f(*args, **kwargs)
    return decorated_function

# Глобальный экземпляр middleware
correlation_middleware = RequestCorrelationMiddleware()

# Flask CLI команды для управления middleware
def register_correlation_commands(app):
    """Регистрация CLI команд управления correlation ID"""
    import click
    from flask.cli import with_appcontext
    
    @app.cli.command('correlation-status')
    @with_appcontext
    def correlation_status():
        """Показать статус middleware корреляции"""
        click.echo("Middleware корреляции запросов:")
        click.echo(f"  Статус: Активен")
        click.echo(f"  Генерация UUID: Включена")
        click.echo(f"  Заголовки: X-Correlation-ID")
        
        # Тестовая генерация
        test_id = str(uuid.uuid4())
        click.echo(f"  Тестовый ID: {test_id}")
    
    @app.cli.command('generate-correlation-id')
    @with_appcontext
    def generate_correlation_id():
        """Сгенерировать новый correlation ID"""
        correlation_id = str(uuid.uuid4())
        click.echo(f"Новый Correlation ID: {correlation_id}")