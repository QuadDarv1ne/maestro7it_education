"""
Сборщик метрик для мониторинга
"""
import time
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from collections import defaultdict
import psutil
import redis

logger = logging.getLogger(__name__)


class MetricsCollector:
    """Сборщик метрик приложения"""
    
    def __init__(self, redis_client: Optional[redis.Redis] = None):
        self.redis = redis_client
        self.metrics = defaultdict(list)
        self.counters = defaultdict(int)
        self.gauges = defaultdict(float)
        self.histograms = defaultdict(list)
    
    def increment_counter(self, name: str, value: int = 1, tags: Dict = None):
        """
        Увеличить счетчик
        
        Args:
            name: имя метрики
            value: значение для увеличения
            tags: теги метрики
        """
        key = self._make_key(name, tags)
        self.counters[key] += value
        
        # Сохраняем в Redis
        if self.redis:
            try:
                self.redis.incr(f"counter:{key}", value)
            except Exception as e:
                logger.error(f"Failed to increment counter: {e}")
    
    def set_gauge(self, name: str, value: float, tags: Dict = None):
        """
        Установить gauge метрику
        
        Args:
            name: имя метрики
            value: значение
            tags: теги метрики
        """
        key = self._make_key(name, tags)
        self.gauges[key] = value
        
        # Сохраняем в Redis
        if self.redis:
            try:
                self.redis.set(f"gauge:{key}", value)
            except Exception as e:
                logger.error(f"Failed to set gauge: {e}")
    
    def record_histogram(self, name: str, value: float, tags: Dict = None):
        """
        Записать значение в histogram
        
        Args:
            name: имя метрики
            value: значение
            tags: теги метрики
        """
        key = self._make_key(name, tags)
        self.histograms[key].append(value)
        
        # Ограничиваем размер
        if len(self.histograms[key]) > 1000:
            self.histograms[key] = self.histograms[key][-1000:]
        
        # Сохраняем в Redis (используем sorted set)
        if self.redis:
            try:
                timestamp = time.time()
                self.redis.zadd(f"histogram:{key}", {str(value): timestamp})
                
                # Удаляем старые значения (старше 1 часа)
                cutoff = timestamp - 3600
                self.redis.zremrangebyscore(f"histogram:{key}", 0, cutoff)
            except Exception as e:
                logger.error(f"Failed to record histogram: {e}")
    
    def _make_key(self, name: str, tags: Optional[Dict] = None) -> str:
        """Создать ключ метрики с тегами"""
        if not tags:
            return name
        
        tag_str = ','.join(f"{k}={v}" for k, v in sorted(tags.items()))
        return f"{name}[{tag_str}]"
    
    def get_counter(self, name: str, tags: Dict = None) -> int:
        """Получить значение счетчика"""
        key = self._make_key(name, tags)
        
        if self.redis:
            try:
                value = self.redis.get(f"counter:{key}")
                return int(value) if value else 0
            except Exception as e:
                logger.error(f"Failed to get counter: {e}")
        
        return self.counters.get(key, 0)
    
    def get_gauge(self, name: str, tags: Dict = None) -> float:
        """Получить значение gauge"""
        key = self._make_key(name, tags)
        
        if self.redis:
            try:
                value = self.redis.get(f"gauge:{key}")
                return float(value) if value else 0.0
            except Exception as e:
                logger.error(f"Failed to get gauge: {e}")
        
        return self.gauges.get(key, 0.0)
    
    def get_histogram_stats(self, name: str, tags: Dict = None) -> Dict[str, float]:
        """Получить статистику histogram"""
        key = self._make_key(name, tags)
        
        values = []
        
        if self.redis:
            try:
                # Получаем значения из Redis
                redis_values = self.redis.zrange(f"histogram:{key}", 0, -1)
                values = [float(v) for v in redis_values]
            except Exception as e:
                logger.error(f"Failed to get histogram: {e}")
        
        if not values:
            values = self.histograms.get(key, [])
        
        if not values:
            return {}
        
        values.sort()
        count = len(values)
        
        return {
            'count': count,
            'min': values[0],
            'max': values[-1],
            'mean': sum(values) / count,
            'median': values[count // 2],
            'p95': values[int(count * 0.95)] if count > 1 else values[0],
            'p99': values[int(count * 0.99)] if count > 1 else values[0]
        }
    
    def collect_system_metrics(self):
        """Собрать системные метрики"""
        # CPU
        cpu_percent = psutil.cpu_percent(interval=1)
        self.set_gauge('system.cpu.percent', cpu_percent)
        
        # Memory
        memory = psutil.virtual_memory()
        self.set_gauge('system.memory.percent', memory.percent)
        self.set_gauge('system.memory.used_mb', memory.used / (1024 * 1024))
        self.set_gauge('system.memory.available_mb', memory.available / (1024 * 1024))
        
        # Disk
        disk = psutil.disk_usage('/')
        self.set_gauge('system.disk.percent', disk.percent)
        self.set_gauge('system.disk.used_gb', disk.used / (1024 * 1024 * 1024))
        self.set_gauge('system.disk.free_gb', disk.free / (1024 * 1024 * 1024))
        
        # Network
        net_io = psutil.net_io_counters()
        self.set_gauge('system.network.bytes_sent', net_io.bytes_sent)
        self.set_gauge('system.network.bytes_recv', net_io.bytes_recv)
    
    def collect_application_metrics(self, app):
        """Собрать метрики приложения"""
        from app import db
        
        # Database connections
        try:
            pool = db.engine.pool
            self.set_gauge('app.db.pool_size', pool.size())
            self.set_gauge('app.db.checked_out', pool.checkedout())
            self.set_gauge('app.db.overflow', pool.overflow())
        except Exception as e:
            logger.error(f"Failed to collect DB metrics: {e}")
        
        # Redis
        if self.redis:
            try:
                info = self.redis.info()
                self.set_gauge('app.redis.used_memory_mb', 
                             info.get('used_memory', 0) / (1024 * 1024))
                self.set_gauge('app.redis.connected_clients', 
                             info.get('connected_clients', 0))
                self.set_gauge('app.redis.keys', self.redis.dbsize())
            except Exception as e:
                logger.error(f"Failed to collect Redis metrics: {e}")
    
    def get_all_metrics(self) -> Dict[str, Any]:
        """Получить все метрики"""
        return {
            'counters': dict(self.counters),
            'gauges': dict(self.gauges),
            'histograms': {
                name: self.get_histogram_stats(name.split('[')[0], 
                    self._parse_tags(name) if '[' in name else None)
                for name in self.histograms.keys()
            },
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def _parse_tags(self, key: str) -> Dict[str, str]:
        """Парсинг тегов из ключа"""
        if '[' not in key:
            return {}
        
        tag_str = key.split('[')[1].rstrip(']')
        tags = {}
        
        for pair in tag_str.split(','):
            k, v = pair.split('=')
            tags[k] = v
        
        return tags
    
    def reset(self):
        """Сбросить все метрики"""
        self.counters.clear()
        self.gauges.clear()
        self.histograms.clear()


class RequestMetrics:
    """Метрики HTTP запросов"""
    
    def __init__(self, collector: MetricsCollector):
        self.collector = collector
    
    def record_request(
        self,
        method: str,
        endpoint: str,
        status_code: int,
        duration: float
    ):
        """Записать метрики запроса"""
        tags = {
            'method': method,
            'endpoint': endpoint,
            'status': str(status_code)
        }
        
        # Счетчик запросов
        self.collector.increment_counter('http.requests', tags=tags)
        
        # Время ответа
        self.collector.record_histogram('http.response_time', duration, tags=tags)
        
        # Счетчик ошибок
        if status_code >= 400:
            self.collector.increment_counter('http.errors', tags=tags)
    
    def get_request_stats(self) -> Dict[str, Any]:
        """Получить статистику запросов"""
        return {
            'total_requests': self.collector.get_counter('http.requests'),
            'total_errors': self.collector.get_counter('http.errors'),
            'response_time': self.collector.get_histogram_stats('http.response_time')
        }


class BusinessMetrics:
    """Бизнес-метрики"""
    
    def __init__(self, collector: MetricsCollector):
        self.collector = collector
    
    def record_user_action(self, action: str, user_id: Optional[str] = None):
        """Записать действие пользователя"""
        tags = {'action': action}
        if user_id:
            tags['user_id'] = user_id
        
        self.collector.increment_counter('user.actions', tags=tags)
    
    def record_tournament_view(self, tournament_id: str):
        """Записать просмотр турнира"""
        self.collector.increment_counter('tournament.views', 
                                        tags={'tournament_id': tournament_id})
    
    def record_search(self, query: str, results_count: int):
        """Записать поиск"""
        self.collector.increment_counter('search.queries')
        self.collector.record_histogram('search.results_count', results_count)
    
    def set_active_users(self, count: int):
        """Установить количество активных пользователей"""
        self.collector.set_gauge('users.active', count)
    
    def set_total_tournaments(self, count: int):
        """Установить общее количество турниров"""
        self.collector.set_gauge('tournaments.total', count)


class PerformanceMonitor:
    """Мониторинг производительности"""
    
    def __init__(self, collector: MetricsCollector):
        self.collector = collector
    
    def monitor_function(self, func_name: str):
        """Декоратор для мониторинга функции"""
        def decorator(func):
            def wrapper(*args, **kwargs):
                start = time.time()
                
                try:
                    result = func(*args, **kwargs)
                    
                    # Записываем успешное выполнение
                    duration = time.time() - start
                    self.collector.record_histogram(
                        f'function.{func_name}.duration',
                        duration
                    )
                    self.collector.increment_counter(
                        f'function.{func_name}.calls',
                        tags={'status': 'success'}
                    )
                    
                    return result
                    
                except Exception as e:
                    # Записываем ошибку
                    duration = time.time() - start
                    self.collector.record_histogram(
                        f'function.{func_name}.duration',
                        duration
                    )
                    self.collector.increment_counter(
                        f'function.{func_name}.calls',
                        tags={'status': 'error'}
                    )
                    raise
            
            return wrapper
        return decorator


# Глобальные экземпляры
metrics_collector = MetricsCollector()
request_metrics = RequestMetrics(metrics_collector)
business_metrics = BusinessMetrics(metrics_collector)
performance_monitor = PerformanceMonitor(metrics_collector)
