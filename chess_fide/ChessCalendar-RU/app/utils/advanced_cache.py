"""
Расширенная система кэширования с Redis и fallback на память
"""
import json
import logging
from functools import wraps
from datetime import timedelta
import hashlib

logger = logging.getLogger(__name__)


class AdvancedCache:
    """Расширенная система кэширования"""
    
    def __init__(self, app=None):
        self.app = app
        self.redis_client = None
        self.memory_cache = {}
        self.cache_stats = {
            'hits': 0,
            'misses': 0,
            'sets': 0,
            'deletes': 0
        }
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Инициализация кэша"""
        try:
            import redis
            redis_url = app.config.get('REDIS_URL', 'redis://localhost:6379/0')
            self.redis_client = redis.from_url(redis_url, decode_responses=True)
            self.redis_client.ping()
            logger.info("Redis cache initialized successfully")
        except Exception as e:
            logger.warning(f"Redis not available, using memory cache: {e}")
            self.redis_client = None
    
    def _generate_key(self, prefix, *args, **kwargs):
        """Генерация ключа кэша"""
        key_parts = [prefix]
        key_parts.extend(str(arg) for arg in args)
        key_parts.extend(f"{k}:{v}" for k, v in sorted(kwargs.items()))
        key_string = ":".join(key_parts)
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def get(self, key):
        """Получить значение из кэша"""
        try:
            if self.redis_client:
                value = self.redis_client.get(key)
                if value:
                    self.cache_stats['hits'] += 1
                    return json.loads(value)
            else:
                if key in self.memory_cache:
                    self.cache_stats['hits'] += 1
                    return self.memory_cache[key]
            
            self.cache_stats['misses'] += 1
            return None
        except Exception as e:
            logger.error(f"Cache get error: {e}")
            return None
    
    def set(self, key, value, ttl=300):
        """Установить значение в кэш"""
        try:
            serialized = json.dumps(value)
            
            if self.redis_client:
                self.redis_client.setex(key, ttl, serialized)
            else:
                self.memory_cache[key] = value
            
            self.cache_stats['sets'] += 1
            return True
        except Exception as e:
            logger.error(f"Cache set error: {e}")
            return False
    
    def delete(self, key):
        """Удалить значение из кэша"""
        try:
            if self.redis_client:
                self.redis_client.delete(key)
            else:
                self.memory_cache.pop(key, None)
            
            self.cache_stats['deletes'] += 1
            return True
        except Exception as e:
            logger.error(f"Cache delete error: {e}")
            return False
    
    def clear(self, pattern=None):
        """Очистить кэш"""
        try:
            if self.redis_client:
                if pattern:
                    keys = self.redis_client.keys(pattern)
                    if keys:
                        self.redis_client.delete(*keys)
                else:
                    self.redis_client.flushdb()
            else:
                if pattern:
                    keys_to_delete = [k for k in self.memory_cache.keys() if pattern in k]
                    for key in keys_to_delete:
                        del self.memory_cache[key]
                else:
                    self.memory_cache.clear()
            
            logger.info(f"Cache cleared: {pattern or 'all'}")
            return True
        except Exception as e:
            logger.error(f"Cache clear error: {e}")
            return False
    
    def get_stats(self):
        """Получить статистику кэша"""
        total_requests = self.cache_stats['hits'] + self.cache_stats['misses']
        hit_rate = (self.cache_stats['hits'] / total_requests * 100) if total_requests > 0 else 0
        
        stats = {
            **self.cache_stats,
            'total_requests': total_requests,
            'hit_rate': round(hit_rate, 2),
            'backend': 'redis' if self.redis_client else 'memory'
        }
        
        if self.redis_client:
            try:
                info = self.redis_client.info('memory')
                stats['memory_used'] = info.get('used_memory_human', 'N/A')
                stats['keys_count'] = self.redis_client.dbsize()
            except:
                pass
        else:
            stats['keys_count'] = len(self.memory_cache)
        
        return stats


def cached(ttl=300, key_prefix='cache'):
    """Декоратор для кэширования результатов функций"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Генерация ключа кэша
            cache_key = f"{key_prefix}:{f.__name__}:{args}:{kwargs}"
            
            # Попытка получить из кэша
            cached_value = advanced_cache.get(cache_key)
            if cached_value is not None:
                logger.debug(f"Cache hit: {cache_key}")
                return cached_value
            
            # Выполнение функции
            result = f(*args, **kwargs)
            
            # Сохранение в кэш
            advanced_cache.set(cache_key, result, ttl)
            logger.debug(f"Cache set: {cache_key}")
            
            return result
        
        return decorated_function
    return decorator


def invalidate_cache(pattern):
    """Декоратор для инвалидации кэша после выполнения функции"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            result = f(*args, **kwargs)
            advanced_cache.clear(pattern)
            logger.info(f"Cache invalidated: {pattern}")
            return result
        return decorated_function
    return decorator


# Глобальный экземпляр
advanced_cache = AdvancedCache()
