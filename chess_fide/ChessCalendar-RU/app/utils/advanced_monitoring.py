"""
Расширенная система мониторинга производительности
Детальная аналитика запросов, профилирование и алерты
"""

import time
import functools
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from collections import defaultdict, deque
from flask import request, g
import threading


class RequestMetrics:
    """Метрики отдельного запроса"""
    
    def __init__(self):
        self.start_time = time.time()
        self.end_time = None
        self.duration = None
        self.endpoint = None
        self.method = None
        self.status_code = None
        self.db_queries = []
        self.cache_hits = 0
        self.cache_misses = 0
        self.external_calls = []
        self.memory_usage = 0
        self.user_id = None
    
    def finish(self, status_code: int):
        """Завершить сбор метрик"""
        self.end_time = time.time()
        self.duration = (self.end_time - self.start_time) * 1000  # в миллисекундах
        self.status_code = status_code
    
    def add_db_query(self, query: str, duration: float):
        """Добавить информацию о DB запросе"""
        self.db_queries.append({
            'query': query[:200],  # Ограничиваем длину
            'duration': duration
        })
    
    def add_external_call(self, url: str, duration: float, status: int):
        """Добавить информацию о внешнем вызове"""
        self.external_calls.append({
            'url': url,
            'duration': duration,
            'status': status
        })
    
    def to_dict(self) -> Dict[str, Any]:
        """Преобразовать в словарь"""
        return {
            'duration': round(self.duration, 2) if self.duration else None,
            'endpoint': self.endpoint,
            'method': self.method,
            'status_code': self.status_code,
            'db_queries_count': len(self.db_queries),
            'db_queries_time': sum(q['duration'] for q in self.db_queries),
            'cache_hits': self.cache_hits,
            'cache_misses': self.cache_misses,
            'external_calls_count': len(self.external_calls),
            'external_calls_time': sum(c['duration'] for c in self.external_calls),
            'timestamp': datetime.fromtimestamp(self.start_time).isoformat()
        }


