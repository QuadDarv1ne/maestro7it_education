"""
Middleware для мониторинга производительности приложения
"""

from flask import request, g
from functools import wraps
import time
import logging
from datetime import datetime
from collections import deque
from threading import Lock

logger = logging.getLogger(__name__)


class PerformanceMonitor:
    """Мониторинг производительности запросов"""
    
    def __init__(self, app=None, max_history=1000):
        self.max_history = max_history
        self.request_history = deque(maxlen=max_history)
        self.slow_queries = deque(maxlen=100)
        self.error_count = 0
        self.total_requests = 0
        self.lock = Lock()
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Инициализация с Flask приложением"""
        app.before_request(self.before_request)
        app.after_request(self.after_request)
        app.teardown_request(self.teardown_request)
        
        # Сохранение ссылки на монитор в приложении
        app.performance_monitor = self
        
        logger.info("Performance monitoring initialized")
    
    def before_request(self):
        """Вызывается перед каждым запросом"""
        g.start_time = time.time()
        g.request_id = f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{self.total_requests}"
    
    def after_request(self, response):
        """Вызывается после каждого запроса"""
        if not hasattr(g, 'start_time'):
            return response
        
        # Расчет времени выполнения
        execution_time = time.time() - g.start_time
        
        # Сбор метрик
        request_data = {
            'id': getattr(g, 'request_id', 'unknown'),
            'timestamp': datetime.utcnow().isoformat(),
            'method': request.method,
            'path': request.path,
            'status_code': response.status_code,
            'execution_time': round(execution_time * 1000, 2),  # в миллисекундах
            'ip': request.remote_addr,
            'user_agent': request.user_agent.string[:100] if request.user_agent else None
        }
        
        with self.lock:
            self.total_requests += 1
            self.request_history.append(request_data)
            
            # Отслеживание медленных запросов (> 1 секунда)
            if execution_time > 1.0:
                logger.warning(
                    f"Slow request: {request.method} {request.path} "
                    f"took {execution_time:.2f}s"
                )
                self.slow_queries.append(request_data)
            
            # Отслеживание ошибок
            if response.status_code >= 400:
                self.error_count += 1
        
        # Добавление заголовков производительности
        response.headers['X-Request-ID'] = request_data['id']
        response.headers['X-Execution-Time'] = str(request_data['execution_time'])
        
        # Логирование (только в debug режиме)
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(
                f"Request: {request.method} {request.path} "
                f"Status: {response.status_code} "
                f"Time: {request_data['execution_time']}ms"
            )
        
        return response
    
    def teardown_request(self, exception=None):
        """Вызывается при завершении запроса (даже если была ошибка)"""
        if exception:
            logger.error(f"Request failed with exception: {exception}")
    
    def get_stats(self):
        """Получить статистику производительности"""
        with self.lock:
            if not self.request_history:
                return {
                    'total_requests': 0,
                    'error_count': 0,
                    'average_time': 0,
                    'slow_queries_count': 0
                }
            
            execution_times = [r['execution_time'] for r in self.request_history]
            
            return {
                'total_requests': self.total_requests,
                'error_count': self.error_count,
                'error_rate': round(self.error_count / self.total_requests * 100, 2) if self.total_requests > 0 else 0,
                'average_time': round(sum(execution_times) / len(execution_times), 2),
                'min_time': round(min(execution_times), 2),
                'max_time': round(max(execution_times), 2),
                'slow_queries_count': len(self.slow_queries),
                'recent_requests': len(self.request_history)
            }
    
    def get_slow_queries(self, limit=10):
        """Получить список медленных запросов"""
        with self.lock:
            return list(self.slow_queries)[-limit:]
    
    def get_recent_requests(self, limit=50):
        """Получить последние запросы"""
        with self.lock:
            return list(self.request_history)[-limit:]
    
    def get_endpoint_stats(self):
        """Получить статистику по эндпоинтам"""
        with self.lock:
            endpoint_stats = {}
            
            for req in self.request_history:
                path = req['path']
                if path not in endpoint_stats:
                    endpoint_stats[path] = {
                        'count': 0,
                        'total_time': 0,
                        'errors': 0
                    }
                
                endpoint_stats[path]['count'] += 1
                endpoint_stats[path]['total_time'] += req['execution_time']
                if req['status_code'] >= 400:
                    endpoint_stats[path]['errors'] += 1
            
            # Расчет средних значений
            for path, stats in endpoint_stats.items():
                stats['average_time'] = round(stats['total_time'] / stats['count'], 2)
                stats['error_rate'] = round(stats['errors'] / stats['count'] * 100, 2)
            
            # Сортировка по количеству запросов
            sorted_stats = sorted(
                endpoint_stats.items(),
                key=lambda x: x[1]['count'],
                reverse=True
            )
            
            return dict(sorted_stats[:20])  # Топ 20 эндпоинтов
    
    def reset_stats(self):
        """Сброс статистики"""
        with self.lock:
            self.request_history.clear()
            self.slow_queries.clear()
            self.error_count = 0
            self.total_requests = 0
        
        logger.info("Performance stats reset")


# Глобальный экземпляр
performance_monitor = PerformanceMonitor()


def measure_time(func_name=None):
    """
    Декоратор для измерения времени выполнения функций
    
    Usage:
        @measure_time()
        def my_function():
            ...
    """
    def decorator(f):
        name = func_name or f.__name__
        
        @wraps(f)
        def decorated_function(*args, **kwargs):
            start_time = time.time()
            try:
                result = f(*args, **kwargs)
                return result
            finally:
                execution_time = time.time() - start_time
                if execution_time > 0.1:  # Логируем только если > 100ms
                    logger.debug(f"Function {name} took {execution_time*1000:.2f}ms")
        
        return decorated_function
    return decorator


def slow_query_threshold(threshold_seconds=1.0):
    """
    Декоратор для предупреждения о медленных операциях
    
    Args:
        threshold_seconds: Порог в секундах
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            start_time = time.time()
            try:
                result = f(*args, **kwargs)
                return result
            finally:
                execution_time = time.time() - start_time
                if execution_time > threshold_seconds:
                    logger.warning(
                        f"Slow operation detected: {f.__name__} "
                        f"took {execution_time:.2f}s "
                        f"(threshold: {threshold_seconds}s)"
                    )
        
        return decorated_function
    return decorator


