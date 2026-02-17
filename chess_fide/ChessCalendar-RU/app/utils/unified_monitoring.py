"""
Unified Monitoring System - объединенная система мониторинга
Производительность, логирование, health checks, метрики
"""
import logging
import logging.handlers
import os
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
        self.duration = (self.end_time - self.start_time) * 1000  # миллисекунды
        self.status_code = status_code
    
    def add_db_query(self, query: str, duration: float):
        """Добавить информацию о DB запросе"""
        self.db_queries.append({
            'query': query[:200],
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
    """
    Унифицированный монитор производительности
    - Отслеживание запросов
    - Метрики функций
    - Алерты
    - Статистика
    """
    
    def __init__(self, max_history: int = 1000):
        self.max_history = max_history
        self.request_history = deque(maxlen=max_history)
        self.function_metrics = defaultdict(list)
        self.endpoint_stats = defaultdict(lambda: {
            'count': 0,
            'total_time': 0,
            'min_time': float('inf'),
            'max_time': 0,
            'errors': 0,
            'slow_requests': 0
        })
        self.slow_threshold = 1000  # миллисекунды
        self.error_threshold = 10
        self.alerts = deque(maxlen=100)
        self.lock = threading.Lock()
        self.logger = logging.getLogger('performance_monitor')
    
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
            self.request_history.append(metrics)
            
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
    
    def track_function(self, func_name: str, execution_time: float, 
                      success: bool = True, error: Optional[str] = None):
        """Отслеживать выполнение функции"""
        with self.lock:
            self.function_metrics[func_name].append({
                'execution_time': execution_time,
                'timestamp': datetime.now().isoformat(),
                'success': success,
                'error': error
            })
            
            # Логируем медленные операции
            if execution_time > 5:  # > 5 секунд
                self.logger.warning(f"Slow function: {func_name} took {execution_time:.2f}s")
    
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
        self.logger.warning(f"Performance alert: {alert_type} - {data}")
    
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
    
    def get_function_metrics(self, func_name: Optional[str] = None) -> Dict[str, Any]:
        """Получить метрики функций"""
        with self.lock:
            if func_name:
                if func_name not in self.function_metrics:
                    return {}
                
                metrics = self.function_metrics[func_name]
                execution_times = [m['execution_time'] for m in metrics if m['success']]
                
                if not execution_times:
                    return {'message': 'No successful executions'}
                
                return {
                    'function': func_name,
                    'call_count': len(metrics),
                    'success_count': len([m for m in metrics if m['success']]),
                    'avg_time': sum(execution_times) / len(execution_times),
                    'min_time': min(execution_times),
                    'max_time': max(execution_times),
                    'error_count': len([m for m in metrics if not m['success']])
                }
            
            # Возвращаем сводку по всем функциям
            summary = {}
            for fname, metrics in self.function_metrics.items():
                execution_times = [m['execution_time'] for m in metrics if m['success']]
                if execution_times:
                    summary[fname] = {
                        'call_count': len(metrics),
                        'success_count': len([m for m in metrics if m['success']]),
                        'avg_time': round(sum(execution_times) / len(execution_times), 3),
                        'min_time': round(min(execution_times), 3),
                        'max_time': round(max(execution_times), 3),
                        'error_count': len([m for m in metrics if not m['success']])
                    }
            return summary
    
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
                'monitored_endpoints': len(self.endpoint_stats),
                'monitored_functions': len(self.function_metrics)
            }
    
    def reset_stats(self):
        """Сбросить статистику"""
        with self.lock:
            self.request_history.clear()
            self.function_metrics.clear()
            self.endpoint_stats.clear()
            self.alerts.clear()


class HealthChecker:
    """Проверка состояния системы"""
    
    def __init__(self):
        self.checks = {}
        self.logger = logging.getLogger('health_checker')
    
    def add_health_check(self, name: str, check_func: Callable):
        """Добавить проверку состояния"""
        self.checks[name] = check_func
    
    def run_health_checks(self) -> Dict[str, Any]:
        """Выполнить все проверки состояния"""
        results = {}
        for name, check_func in self.checks.items():
            try:
                result = check_func()
                results[name] = {
                    'status': 'healthy' if result else 'unhealthy',
                    'result': result,
                    'timestamp': datetime.now().isoformat()
                }
            except Exception as e:
                results[name] = {
                    'status': 'error',
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                }
                self.logger.error(f"Health check {name} failed: {e}")
        
        return results
    
    def get_health_status(self) -> str:
        """Получить общий статус здоровья системы"""
        results = self.run_health_checks()
        unhealthy_checks = [name for name, result in results.items() 
                          if result['status'] != 'healthy']
        
        if not unhealthy_checks:
            return 'healthy'
        elif len(unhealthy_checks) == len(results):
            return 'critical'
        else:
            return 'degraded'


class LoggerSetup:
    """Настройка системы логирования"""
    
    @staticmethod
    def setup_logging(log_level=logging.INFO, log_file='chess_calendar.log'):
        """Настройка логирования для приложения"""
        log_dir = 'logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        formatter = logging.Formatter(log_format)
        
        root_logger = logging.getLogger()
        root_logger.setLevel(log_level)
        
        # Файловый обработчик с ротацией
        file_handler = logging.handlers.RotatingFileHandler(
            os.path.join(log_dir, log_file),
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
        
        # Консольный обработчик
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)
        
        logging.info("Logging system initialized")


# Декораторы
def track_performance(func_name: Optional[str] = None):
    """Декоратор для отслеживания производительности функций"""
    def decorator(func: Callable) -> Callable:
        name = func_name or func.__name__
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                performance_monitor.track_function(name, execution_time, success=True)
                return result
            except Exception as e:
                execution_time = time.time() - start_time
                performance_monitor.track_function(name, execution_time, success=False, error=str(e))
                raise
        
        return wrapper
    return decorator


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
            
            if duration > 100:  # > 100ms
                logger = logging.getLogger('performance_monitor')
                logger.warning(f"Slow function: {func.__name__} took {duration:.2f}ms")
    
    return wrapper


def log_action(action_name: str):
    """Декоратор для логирования действий"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logging.info(f"Starting action: {action_name}")
            try:
                result = func(*args, **kwargs)
                logging.info(f"Action completed: {action_name}")
                return result
            except Exception as e:
                logging.error(f"Action failed: {action_name} - {e}")
                raise
        return wrapper
    return decorator


# Глобальные экземпляры
performance_monitor = PerformanceMonitor()
health_checker = HealthChecker()
logger_setup = LoggerSetup()


# Предопределенные проверки состояния
def check_database_connection():
    """Проверка соединения с базой данных"""
    try:
        from app import db
        db.session.execute('SELECT 1')
        return True
    except Exception:
        return False


def check_cache_connection():
    """Проверка соединения с кэшем"""
    try:
        from app.utils.unified_cache import cache
        stats = cache.get_stats()
        return stats.get('l2', {}).get('connected', False) or len(stats.get('l1', {})) > 0
    except Exception:
        return False


def check_parser_status():
    """Проверка работоспособности парсеров"""
    try:
        from app.utils.fide_parser import FIDEParses
        from app.utils.cfr_parser import CFRParser
        
        fide_parser = FIDEParses()
        cfr_parser = CFRParser()
        
        return fide_parser is not None and cfr_parser is not None
    except Exception:
        return False


def check_application_status():
    """Проверка общего статуса приложения"""
    try:
        return {
            'status': 'running',
            'timestamp': datetime.now().isoformat()
        }
    except Exception:
        return False


# Регистрируем стандартные проверки
health_checker.add_health_check('database', check_database_connection)
health_checker.add_health_check('cache', check_cache_connection)
health_checker.add_health_check('parsers', check_parser_status)
health_checker.add_health_check('application', check_application_status)


# Backward compatibility aliases
perf_monitor = performance_monitor
measure_execution_time = track_performance
