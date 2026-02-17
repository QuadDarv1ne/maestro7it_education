"""
Middleware для трассировки запросов
"""
import uuid
import logging
import time
from flask import request, g
from functools import wraps

logger = logging.getLogger(__name__)


class RequestIDMiddleware:
    """Добавляет уникальный ID к каждому запросу для трассировки"""
    
    def __init__(self, app=None):
        self.app = app
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Инициализация с Flask приложением"""
        app.before_request(self.before_request)
        app.after_request(self.after_request)
        
        # Добавляем фильтр для логирования
        self.setup_logging()
    
    def before_request(self):
        """Генерация request ID перед обработкой запроса"""
        # Проверяем, есть ли ID в заголовках (для цепочки запросов)
        request_id = request.headers.get('X-Request-ID')
        
        if not request_id:
            request_id = str(uuid.uuid4())
        
        g.request_id = request_id
        g.request_start_time = time.time()
        
        # Логируем начало запроса
        logger.info(
            f"Request started",
            extra={
                'request_id': request_id,
                'method': request.method,
                'path': request.path,
                'remote_addr': request.remote_addr,
                'user_agent': request.user_agent.string
            }
        )
    
    def after_request(self, response):
        """Добавление request ID в заголовки ответа"""
        if hasattr(g, 'request_id'):
            response.headers['X-Request-ID'] = g.request_id
            
            # Вычисляем время обработки
            if hasattr(g, 'request_start_time'):
                duration = time.time() - g.request_start_time
                response.headers['X-Response-Time'] = f"{duration:.3f}s"
                
                # Логируем завершение запроса
                logger.info(
                    f"Request completed",
                    extra={
                        'request_id': g.request_id,
                        'status_code': response.status_code,
                        'duration': duration,
                        'content_length': response.content_length
                    }
                )
        
        return response
    
    def setup_logging(self):
        """Настройка логирования с request ID"""
        class RequestIDFilter(logging.Filter):
            def filter(self, record):
                record.request_id = getattr(g, 'request_id', 'no-request-id')
                return True
        
        # Добавляем фильтр ко всем handlers
        for handler in logger.handlers:
            handler.addFilter(RequestIDFilter())


def with_request_id(func):
    """Декоратор для передачи request ID в функцию"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if hasattr(g, 'request_id'):
            kwargs['request_id'] = g.request_id
        return func(*args, **kwargs)
    return wrapper


