"""
Unified Cache System - объединенная система кэширования
Многоуровневое кэширование с поддержкой Redis, in-memory и тегирования
"""
import redis
import pickle
import json
import hashlib
import logging
import time
from functools import wraps
from typing import Any, Optional, List, Callable, Dict
from collections import OrderedDict

logger = logging.getLogger(__name__)


class UnifiedCache:
    """
    Унифицированная система кэширования с поддержкой:
    - L1 (In-memory) - быстрый, ограниченный
    - L2 (Redis) - распределенный, персистентный
    - Автоматическая инвалидация по тегам и паттернам
    - LFU eviction для L1
    - Статистика и мониторинг
    """
    
    def __init__(self, redis_url: str = 'redis://localhost:6379/0', 
                 l1_max_size: int = 1000,
                 default_timeout: int = 300):
        self.default_timeout = default_timeout
        self.l1_max_size = l1_max_size
        
        # L1 Cache (In-memory) с LFU
        self.l1_cache = OrderedDict()
        self.l1_access_count = {}
        
        # L2 Cache (Redis)
        self.redis_client = None
        self.redis_available = False
        
        # Статистика
        self.stats = {
            'l1_hits': 0,
            'l2_hits': 0,
            'misses': 0,
            'sets': 0,
            'deletes': 0,
            'evictions': 0
        }
        
        # Инициализация Redis
        self._init_redis(redis_url)
    
    def _init_redis(self, redis_url: str):
        """Инициализация Redis с fallback"""
        try:
            self.redis_client = redis.from_url(redis_url, decode_responses=False)
            self.redis_client.ping()
            self.redis_available = True
            logger.info(f"Redis cache initialized: {redis_url}")
        except Exception as e:
            logger.warning(f"Redis unavailable, using L1 only: {e}")
            self.redis_available = False
    
    def _evict_l1_if_needed(self):
        """Вытеснение из L1 при превышении размера (LFU)"""
        if len(self.l1_cache) >= self.l1_max_size:
            if self.l1_access_count:
                # Удаляем наименее часто используемый элемент
                least_used = min(self.l1_access_count, key=self.l1_access_count.get)
                self.l1_cache.pop(least_used, None)
                self.l1_access_count.pop(least_used, None)
                self.stats['evictions'] += 1
    
    def get(self, key: str) -> Optional[Any]:
        """Получить значение из кэша (проверяет L1, затем L2)"""
        start_time = time.time()
        
        # L1 - In-memory
        if key in self.l1_cache:
            self.l1_access_count[key] = self.l1_access_count.get(key, 0) + 1
            self.stats['l1_hits'] += 1
            elapsed = time.time() - start_time
            if elapsed > 0.01:
                logger.debug(f"L1 hit: {key} ({elapsed:.3f}s)")
            return self.l1_cache[key]
        
        # L2 - Redis
        if self.redis_available:
            try:
                value = self.redis_client.get(key)
                if value:
                    try:
                        deserialized = pickle.loads(value)
                        # Продвигаем в L1
                        self._evict_l1_if_needed()
                        self.l1_cache[key] = deserialized
                        self.l1_access_count[key] = 1
                        self.stats['l2_hits'] += 1
                        
                        elapsed = time.time() - start_time
                        if elapsed > 0.1:
                            logger.warning(f"Slow L2 hit: {key} ({elapsed:.3f}s)")
                        return deserialized
                    except (pickle.UnpicklingError, TypeError) as e:
                        logger.warning(f"Failed to deserialize cached value for {key}: {e}")
                        self.redis_client.delete(key)
            except Exception as e:
                logger.error(f"L2 cache error: {e}")
        
        self.stats['misses'] += 1
        return None
    
    def set(self, key: str, value: Any, timeout: Optional[int] = None, 
            tags: Optional[List[str]] = None):
        """Установить значение в кэш"""
        if timeout is None:
            timeout = self.default_timeout
        
        start_time = time.time()
        
        # L1 - In-memory
        self._evict_l1_if_needed()
        self.l1_cache[key] = value
        self.l1_access_count[key] = 0
        
        # L2 - Redis
        if self.redis_available:
            try:
                serialized = pickle.dumps(value)
                self.redis_client.setex(key, timeout, serialized)
                
                # Регистрируем теги
                if tags:
                    for tag in tags:
                        tag_key = f"tag:{tag}"
                        self.redis_client.sadd(tag_key, key)
                        self.redis_client.expire(tag_key, timeout)
                
                elapsed = time.time() - start_time
                if elapsed > 0.1:
                    logger.warning(f"Slow cache set: {key} ({elapsed:.3f}s)")
            except (pickle.PicklingError, TypeError) as e:
                logger.warning(f"Failed to serialize value for {key}: {e}")
            except Exception as e:
                logger.error(f"L2 cache set error: {e}")
        
        self.stats['sets'] += 1
    
    def delete(self, key: str):
        """Удалить значение из всех уровней кэша"""
        # L1
        self.l1_cache.pop(key, None)
        self.l1_access_count.pop(key, None)
        
        # L2
        if self.redis_available:
            try:
                self.redis_client.delete(key)
            except Exception as e:
                logger.error(f"L2 cache delete error: {e}")
        
        self.stats['deletes'] += 1
    
    def invalidate_by_tag(self, tag: str):
        """Инвалидировать все ключи с определенным тегом"""
        if not self.redis_available:
            # Для L1 очищаем все (упрощенная версия)
            self.l1_cache.clear()
            self.l1_access_count.clear()
            return
        
        try:
            tag_key = f"tag:{tag}"
            keys = self.redis_client.smembers(tag_key)
            
            if keys:
                # Удаляем из L1
                for key in keys:
                    key_str = key.decode() if isinstance(key, bytes) else key
                    self.l1_cache.pop(key_str, None)
                    self.l1_access_count.pop(key_str, None)
                
                # Удаляем из L2
                self.redis_client.delete(*keys)
                self.redis_client.delete(tag_key)
                
                logger.info(f"Invalidated {len(keys)} keys with tag '{tag}'")
        except Exception as e:
            logger.error(f"Tag invalidation error: {e}")
    
    def invalidate_by_pattern(self, pattern: str):
        """Инвалидировать ключи по паттерну"""
        if not self.redis_available:
            self.l1_cache.clear()
            self.l1_access_count.clear()
            return
        
        try:
            keys = self.redis_client.keys(pattern)
            if keys:
                # Удаляем из L1
                for key in keys:
                    key_str = key.decode() if isinstance(key, bytes) else key
                    self.l1_cache.pop(key_str, None)
                    self.l1_access_count.pop(key_str, None)
                
                # Удаляем из L2
                self.redis_client.delete(*keys)
                logger.info(f"Invalidated {len(keys)} keys matching '{pattern}'")
        except Exception as e:
            logger.error(f"Pattern invalidation error: {e}")
    
    def clear(self):
        """Очистить весь кэш"""
        self.l1_cache.clear()
        self.l1_access_count.clear()
        
        if self.redis_available:
            try:
                self.redis_client.flushdb()
            except Exception as e:
                logger.error(f"Cache clear error: {e}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Получить статистику кэша"""
        total_requests = self.stats['l1_hits'] + self.stats['l2_hits'] + self.stats['misses']
        hit_rate = ((self.stats['l1_hits'] + self.stats['l2_hits']) / total_requests * 100) if total_requests > 0 else 0
        
        stats = {
            **self.stats,
            'total_requests': total_requests,
            'hit_rate': round(hit_rate, 2),
            'l1': {
                'size': len(self.l1_cache),
                'max_size': self.l1_max_size,
                'utilization': round(len(self.l1_cache) / self.l1_max_size * 100, 2)
            }
        }
        
        if self.redis_available:
            try:
                info = self.redis_client.info()
                stats['l2'] = {
                    'keys': self.redis_client.dbsize(),
                    'used_memory': info.get('used_memory_human'),
                    'connected': True
                }
            except Exception as e:
                logger.error(f"Stats error: {e}")
                stats['l2'] = {'connected': False}
        else:
            stats['l2'] = {'connected': False}
        
        return stats
    
    def bulk_get(self, keys: List[str]) -> Dict[str, Any]:
        """Массовое получение значений"""
        results = {}
        
        # Проверяем L1
        for key in keys:
            if key in self.l1_cache:
                self.l1_access_count[key] = self.l1_access_count.get(key, 0) + 1
                results[key] = self.l1_cache[key]
                self.stats['l1_hits'] += 1
        
        # Для остальных проверяем L2
        if self.redis_available:
            missing_keys = [k for k in keys if k not in results]
            if missing_keys:
                try:
                    pipe = self.redis_client.pipeline()
                    for key in missing_keys:
                        pipe.get(key)
                    
                    values = pipe.execute()
                    
                    for i, key in enumerate(missing_keys):
                        value = values[i]
                        if value:
                            try:
                                deserialized = pickle.loads(value)
                                self._evict_l1_if_needed()
                                self.l1_cache[key] = deserialized
                                self.l1_access_count[key] = 1
                                results[key] = deserialized
                                self.stats['l2_hits'] += 1
                            except (pickle.UnpicklingError, TypeError):
                                continue
                        else:
                            self.stats['misses'] += 1
                except Exception as e:
                    logger.error(f"Bulk get error: {e}")
        
        return results
    
    def bulk_set(self, data: Dict[str, Any], timeout: Optional[int] = None, 
                 tags: Optional[List[str]] = None):
        """Массовая установка значений"""
        if not data:
            return
        
        if timeout is None:
            timeout = self.default_timeout
        
        # L1
        for key, value in data.items():
            self._evict_l1_if_needed()
            self.l1_cache[key] = value
            self.l1_access_count[key] = 0
        
        # L2
        if self.redis_available:
            try:
                pipe = self.redis_client.pipeline()
                for key, value in data.items():
                    try:
                        serialized = pickle.dumps(value)
                        pipe.setex(key, timeout, serialized)
                        
                        if tags:
                            for tag in tags:
                                tag_key = f"tag:{tag}"
                                pipe.sadd(tag_key, key)
                                pipe.expire(tag_key, timeout)
                    except (pickle.PicklingError, TypeError):
                        continue
                
                pipe.execute()
                self.stats['sets'] += len(data)
            except Exception as e:
                logger.error(f"Bulk set error: {e}")


# Глобальный экземпляр
cache = UnifiedCache()


# Декораторы
def cached(timeout: int = 300, tags: Optional[List[str]] = None, key_prefix: str = 'cache'):
    """
    Декоратор для кэширования результатов функций
    
    Args:
        timeout: Время жизни кэша в секундах
        tags: Теги для группировки и инвалидации
        key_prefix: Префикс ключа кэша
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Генерируем ключ кэша
            key_parts = [key_prefix, func.__name__]
            
            if args:
                key_parts.append(hashlib.md5(str(args).encode()).hexdigest()[:8])
            if kwargs:
                key_parts.append(hashlib.md5(str(sorted(kwargs.items())).encode()).hexdigest()[:8])
            
            cache_key = ':'.join(key_parts)
            
            # Проверяем кэш
            result = cache.get(cache_key)
            if result is not None:
                return result
            
            # Выполняем функцию
            result = func(*args, **kwargs)
            
            # Кэшируем результат
            cache.set(cache_key, result, timeout, tags)
            
            return result
        return wrapper
    return decorator


def invalidate_cache(tags: Optional[List[str]] = None, pattern: Optional[str] = None):
    """
    Декоратор для автоматической инвалидации кэша после выполнения функции
    
    Args:
        tags: Теги для инвалидации
        pattern: Паттерн ключей для инвалидации
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            
            if tags:
                for tag in tags:
                    cache.invalidate_by_tag(tag)
            
            if pattern:
                cache.invalidate_by_pattern(pattern)
            
            return result
        return wrapper
    return decorator


# Специализированные менеджеры кэша
class TournamentCache:
    """Менеджер кэша для турниров"""
    
    @staticmethod
    @cached(timeout=600, tags=['tournaments'], key_prefix='tournaments')
    def get_all(filters: Optional[Dict] = None):
        """Получить все турниры с кэшированием"""
        from app.models.tournament import Tournament
        query = Tournament.query
        
        if filters:
            if 'category' in filters:
                query = query.filter(Tournament.category == filters['category'])
            if 'status' in filters:
                query = query.filter(Tournament.status == filters['status'])
            if 'location' in filters:
                query = query.filter(Tournament.location.contains(filters['location']))
        
        return query.all()
    
    @staticmethod
    @cached(timeout=1800, tags=['tournaments'], key_prefix='tournament')
    def get_by_id(tournament_id: int):
        """Получить турнир по ID с кэшированием"""
        from app.models.tournament import Tournament
        return Tournament.query.get(tournament_id)
    
    @staticmethod
    @cached(timeout=3600, tags=['tournaments', 'stats'], key_prefix='tournaments_stats')
    def get_stats():
        """Получить статистику турниров"""
        from app.models.tournament import Tournament
        from sqlalchemy import func
        from app import db
        
        return {
            'total': Tournament.query.count(),
            'by_status': dict(db.session.query(Tournament.status, func.count(Tournament.id))
                            .group_by(Tournament.status).all()),
            'by_category': dict(db.session.query(Tournament.category, func.count(Tournament.id))
                              .group_by(Tournament.category).all())
        }
    
    @staticmethod
    @invalidate_cache(tags=['tournaments'])
    def invalidate_all():
        """Инвалидировать весь кэш турниров"""
        logger.info("Tournament cache invalidated")
    
    @staticmethod
    def invalidate_tournament(tournament_id: int):
        """Инвалидировать кэш конкретного турнира"""
        cache.invalidate_by_pattern(f'tournament:get_by_id:*')
        cache.invalidate_by_tag('tournaments')


class UserCache:
    """Менеджер кэша для пользователей"""
    
    @staticmethod
    @cached(timeout=900, tags=['users'], key_prefix='user')
    def get_by_id(user_id: int):
        """Получить пользователя по ID с кэшированием"""
        from app.models.user import User
        return User.query.get(user_id)
    
    @staticmethod
    def invalidate_user(user_id: int):
        """Инвалидировать кэш пользователя"""
        cache.invalidate_by_pattern(f'user:get_by_id:*')
        cache.invalidate_by_tag('users')