class PerformanceMonitor:
    """Монитор производительности приложения"""
    
    def __init__(self, max_history: int = 1000):
        self.max_history = max_history
        self.request_history = deque(maxlen=max_history)
        self.endpoint_stats = defaultdict(lambda: {
            'count': 0,
            'total_time': 0,
            'min_time': float('inf'),
            'max_time': 0,
            'errors': 0,
            'slow_requests': 0
        })
        self.slow_threshold = 1000  # миллисекунды
        self.error_threshold = 10  # количество ошибок для алерта
        self.alerts = deque(maxlen=100)
        self.lock = threading.Lock()
    
    def start_request(self):
        """Начать отслеживание запроса"""
        metrics = RequestMetrics()
        metrics.endpoint = request.endpoint
        metrics.method = request.method
        metrics.user_id = getattr(g, 'user_id', None)
        
        g.request_metrics = metrics
        return metrics
    
    def finish_request(self, status_code: int):
        """Завершить отслеживание запроса"""
        if not hasattr(g, 'request_metrics'):
            return
        
        metrics = g.request_metrics
        metrics.finish(status_code)
        
        with self.lock:
            # Добавляем в историю
            self.request_history.append(metrics)
            
            # Обновляем статистику по endpoint
            endpoint = metrics.endpoint or 'unknown'
            stats = self.endpoint_stats[endpoint]
            stats['count'] += 1
            stats['total_time'] += metrics.duration
            stats['min_time'] = min(stats['min_time'], metrics.duration)
            stats['max_time'] = max(stats['max_time'], metrics.duration)
            
            if status_code >= 500:
                stats['errors'] += 1
                self._check_error_threshold(endpoint, stats['errors'])
            
            if metrics.duration > self.slow_threshold:
                stats['slow_requests'] += 1
                self._create_alert('slow_request', {
                    'endpoint': endpoint,
                    'duration': metrics.duration,
                    'threshold': self.slow_threshold
                })
    
    def _check_error_threshold(self, endpoint: str, error_count: int):
        """Проверить порог ошибок"""
        if error_count >= self.error_threshold:
            self._create_alert('high_error_rate', {
                'endpoint': endpoint,
                'error_count': error_count,
                'threshold': self.error_threshold
            })
    
    def _create_alert(self, alert_type: str, data: Dict[str, Any]):
        """Создать алерт"""
        alert = {
            'type': alert_type,
            'timestamp': datetime.utcnow().isoformat(),
            'data': data
        }
        self.alerts.append(alert)
        
        # Логирование
        import logging
        logger = logging.getLogger('performance_monitor')
        logger.warning(f"Performance alert: {alert_type} - {data}")
    
    def get_endpoint_stats(self, endpoint: Optional[str] = None) -> Dict[str, Any]:
        """Получить статистику по endpoint"""
        with self.lock:
            if endpoint:
                if endpoint not in self.endpoint_stats:
                    return {}
                
                stats = self.endpoint_stats[endpoint]
                return {
                    'endpoint': endpoint,
                    'count': stats['count'],
                    'avg_time': stats['total_time'] / stats['count'] if stats['count'] > 0 else 0,
                    'min_time': stats['min_time'] if stats['min_time'] != float('inf') else 0,
                    'max_time': stats['max_time'],
                    'errors': stats['errors'],
                    'slow_requests': stats['slow_requests'],
                    'error_rate': stats['errors'] / stats['count'] if stats['count'] > 0 else 0
                }
            
            # Возвращаем статистику по всем endpoints
            return {
                ep: {
                    'count': stats['count'],
                    'avg_time': round(stats['total_time'] / stats['count'], 2) if stats['count'] > 0 else 0,
                    'min_time': round(stats['min_time'], 2) if stats['min_time'] != float('inf') else 0,
                    'max_time': round(stats['max_time'], 2),
                    'errors': stats['errors'],
                    'slow_requests': stats['slow_requests']
                }
                for ep, stats in self.endpoint_stats.items()
            }
    
    def get_recent_requests(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Получить последние запросы"""
        with self.lock:
            return [m.to_dict() for m in list(self.request_history)[-limit:]]
    
    def get_slow_requests(self, threshold: Optional[int] = None) -> List[Dict[str, Any]]:
        """Получить медленные запросы"""
        threshold = threshold or self.slow_threshold
        
        with self.lock:
            slow = [
                m.to_dict() for m in self.request_history
                if m.duration and m.duration > threshold
            ]
            return sorted(slow, key=lambda x: x['duration'], reverse=True)
    
    def get_alerts(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Получить последние алерты"""
        with self.lock:
            return list(self.alerts)[-limit:]
    
    def get_summary(self) -> Dict[str, Any]:
        """Получить общую сводку"""
        with self.lock:
            total_requests = len(self.request_history)
            if total_requests == 0:
                return {'message': 'No requests recorded'}
            
            total_time = sum(m.duration for m in self.request_history if m.duration)
            error_count = sum(1 for m in self.request_history if m.status_code and m.status_code >= 500)
            slow_count = sum(1 for m in self.request_history if m.duration and m.duration > self.slow_threshold)
            
            return {
                'total_requests': total_requests,
                'avg_response_time': round(total_time / total_requests, 2),
                'error_count': error_count,
                'error_rate': round(error_count / total_requests * 100, 2),
                'slow_requests': slow_count,
                'slow_request_rate': round(slow_count / total_requests * 100, 2),
                'active_alerts': len(self.alerts),
                'monitored_endpoints': len(self.endpoint_stats)
            }
    
    def reset_stats(self):
        """Сбросить статистику"""
        with self.lock:
            self.request_history.clear()
            self.endpoint_stats.clear()
            self.alerts.clear()


def profile_function(func: Callable) -> Callable:
    """Декоратор для профилирования функций"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            duration = (time.time() - start_time) * 1000
            
            # Логирование медленных функций
            if duration > 100:  # > 100ms
                import logging
                logger = logging.getLogger('performance_monitor')
                logger.warning(f"Slow function: {func.__name__} took {duration:.2f}ms")
    
    return wrapper


# Глобальный экземпляр
performance_monitor = PerformanceMonitor()
