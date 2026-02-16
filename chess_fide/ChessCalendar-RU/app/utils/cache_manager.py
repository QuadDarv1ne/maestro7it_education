"""
Улучшенная система кэширования с поддержкой:
- Автоматической инвалидации
- Тегирования кэша
- CDN интеграции
- Многоуровневого кэширования
"""
import redis
import pickle
import hashlib
import logging
import os
import requests
from datetime import timedelta
from functools import wraps
from typing import Any, Optional, List, Callable
import time

logger = logging.getLogger(__name__)

class CacheInvalidationStrategy:
    """Стратегии инвалидации кэша"""
    
    @staticmethod
    def time_based(timeout: int):
        """Инвалидация по времени"""
        return {'type': 'time', 'timeout': timeout}
    
    @staticmethod
    def tag_based(tags: List[str]):
        """Инвалидация по тегам"""
        return {'type': 'tags', 'tags': tags}
    
    @staticmethod
    def dependency_based(dependencies: List[str]):
        """Инвалидация по зависимостям"""
        return {'type': 'dependencies', 'deps': dependencies}

class MultiLevelCache:
    """
    Многоуровневая система кэширования:
    L1 - In-memory (быстрый, ограниченный)
    L2 - Redis (средний, распределенный)
    L3 - CDN (медленный, глобальный)
    """
    
    def __init__(self, redis_url: str = 'redis://localhost:6379/0', 
                 l1_max_size: int = 1000,
                 enable_cdn: bool = False):
        self.l1_cache = {}  # In-memory cache
        self.l1_max_size = l1_max_size
        self.l1_access_count = {}
        self.enable_cdn = enable_cdn
        
        # Redis (L2)
        try:
            self.redis_client = redis.from_url(redis_url, decode_responses=False)
            self.redis_client.ping()
            self.redis_available = True
            logger.info("Redis L2 cache initialized")
        except Exception as e:
            logger.warning(f"Redis unavailable, using L1 only: {e}")
            self.redis_available = False
        
        # Теги для группировки кэша
        self.tag_registry = {}
    
    def _evict_l1_if_needed(self):
        """Вытеснение из L1 кэша при превышении размера (LFU)"""
        if len(self.l1_cache) >= self.l1_max_size:
            # Удаляем наименее часто используемый элемент
            if self.l1_access_count:
                least_used = min(self.l1_access_count, key=self.l1_access_count.get)
                self.l1_cache.pop(least_used, None)
                self.l1_access_count.pop(least_used, None)
    
    def get(self, key: str) -> Optional[Any]:
        """Получить значение из кэша (проверяет все уровни)"""
        start_time = time.time()
        
        # L1 - In-memory
        if key in self.l1_cache:
            self.l1_access_count[key] = self.l1_access_count.get(key, 0) + 1
            logger.debug(f"L1 cache hit: {key}")
            return self.l1_cache[key]
        
        # L2 - Redis
        if self.redis_available:
            try:
                value = self.redis_client.get(key)
                if value:
                    deserialized = pickle.loads(value)
                    # Продвигаем в L1
                    self._evict_l1_if_needed()
                    self.l1_cache[key] = deserialized
                    self.l1_access_count[key] = 1
                    
                    elapsed = time.time() - start_time
                    logger.debug(f"L2 cache hit: {key} ({elapsed:.3f}s)")
                    return deserialized
            except Exception as e:
                logger.error(f"L2 cache error: {e}")
        
        logger.debug(f"Cache miss: {key}")
        return None
    
    def set(self, key: str, value: Any, timeout: int = 300, tags: Optional[List[str]] = None):
        """Установить значение в кэш"""
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
            except Exception as e:
                logger.error(f"L2 cache set error: {e}")
    
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
    
    def get_stats(self) -> dict:
        """Получить статистику кэша"""
        stats = {
            'l1': {
                'size': len(self.l1_cache),
                'max_size': self.l1_max_size,
                'utilization': len(self.l1_cache) / self.l1_max_size * 100
            }
        }
        
        if self.redis_available:
            try:
                info = self.redis_client.info()
                stats['l2'] = {
                    'keys': self.redis_client.dbsize(),
                    'used_memory': info.get('used_memory_human'),
                    'hit_rate': info.get('keyspace_hits', 0) / max(info.get('keyspace_hits', 0) + info.get('keyspace_misses', 1), 1) * 100
                }
            except Exception as e:
                logger.error(f"Stats error: {e}")
        
        return stats
    
    def warm_cache(self, key_patterns: List[str], timeout: int = 3600):
        """Предварительная загрузка кэша по шаблонам"""
        if not self.redis_available:
            return
        
        try:
            for pattern in key_patterns:
                keys = self.redis_client.keys(pattern)
                if keys:
                    # Загружаем ключи в L1 кэш
                    for key in keys:
                        key_str = key.decode() if isinstance(key, bytes) else key
                        value = self.redis_client.get(key_str)
                        if value:
                            try:
                                deserialized = pickle.loads(value)
                                self._evict_l1_if_needed()
                                self.l1_cache[key_str] = deserialized
                                self.l1_access_count[key_str] = 0
                            except pickle.UnpicklingError:
                                continue
            
            logger.info(f"Warmed up cache for {len(key_patterns)} patterns")
        except Exception as e:
            logger.error(f"Cache warming error: {e}")
    
    def bulk_set(self, data: dict, timeout: int = 300, tags: Optional[List[str]] = None):
        """Массовая установка значений в кэш"""
        if not data:
            return
        
        # L1 - In-memory
        for key, value in data.items():
            self._evict_l1_if_needed()
            self.l1_cache[key] = value
            self.l1_access_count[key] = 0
        
        # L2 - Redis
        if self.redis_available:
            try:
                pipe = self.redis_client.pipeline()
                for key, value in data.items():
                    serialized = pickle.dumps(value)
                    pipe.setex(key, timeout, serialized)
                    
                    # Регистрируем теги
                    if tags:
                        for tag in tags:
                            tag_key = f"tag:{tag}"
                            pipe.sadd(tag_key, key)
                            pipe.expire(tag_key, timeout)
                
                pipe.execute()
            except Exception as e:
                logger.error(f"Bulk set error: {e}")
    
    def bulk_get(self, keys: List[str]) -> dict:
        """Массовое получение значений из кэша"""
        results = {}
        
        # Сначала проверяем L1
        for key in keys:
            if key in self.l1_cache:
                self.l1_access_count[key] = self.l1_access_count.get(key, 0) + 1
                results[key] = self.l1_cache[key]
        
        # Для остальных ключей проверяем L2
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
                                # Продвигаем в L1
                                self._evict_l1_if_needed()
                                self.l1_cache[key] = deserialized
                                self.l1_access_count[key] = 1
                                results[key] = deserialized
                            except pickle.UnpicklingError:
                                continue
                except Exception as e:
                    logger.error(f"Bulk get error: {e}")
        
        return results
    
    def get_keys_by_pattern(self, pattern: str) -> List[str]:
        """Получить список ключей по шаблону"""
        if not self.redis_available:
            return []
        
        try:
            keys = self.redis_client.keys(pattern)
            return [key.decode() if isinstance(key, bytes) else key for key in keys]
        except Exception as e:
            logger.error(f"Get keys by pattern error: {e}")
            return []