class CorrelationIDMiddleware:
    """
    Middleware для корреляции запросов между микросервисами
    Поддерживает X-Correlation-ID для отслеживания цепочки запросов
    """
    
    def __init__(self, app=None):
        self.app = app
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Инициализация с Flask приложением"""
        app.before_request(self.before_request)
        app.after_request(self.after_request)
    
    def before_request(self):
        """Обработка correlation ID"""
        # Получаем или создаем correlation ID
        correlation_id = request.headers.get('X-Correlation-ID')
        
        if not correlation_id:
            correlation_id = str(uuid.uuid4())
        
        g.correlation_id = correlation_id
        
        # Получаем или создаем span ID (для трассировки внутри одного запроса)
        span_id = request.headers.get('X-Span-ID')
        if not span_id:
            span_id = str(uuid.uuid4())
        
        g.span_id = span_id
        
        # Получаем parent span ID (если есть)
        parent_span_id = request.headers.get('X-Parent-Span-ID')
        if parent_span_id:
            g.parent_span_id = parent_span_id
        
        logger.info(
            f"Correlation tracking",
            extra={
                'correlation_id': correlation_id,
                'span_id': span_id,
                'parent_span_id': parent_span_id
            }
        )
    
    def after_request(self, response):
        """Добавление correlation headers в ответ"""
        if hasattr(g, 'correlation_id'):
            response.headers['X-Correlation-ID'] = g.correlation_id
        
        if hasattr(g, 'span_id'):
            response.headers['X-Span-ID'] = g.span_id
        
        return response


def propagate_correlation_headers():
    """
    Получить заголовки для передачи в другие сервисы
    Использовать при вызове других микросервисов
    """
    headers = {}
    
    if hasattr(g, 'correlation_id'):
        headers['X-Correlation-ID'] = g.correlation_id
    
    if hasattr(g, 'span_id'):
        # Текущий span становится parent для следующего запроса
        headers['X-Parent-Span-ID'] = g.span_id
    
    # Генерируем новый span ID для следующего запроса
    headers['X-Span-ID'] = str(uuid.uuid4())
    
    return headers


class RequestContextMiddleware:
    """
    Middleware для сохранения контекста запроса
    Полезно для передачи информации между middleware и handlers
    """
    
    def __init__(self, app=None):
        self.app = app
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Инициализация с Flask приложением"""
        app.before_request(self.before_request)
    
    def before_request(self):
        """Сохранение контекста запроса"""
        g.request_context = {
            'method': request.method,
            'path': request.path,
            'url': request.url,
            'remote_addr': request.remote_addr,
            'user_agent': request.user_agent.string,
            'referrer': request.referrer,
            'timestamp': time.time(),
            'headers': dict(request.headers)
        }
        
        # Извлекаем user_id если есть (из JWT или сессии)
        if hasattr(g, 'current_user'):
            g.request_context['user_id'] = g.current_user.id
        
        # Извлекаем API key если есть
        api_key = request.headers.get('X-API-Key')
        if api_key:
            g.request_context['api_key'] = api_key[:8] + '...'  # Частично скрываем


def get_request_context() -> dict:
    """Получить контекст текущего запроса"""
    return getattr(g, 'request_context', {})


class RequestMetricsMiddleware:
    """
    Middleware для сбора метрик запросов
    """
    
    def __init__(self, app=None):
        self.app = app
        self.metrics = {
            'total_requests': 0,
            'requests_by_method': {},
            'requests_by_endpoint': {},
            'response_times': []
        }
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Инициализация с Flask приложением"""
        app.before_request(self.before_request)
        app.after_request(self.after_request)
    
    def before_request(self):
        """Начало измерения времени"""
        g.metrics_start_time = time.time()
    
    def after_request(self, response):
        """Сбор метрик после обработки запроса"""
        if hasattr(g, 'metrics_start_time'):
            duration = time.time() - g.metrics_start_time
            
            # Обновляем метрики
            self.metrics['total_requests'] += 1
            
            method = request.method
            self.metrics['requests_by_method'][method] = \
                self.metrics['requests_by_method'].get(method, 0) + 1
            
            endpoint = request.endpoint or 'unknown'
            self.metrics['requests_by_endpoint'][endpoint] = \
                self.metrics['requests_by_endpoint'].get(endpoint, 0) + 1
            
            self.metrics['response_times'].append(duration)
            
            # Ограничиваем размер списка времен ответа
            if len(self.metrics['response_times']) > 1000:
                self.metrics['response_times'] = self.metrics['response_times'][-1000:]
        
        return response
    
    def get_metrics(self) -> dict:
        """Получить собранные метрики"""
        response_times = self.metrics['response_times']
        
        if response_times:
            avg_response_time = sum(response_times) / len(response_times)
            max_response_time = max(response_times)
            min_response_time = min(response_times)
        else:
            avg_response_time = max_response_time = min_response_time = 0
        
        return {
            'total_requests': self.metrics['total_requests'],
            'requests_by_method': self.metrics['requests_by_method'],
            'requests_by_endpoint': self.metrics['requests_by_endpoint'],
            'avg_response_time': avg_response_time,
            'max_response_time': max_response_time,
            'min_response_time': min_response_time
        }


# Глобальные экземпляры
request_id_middleware = RequestIDMiddleware()
correlation_id_middleware = CorrelationIDMiddleware()
request_context_middleware = RequestContextMiddleware()
request_metrics_middleware = RequestMetricsMiddleware()
