"""
Продвинутые стратегии кэширования
"""
import logging
import time
import hashlib
import pickle
from typing import Any, Optional, Callable, List
from functools import wraps
from datetime import datetime, timedelta
import redis

logger = logging.getLogger(__name__)


class CacheStrategy:
    """Базовая стратегия кэширования"""
    
    def __init__(self, redis_client: redis.Redis, ttl: int = 300):
        self.redis = redis_client
        self.ttl = ttl
    
    def get(self, key: str) -> Optional[Any]:
        """Получить значение из кэша"""
        raise NotImplementedError
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """Установить значение в кэш"""
        raise NotImplementedError
    
    def delete(self, key: str):
        """Удалить значение из кэша"""
        raise NotImplementedError
    
    def clear(self, pattern: str = "*"):
        """Очистить кэш по паттерну"""
        raise NotImplementedError


class SimpleCacheStrategy(CacheStrategy):
    """Простая стратегия кэширования"""
    
    def get(self, key: str) -> Optional[Any]:
        try:
            value = self.redis.get(key)
            if value:
                return pickle.loads(value)
            return None
        except Exception as e:
            logger.error(f"Cache get error: {e}")
            return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        try:
            ttl = ttl or self.ttl
            serialized = pickle.dumps(value)
            self.redis.setex(key, ttl, serialized)
        except Exception as e:
            logger.error(f"Cache set error: {e}")
    
    def delete(self, key: str):
        try:
            self.redis.delete(key)
        except Exception as e:
            logger.error(f"Cache delete error: {e}")
    
    def clear(self, pattern: str = "*"):
        try:
            keys = self.redis.keys(pattern)
            if keys:
                self.redis.delete(*keys)
        except Exception as e:
            logger.error(f"Cache clear error: {e}")


class WriteThrough(CacheStrategy):
    """
    Write-Through кэширование
    Данные записываются одновременно в кэш и БД
    """
    
    def __init__(self, redis_client: redis.Redis, db_writer: Callable, ttl: int = 300):
        super().__init__(redis_client, ttl)
        self.db_writer = db_writer
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        try:
            # Записываем в БД
            self.db_writer(key, value)
            
            # Записываем в кэш
            ttl = ttl or self.ttl
            serialized = pickle.dumps(value)
            self.redis.setex(key, ttl, serialized)
            
            logger.debug(f"Write-through: {key}")
        except Exception as e:
            logger.error(f"Write-through error: {e}")
            raise
    
    def get(self, key: str) -> Optional[Any]:
        try:
            value = self.redis.get(key)
            if value:
                return pickle.loads(value)
            return None
        except Exception as e:
            logger.error(f"Cache get error: {e}")
            return None
    
    def delete(self, key: str):
        try:
            self.redis.delete(key)
        except Exception as e:
            logger.error(f"Cache delete error: {e}")
    
    def clear(self, pattern: str = "*"):
        try:
            keys = self.redis.keys(pattern)
            if keys:
                self.redis.delete(*keys)
        except Exception as e:
            logger.error(f"Cache clear error: {e}")


class WriteBack(CacheStrategy):
    """
    Write-Back (Write-Behind) кэширование
    Данные записываются в кэш, в БД асинхронно
    """
    
    def __init__(
        self,
        redis_client: redis.Redis,
        db_writer: Callable,
        ttl: int = 300,
        flush_interval: int = 60
    ):
        super().__init__(redis_client, ttl)
        self.db_writer = db_writer
        self.flush_interval = flush_interval
        self.dirty_keys = set()
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        try:
            # Записываем в кэш
            ttl = ttl or self.ttl
            serialized = pickle.dumps(value)
            self.redis.setex(key, ttl, serialized)
            
            # Помечаем как "грязный"
            self.dirty_keys.add(key)
            
            # Сохраняем в список для отложенной записи
            self.redis.sadd('dirty_keys', key)
            
            logger.debug(f"Write-back: {key} marked dirty")
        except Exception as e:
            logger.error(f"Write-back error: {e}")
    
    def flush(self):
        """Записать все грязные ключи в БД"""
        try:
            dirty_keys = self.redis.smembers('dirty_keys')
            
            for key in dirty_keys:
                key_str = key.decode() if isinstance(key, bytes) else key
                value = self.get(key_str)
                
                if value is not None:
                    try:
                        self.db_writer(key_str, value)
                        self.redis.srem('dirty_keys', key)
                        logger.debug(f"Flushed: {key_str}")
                    except Exception as e:
                        logger.error(f"Failed to flush {key_str}: {e}")
            
            logger.info(f"Flushed {len(dirty_keys)} keys to database")
        except Exception as e:
            logger.error(f"Flush error: {e}")
    
    def get(self, key: str) -> Optional[Any]:
        try:
            value = self.redis.get(key)
            if value:
                return pickle.loads(value)
            return None
        except Exception as e:
            logger.error(f"Cache get error: {e}")
            return None
    
    def delete(self, key: str):
        try:
            self.redis.delete(key)
            self.redis.srem('dirty_keys', key)
        except Exception as e:
            logger.error(f"Cache delete error: {e}")
    
    def clear(self, pattern: str = "*"):
        try:
            keys = self.redis.keys(pattern)
            if keys:
                self.redis.delete(*keys)
        except Exception as e:
            logger.error(f"Cache clear error: {e}")