# Глобальный экземпляр
cache_manager = MultiLevelCache()

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
            
            # Добавляем аргументы в ключ
            if args:
                key_parts.append(hashlib.md5(str(args).encode()).hexdigest()[:8])
            if kwargs:
                key_parts.append(hashlib.md5(str(sorted(kwargs.items())).encode()).hexdigest()[:8])
            
            cache_key = ':'.join(key_parts)
            
            # Проверяем кэш
            result = cache_manager.get(cache_key)
            if result is not None:
                return result
            
            # Выполняем функцию
            result = func(*args, **kwargs)
            
            # Кэшируем результат
            cache_manager.set(cache_key, result, timeout, tags)
            
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
            
            # Инвалидируем кэш
            if tags:
                for tag in tags:
                    cache_manager.invalidate_by_tag(tag)
            
            if pattern:
                cache_manager.invalidate_by_pattern(pattern)
            
            return result
        return wrapper
    return decorator

# Специализированные кэш-менеджеры
class TournamentCacheManager:
    """Менеджер кэша для турниров"""
    
    @staticmethod
    @cached(timeout=600, tags=['tournaments', 'list'], key_prefix='tournaments')
    def get_all(filters: dict = None):
        """Получить все турниры с кэшированием"""
        from app.models.tournament import Tournament
        query = Tournament.query
        
        if filters:
            if 'category' in filters:
                query = query.filter(Tournament.category == filters['category'])
            if 'status' in filters:
                query = query.filter(Tournament.status == filters['status'])
        
        return query.all()
    
    @staticmethod
    @cached(timeout=1800, tags=['tournaments', 'detail'], key_prefix='tournament')
    def get_by_id(tournament_id: int):
        """Получить турнир по ID с кэшированием"""
        from app.models.tournament import Tournament
        return Tournament.query.get(tournament_id)
    
    @staticmethod
    @cached(timeout=3600, tags=['tournaments', 'calendar'], key_prefix='tournaments_calendar')
    def get_tournaments_for_calendar(start_date: str, end_date: str):
        """Получить турниры для календаря с кэшированием"""
        from app.models.tournament import Tournament
        from datetime import datetime
        
        start = datetime.strptime(start_date, '%Y-%m-%d').date()
        end = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        tournaments = Tournament.query.filter(
            Tournament.start_date <= end,
            Tournament.end_date >= start
        ).all()
        
        return [tournament.to_dict() for tournament in tournaments]
    
    @staticmethod
    @cached(timeout=1800, tags=['tournaments', 'stats'], key_prefix='tournaments_stats')
    def get_tournaments_stats():
        """Получить статистику турниров с кэшированием"""
        from app.models.tournament import Tournament
        from sqlalchemy import func
        from app import db
        
        stats = {
            'total': Tournament.query.count(),
            'by_status': {},
            'by_category': {},
            'by_month': {}
        }
        
        # Статистика по статусам
        status_counts = db.session.query(
            Tournament.status, 
            func.count(Tournament.id)
        ).group_by(Tournament.status).all()
        
        for status, count in status_counts:
            stats['by_status'][status] = count
        
        # Статистика по категориям
        category_counts = db.session.query(
            Tournament.category, 
            func.count(Tournament.id)
        ).group_by(Tournament.category).all()
        
        for category, count in category_counts:
            stats['by_category'][category] = count
        
        # Статистика по месяцам
        monthly_counts = db.session.query(
            func.strftime('%Y-%m', Tournament.start_date).label('month'),
            func.count(Tournament.id)
        ).group_by(func.strftime('%Y-%m', Tournament.start_date)).all()
        
        for month, count in monthly_counts:
            stats['by_month'][month] = count
        
        return stats
    
    @staticmethod
    @invalidate_cache(tags=['tournaments'])
    def invalidate_all():
        """Инвалидировать весь кэш турниров"""
        logger.info("Tournament cache invalidated")
    
    @staticmethod
    def invalidate_tournament(tournament_id: int):
        """Инвалидировать кэш конкретного турнира"""
        cache_manager.invalidate_by_pattern(f'tournament:get_by_id:*{tournament_id}*')
        cache_manager.invalidate_by_tag('tournaments')
    
    @staticmethod
    def invalidate_calendar_cache():
        """Инвалидировать кэш календаря турниров"""
        cache_manager.invalidate_by_pattern('tournaments_calendar*')
    
    @staticmethod
    def invalidate_stats_cache():
        """Инвалидировать кэш статистики турниров"""
        cache_manager.invalidate_by_pattern('tournaments_stats*')

