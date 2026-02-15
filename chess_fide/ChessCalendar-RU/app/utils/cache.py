import redis
import json
import pickle
from datetime import timedelta
from functools import wraps
import logging

class CacheService:
    def __init__(self, host='localhost', port=6379, db=0, default_timeout=300):
        self.default_timeout = default_timeout
        self.logger = logging.getLogger(__name__)
        
        try:
            self.redis_client = redis.Redis(
                host=host, 
                port=port, 
                db=db,
                decode_responses=False  # Для pickle сериализации
            )
            # Проверяем соединение
            self.redis_client.ping()
            self.use_redis = True
            self.logger.info("Redis cache initialized successfully")
        except:
            self.use_redis = False
            self.cache = {}  # In-memory fallback
            self.logger.warning("Redis unavailable, using in-memory cache")
    
    def get(self, key):
        """Получить значение из кэша"""
        try:
            if self.use_redis:
                value = self.redis_client.get(key)
                if value:
                    return pickle.loads(value)
            else:
                return self.cache.get(key)
        except Exception as e:
            self.logger.error(f"Cache get error: {e}")
        return None
    
    def set(self, key, value, timeout=None):
        """Установить значение в кэш"""
        if timeout is None:
            timeout = self.default_timeout
            
        try:
            if self.use_redis:
                serialized_value = pickle.dumps(value)
                self.redis_client.setex(key, timeout, serialized_value)
            else:
                self.cache[key] = value
                # Для in-memory кэша реализуем простое удаление по времени
                # В реальном приложении использовать более сложную логику
        except Exception as e:
            self.logger.error(f"Cache set error: {e}")
    
    def delete(self, key):
        """Удалить значение из кэша"""
        try:
            if self.use_redis:
                self.redis_client.delete(key)
            else:
                self.cache.pop(key, None)
        except Exception as e:
            self.logger.error(f"Cache delete error: {e}")
    
    def clear(self):
        """Очистить весь кэш"""
        try:
            if self.use_redis:
                self.redis_client.flushdb()
            else:
                self.cache.clear()
        except Exception as e:
            self.logger.error(f"Cache clear error: {e}")
    
    def get_stats(self):
        """Получить статистику кэша"""
        try:
            if self.use_redis:
                info = self.redis_client.info()
                return {
                    'type': 'redis',
                    'keys': self.redis_client.dbsize(),
                    'used_memory': info.get('used_memory_human', 'N/A'),
                    'connected': True
                }
            else:
                return {
                    'type': 'in-memory',
                    'keys': len(self.cache),
                    'connected': True
                }
        except Exception as e:
            self.logger.error(f"Cache stats error: {e}")
            return {'type': 'unknown', 'connected': False}

# Декоратор для кэширования функций
def cached(timeout=300, key_prefix='func_cache'):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Создаем ключ кэша
            cache_key = f"{key_prefix}:{func.__name__}:{hash(str(args) + str(sorted(kwargs.items())))}"
            
            # Проверяем кэш
            result = cache_service.get(cache_key)
            if result is not None:
                return result
            
            # Выполняем функцию и кэшируем результат
            result = func(*args, **kwargs)
            cache_service.set(cache_key, result, timeout)
            return result
        return wrapper
    return decorator

# Глобальный экземпляр кэш-сервиса
cache_service = CacheService()

# Утилиты для работы с кэшем турниров
class TournamentCache:
    @staticmethod
    @cached(timeout=600, key_prefix='tournaments')
    def get_all_tournaments():
        """Получить все турниры с кэшированием на 10 минут"""
        from app.models.tournament import Tournament
        return Tournament.query.all()
    
    @staticmethod
    @cached(timeout=300, key_prefix='tournaments_filtered')
    def get_filtered_tournaments(category=None, status=None, location=None):
        """Получить отфильтрованные турниры с кэшированием на 5 минут"""
        from app.models.tournament import Tournament
        
        query = Tournament.query
        if category:
            query = query.filter(Tournament.category == category)
        if status:
            query = query.filter(Tournament.status == status)
        if location:
            query = query.filter(Tournament.location.contains(location))
            
        return query.all()
    
    @staticmethod
    def invalidate_tournaments_cache():
        """Инвалидировать кэш турниров"""
        # Удаляем все ключи, связанные с турнирами
        try:
            if cache_service.use_redis:
                # Используем паттерн для удаления по префиксу
                keys = cache_service.redis_client.keys('tournaments*')
                if keys:
                    cache_service.redis_client.delete(*keys)
            else:
                # Для in-memory кэша очищаем все (упрощенный вариант)
                cache_service.clear()
        except Exception as e:
            logging.error(f"Cache invalidation error: {e}")
    
    @staticmethod
    @cached(timeout=3600, key_prefix='tournaments_stats')
    def get_tournaments_stats():
        """Получить статистику турниров с кэшированием на 1 час"""
        from app.models.tournament import Tournament
        from app import db
        
        stats = {
            'total': Tournament.query.count(),
            'by_category': dict(db.session.query(Tournament.category, db.func.count(Tournament.id))
                              .group_by(Tournament.category).all()),
            'by_status': dict(db.session.query(Tournament.status, db.func.count(Tournament.id))
                            .group_by(Tournament.status).all()),
            'by_location': dict(db.session.query(Tournament.location, db.func.count(Tournament.id))
                              .group_by(Tournament.location).all()[:10])  # Топ 10 локаций
        }
        return stats