class CacheAside(CacheStrategy):
    """
    Cache-Aside (Lazy Loading)
    Приложение проверяет кэш, если нет - загружает из БД
    """
    
    def __init__(self, redis_client: redis.Redis, db_loader: Callable, ttl: int = 300):
        super().__init__(redis_client, ttl)
        self.db_loader = db_loader
    
    def get(self, key: str) -> Optional[Any]:
        try:
            # Проверяем кэш
            value = self.redis.get(key)
            if value:
                logger.debug(f"Cache hit: {key}")
                return pickle.loads(value)
            
            # Загружаем из БД
            logger.debug(f"Cache miss: {key}")
            value = self.db_loader(key)
            
            if value is not None:
                # Сохраняем в кэш
                self.set(key, value)
            
            return value
        except Exception as e:
            logger.error(f"Cache-aside get error: {e}")
            return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        try:
            ttl = ttl or self.ttl
            serialized = pickle.dumps(value)
            self.redis.setex(key, ttl, serialized)
        except Exception as e:
            logger.error(f"Cache set error: {e}")
    
    def delete(self, key: str):
        try:
            self.redis.delete(key)
        except Exception as e:
            logger.error(f"Cache delete error: {e}")
    
    def clear(self, pattern: str = "*"):
        try:
            keys = self.redis.keys(pattern)
            if keys:
                self.redis.delete(*keys)
        except Exception as e:
            logger.error(f"Cache clear error: {e}")


class MultiLevelCache:
    """
    Многоуровневое кэширование
    L1: In-Memory (быстрый, маленький)
    L2: Redis (средний, большой)
    """
    
    def __init__(
        self,
        redis_client: redis.Redis,
        l1_size: int = 100,
        l1_ttl: int = 60,
        l2_ttl: int = 300
    ):
        self.redis = redis_client
        self.l1_cache = {}  # In-memory cache
        self.l1_access_times = {}
        self.l1_size = l1_size
        self.l1_ttl = l1_ttl
        self.l2_ttl = l2_ttl
    
    def get(self, key: str) -> Optional[Any]:
        # Проверяем L1
        if key in self.l1_cache:
            # Проверяем TTL
            if time.time() - self.l1_access_times[key] < self.l1_ttl:
                logger.debug(f"L1 cache hit: {key}")
                return self.l1_cache[key]
            else:
                # Истек TTL
                del self.l1_cache[key]
                del self.l1_access_times[key]
        
        # Проверяем L2 (Redis)
        try:
            value = self.redis.get(key)
            if value:
                logger.debug(f"L2 cache hit: {key}")
                deserialized = pickle.loads(value)
                
                # Продвигаем в L1
                self._promote_to_l1(key, deserialized)
                
                return deserialized
        except Exception as e:
            logger.error(f"L2 cache error: {e}")
        
        logger.debug(f"Cache miss: {key}")
        return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        # Записываем в L1
        self._promote_to_l1(key, value)
        
        # Записываем в L2
        try:
            ttl = ttl or self.l2_ttl
            serialized = pickle.dumps(value)
            self.redis.setex(key, ttl, serialized)
        except Exception as e:
            logger.error(f"L2 cache set error: {e}")
    
    def _promote_to_l1(self, key: str, value: Any):
        """Продвинуть значение в L1 кэш"""
        # Проверяем размер L1
        if len(self.l1_cache) >= self.l1_size:
            # Удаляем самый старый элемент (LRU)
            oldest_key = min(self.l1_access_times, key=self.l1_access_times.get)
            del self.l1_cache[oldest_key]
            del self.l1_access_times[oldest_key]
        
        self.l1_cache[key] = value
        self.l1_access_times[key] = time.time()
    
    def delete(self, key: str):
        # Удаляем из L1
        if key in self.l1_cache:
            del self.l1_cache[key]
            del self.l1_access_times[key]
        
        # Удаляем из L2
        try:
            self.redis.delete(key)
        except Exception as e:
            logger.error(f"Cache delete error: {e}")
    
    def clear(self):
        """Очистить все уровни кэша"""
        self.l1_cache.clear()
        self.l1_access_times.clear()
        
        try:
            self.redis.flushdb()
        except Exception as e:
            logger.error(f"Cache clear error: {e}")
    
    def get_stats(self) -> dict:
        """Получить статистику кэша"""
        return {
            'l1_size': len(self.l1_cache),
            'l1_max_size': self.l1_size,
            'l2_keys': self.redis.dbsize() if self.redis else 0
        }


def cache_with_strategy(
    strategy: str = 'simple',
    ttl: int = 300,
    key_prefix: str = 'cache'
):
    """
    Декоратор для кэширования с выбором стратегии
    
    Args:
        strategy: стратегия (simple, cache_aside, multi_level)
        ttl: время жизни
        key_prefix: префикс ключа
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Генерируем ключ
            key_parts = [key_prefix, func.__name__]
            key_parts.extend(str(arg) for arg in args)
            key_parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))
            
            cache_key = ':'.join(key_parts)
            cache_key = hashlib.md5(cache_key.encode()).hexdigest()
            
            # Получаем стратегию кэширования
            from flask import current_app
            import redis
            
            redis_url = current_app.config.get('REDIS_URL', 'redis://localhost:6379/0')
            redis_client = redis.from_url(redis_url)
            
            if strategy == 'simple':
                cache = SimpleCacheStrategy(redis_client, ttl)
            elif strategy == 'cache_aside':
                cache = CacheAside(redis_client, lambda k: None, ttl)
            elif strategy == 'multi_level':
                cache = MultiLevelCache(redis_client, l2_ttl=ttl)
            else:
                cache = SimpleCacheStrategy(redis_client, ttl)
            
            # Проверяем кэш
            cached_value = cache.get(cache_key)
            if cached_value is not None:
                return cached_value
            
            # Выполняем функцию
            result = func(*args, **kwargs)
            
            # Сохраняем в кэш
            cache.set(cache_key, result)
            
            return result
        
        return wrapper
    return decorator