class UserCacheManager:
    """Менеджер кэша для пользователей"""
    
    @staticmethod
    @cached(timeout=900, tags=['users'], key_prefix='user')
    def get_by_id(user_id: int):
        """Получить пользователя по ID с кэшированием"""
        from app.models.user import User
        return User.query.get(user_id)
    
    @staticmethod
    @cached(timeout=1800, tags=['users', 'preferences'], key_prefix='user_preferences')
    def get_user_preferences(user_id: int):
        """Получить настройки пользователя с кэшированием"""
        from app.models.preference import Preference
        return Preference.query.filter_by(user_id=user_id).first()
    
    @staticmethod
    @cached(timeout=1800, tags=['users', 'notifications'], key_prefix='user_notifications')
    def get_unread_notifications_count(user_id: int):
        """Получить количество непрочитанных уведомлений с кэшированием"""
        from app.models.notification import Notification
        return Notification.query.filter_by(user_id=user_id, is_read=False).count()
    
    @staticmethod
    def invalidate_user(user_id: int):
        """Инвалидировать кэш пользователя"""
        cache_manager.invalidate_by_pattern(f'user:get_by_id:*{user_id}*')
        cache_manager.invalidate_by_pattern(f'user_preferences:*{user_id}*')
        cache_manager.invalidate_by_pattern(f'user_notifications:*{user_id}*')
        cache_manager.invalidate_by_tag('users')

