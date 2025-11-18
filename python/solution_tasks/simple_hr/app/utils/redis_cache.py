"""
Redis кэширование для Simple HR
Опциональная зависимость - работает с fallback на память
"""

import json
import logging
from functools import wraps
from typing import Any, Optional, Callable
from datetime import timedelta

logger = logging.getLogger(__name__)

# Попытка импорта Redis
try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    logger.warning("Redis не установлен. Используется fallback кэш в памяти")


class MemoryCache:
    """Простой кэш в памяти как fallback"""
    
    def __init__(self):
        self._cache = {}
        self._expiry = {}
    
    def get(self, key: str) -> Optional[str]:
        """Получить значение из кэша"""
        import time
        
        if key in self._cache:
            # Проверка срока действия
            if key in self._expiry and time.time() > self._expiry[key]:
                del self._cache[key]
                del self._expiry[key]
                return None
            return self._cache[key]
        return None
    
    def set(self, key: str, value: str, ex: int = 300):
        """Сохранить значение в кэш"""
        import time
        
        self._cache[key] = value
        if ex:
            self._expiry[key] = time.time() + ex
    
    def delete(self, key: str):
        """Удалить значение из кэша"""
        if key in self._cache:
            del self._cache[key]
        if key in self._expiry:
            del self._expiry[key]
    
    def exists(self, key: str) -> bool:
        """Проверить существование ключа"""
        return self.get(key) is not None
    
    def flushdb(self):
        """Очистить весь кэш"""
        self._cache.clear()
        self._expiry.clear()
    
    def keys(self, pattern: str = '*'):
        """Получить список ключей по паттерну"""
        if pattern == '*':
            return list(self._cache.keys())
        
        # Простая поддержка паттернов
        import re
        regex = re.compile(pattern.replace('*', '.*'))
        return [k for k in self._cache.keys() if regex.match(k)]


class CacheManager:
    """Менеджер кэширования с автоматическим fallback"""
    
    def __init__(self, app=None):
        self.redis_client: Optional[redis.Redis] = None
        self.memory_cache = MemoryCache()
        self.enabled = False
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Инициализация с Flask приложением"""
        redis_url = app.config.get('REDIS_URL', 'redis://localhost:6379/0')
        
        if REDIS_AVAILABLE:
            try:
                self.redis_client = redis.from_url(
                    redis_url,
                    decode_responses=True,
                    socket_connect_timeout=1,
                    socket_timeout=1
                )
                # Проверка подключения
                try:
                    self.redis_client.ping()
                    self.enabled = True
                    logger.info(f"Redis подключен: {redis_url}")
                except (redis.exceptions.ConnectionError, redis.exceptions.TimeoutError, TimeoutError):
                    logger.warning(f"Не удалось подключиться к Redis (timeout). Используется fallback")
                    self.redis_client = None
                    self.enabled = True  # Включаем с memory cache
            except Exception as e:
                logger.warning(f"Не удалось подключиться к Redis: {e}. Используется fallback")
                self.redis_client = None
                self.enabled = True  # Включаем с memory cache
        else:
            self.enabled = True
            logger.info("Используется fallback кэш в памяти")
    
    @property
    def client(self):
        """Получить активный клиент кэша"""
        return self.redis_client if self.redis_client else self.memory_cache
    
    def get(self, key: str) -> Optional[Any]:
        """Получить значение из кэша"""
        if not self.enabled:
            return None
        
        try:
            value = self.client.get(key)
            if value:
                # Попытка десериализации JSON
                try:
                    return json.loads(value)
                except (json.JSONDecodeError, TypeError):
                    return value
            return None
        except Exception as e:
            logger.error(f"Ошибка чтения из кэша {key}: {e}")
            return None
    
    def set(self, key: str, value: Any, timeout: int = 300):
        """Сохранить значение в кэш"""
        if not self.enabled:
            return False
        
        try:
            # Сериализация в JSON если не строка
            if not isinstance(value, str):
                value = json.dumps(value, ensure_ascii=False, default=str)
            
            self.client.set(key, value, ex=timeout)
            return True
        except Exception as e:
            logger.error(f"Ошибка записи в кэш {key}: {e}")
            return False
    
    def delete(self, key: str):
        """Удалить значение из кэша"""
        if not self.enabled:
            return False
        
        try:
            self.client.delete(key)
            return True
        except Exception as e:
            logger.error(f"Ошибка удаления из кэша {key}: {e}")
            return False
    
    def exists(self, key: str) -> bool:
        """Проверить существование ключа"""
        if not self.enabled:
            return False
        
        try:
            return bool(self.client.exists(key))
        except Exception as e:
            logger.error(f"Ошибка проверки существования {key}: {e}")
            return False
    
    def clear_pattern(self, pattern: str):
        """Очистить ключи по паттерну"""
        if not self.enabled:
            return 0
        
        try:
            keys = self.client.keys(pattern)
            if keys:
                return self.client.delete(*keys) if self.redis_client else len([self.client.delete(k) for k in keys])
            return 0
        except Exception as e:
            logger.error(f"Ошибка очистки по паттерну {pattern}: {e}")
            return 0
    
    def flush_all(self):
        """Очистить весь кэш"""
        if not self.enabled:
            return False
        
        try:
            self.client.flushdb()
            logger.info("Кэш полностью очищен")
            return True
        except Exception as e:
            logger.error(f"Ошибка очистки кэша: {e}")
            return False
    
    def get_stats(self) -> dict:
        """Получить статистику кэша"""
        if not self.enabled:
            return {'enabled': False}
        
        try:
            if self.redis_client:
                info = self.redis_client.info('stats')
                return {
                    'enabled': True,
                    'type': 'redis',
                    'keys': self.redis_client.dbsize(),
                    'hits': info.get('keyspace_hits', 0),
                    'misses': info.get('keyspace_misses', 0),
                    'memory_used': self.redis_client.info('memory').get('used_memory_human', 'N/A')
                }
            else:
                return {
                    'enabled': True,
                    'type': 'memory',
                    'keys': len(self.memory_cache._cache)
                }
        except Exception as e:
            logger.error(f"Ошибка получения статистики: {e}")
            return {'enabled': False, 'error': str(e)}


# Глобальный экземпляр
cache = CacheManager()


def cached(timeout: int = 300, key_prefix: str = 'view'):
    """
    Декоратор для кэширования результатов функций
    
    Args:
        timeout: Время жизни кэша в секундах
        key_prefix: Префикс для ключа кэша
    """
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Формирование ключа кэша
            cache_key = f"{key_prefix}:{f.__name__}"
            
            # Добавление аргументов в ключ
            if args:
                cache_key += ':' + ':'.join(str(arg) for arg in args)
            if kwargs:
                cache_key += ':' + ':'.join(f"{k}={v}" for k, v in sorted(kwargs.items()))
            
            # Попытка получить из кэша
            cached_value = cache.get(cache_key)
            if cached_value is not None:
                logger.debug(f"Cache hit: {cache_key}")
                return cached_value
            
            # Вычисление и сохранение в кэш
            logger.debug(f"Cache miss: {cache_key}")
            result = f(*args, **kwargs)
            cache.set(cache_key, result, timeout)
            
            return result
        
        return decorated_function
    return decorator


def invalidate_cache(pattern: str):
    """
    Инвалидация кэша по паттерну
    
    Args:
        pattern: Паттерн для поиска ключей (например, 'view:employees:*')
    """
    count = cache.clear_pattern(pattern)
    logger.info(f"Инвалидировано {count} ключей по паттерну {pattern}")
    return count


def cache_stats() -> dict:
    """Получить статистику использования кэша"""
    return cache.get_stats()