class DatabaseQueryMonitor:
    """Мониторинг запросов к базе данных"""
    
    def __init__(self):
        self.queries = deque(maxlen=1000)
        self.slow_queries = deque(maxlen=100)
        self.lock = Lock()
    
    def log_query(self, query, duration):
        """Логирование запроса к БД"""
        query_data = {
            'query': str(query)[:500],  # Ограничиваем длину
            'duration': round(duration * 1000, 2),  # мс
            'timestamp': datetime.utcnow().isoformat()
        }
        
        with self.lock:
            self.queries.append(query_data)
            
            if duration > 0.1:  # Медленные запросы > 100ms
                self.slow_queries.append(query_data)
                logger.warning(f"Slow database query ({duration*1000:.2f}ms): {query_data['query']}")
    
    def get_stats(self):
        """Получить статистику запросов к БД"""
        with self.lock:
            if not self.queries:
                return {
                    'total_queries': 0,
                    'average_time': 0,
                    'slow_queries': 0
                }
            
            durations = [q['duration'] for q in self.queries]
            
            return {
                'total_queries': len(self.queries),
                'average_time': round(sum(durations) / len(durations), 2),
                'min_time': round(min(durations), 2),
                'max_time': round(max(durations), 2),
                'slow_queries': len(self.slow_queries)
            }
    
    def get_slow_queries(self, limit=10):
        """Получить медленные запросы"""
        with self.lock:
            return list(self.slow_queries)[-limit:]


# Глобальный экземпляр для БД
db_monitor = DatabaseQueryMonitor()