# CDN интеграция с реальной реализацией
class CDNCache:
    """Интеграция с CDN для кэширования статических ресурсов"""
    
    def __init__(self, provider: str = 'cloudflare', api_key: str = None, zone_id: str = None):
        self.provider = provider
        self.api_key = api_key or os.getenv('CF_API_KEY')
        self.zone_id = zone_id or os.getenv('CF_ZONE_ID')
        self.base_url = os.getenv('CDN_BASE_URL', 'https://chesscalendar.ru')
        logger.info(f"CDN cache initialized with provider: {provider}")
    
    def purge_url(self, url: str):
        """Очистить URL в CDN"""
        if self.provider == 'cloudflare' and self.api_key and self.zone_id:
            try:
                headers = {
                    'Authorization': f'Bearer {self.api_key}',
                    'Content-Type': 'application/json'
                }
                data = {
                    'files': [url]
                }
                response = requests.post(
                    f'https://api.cloudflare.com/client/v4/zones/{self.zone_id}/purge_cache',
                    json=data,
                    headers=headers
                )
                logger.info(f"CDN purge response: {response.status_code} for {url}")
                return response.status_code == 200
            except Exception as e:
                logger.error(f"CDN purge failed: {e}")
                return False
        logger.info(f"CDN purge: {url}")
        return True
    
    def purge_tag(self, tag: str):
        """Очистить все URL с определенным тегом"""
        if self.provider == 'cloudflare' and self.api_key and self.zone_id:
            try:
                headers = {
                    'Authorization': f'Bearer {self.api_key}',
                    'Content-Type': 'application/json'
                }
                data = {
                    'tags': [tag]
                }
                response = requests.post(
                    f'https://api.cloudflare.com/client/v4/zones/{self.zone_id}/purge_cache',
                    json=data,
                    headers=headers
                )
                logger.info(f"CDN purge tag response: {response.status_code} for {tag}")
                return response.status_code == 200
            except Exception as e:
                logger.error(f"CDN purge tag failed: {e}")
                return False
        logger.info(f"CDN purge tag: {tag}")
        return True
    
    def purge_by_pattern(self, pattern: str):
        """Очистить все URL по шаблону"""
        logger.info(f"CDN purge pattern: {pattern}")
        # В реальном приложении здесь будет логика сопоставления шаблона
        # и вызова соответствующего API провайдера
        return True

# Инициализация CDN кэша
try:
    cdn_cache = CDNCache()
except Exception as e:
    logger.warning(f"Failed to initialize CDN cache: {e}")
    # Резервная реализация
    class MockCDNCache:
        def purge_url(self, url: str): return True
        def purge_tag(self, tag: str): return True
        def purge_by_pattern(self, pattern: str): return True
    cdn_cache = MockCDNCache()
