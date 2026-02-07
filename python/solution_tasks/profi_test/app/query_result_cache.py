# -*- coding: utf-8 -*-
"""
Продвинутый кэш результатов запросов с Redis для оптимизации производительности
"""
import logging
import json
import hashlib
import time
from typing import Dict, Any, Optional, List, Union
from functools import wraps
import pickle
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class QueryResultCache:
    """Продвинутая система кэширования для результатов запросов базы данных с Redis"""
    
    def __init__(self, app=None, redis_client=None):
        self.app = app
        self.redis = redis_client
        self.cache_stats = {
            'hits': 0,
            'misses': 0,
            'sets': 0,
            'deletes': 0,
            'evictions': 0,
            'total_requests': 0
        }
        self.default_ttl = 300  # 5 minutes
        self.cache_prefix = 'query_cache:'
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Инициализирует кэш с Flask приложением"""
        self.app = app
        
        # Try to get Redis client from app
        if hasattr(app, 'redis') and app.redis:
            self.redis = app.redis
        elif hasattr(app, 'redis_client'):
            self.redis = app.redis_client
        else:
            # Try to create Redis connection
            try:
                import redis
                redis_url = app.config.get('REDIS_URL', 'redis://localhost:6379/0')
                self.redis = redis.from_url(redis_url, decode_responses=False)
                # Test connection
                self.redis.ping()
                logger.info("Query result cache connected to Redis")
            except Exception as e:
                logger.warning(f"Redis not available for query cache: {e}")
                self.redis = None
        
        # Add to app context
        app.query_result_cache = self
    
    def _generate_cache_key(self, query: str, params: Dict = None) -> str:
        """Генерирует уникальный ключ кэша для запроса и параметров"""
        # Create hash of query and parameters
        key_data = {
            'query': query,
            'params': params or {}
        }
        key_string = json.dumps(key_data, sort_keys=True, default=str)
        key_hash = hashlib.md5(key_string.encode()).hexdigest()
        
        return f"{self.cache_prefix}{key_hash}"
    
    def _serialize_result(self, result: Any) -> bytes:
        """Сериализует результат запроса для хранения"""
        try:
            # Handle different result types
            if isinstance(result, list):
                # Serialize list of objects
                serialized = pickle.dumps(result)
            elif hasattr(result, '__dict__'):
                # Serialize SQLAlchemy model objects
                serialized = pickle.dumps(result)
            else:
                # Serialize simple types
                serialized = pickle.dumps(result)
            
            return serialized
        except Exception as e:
            logger.error(f"Error serializing result: {e}")
            raise
    
    def _deserialize_result(self, data: bytes) -> Any:
        """Десериализует сохраненный результат запроса"""
        try:
            return pickle.loads(data)
        except Exception as e:
            logger.error(f"Error deserializing result: {e}")
            raise
    
    def get(self, query: str, params: Dict = None, ttl: Optional[int] = None) -> Optional[Any]:
        """
        Получает результат кэшированного запроса
        
        Args:
            query: SQL запрос строка
            params: Параметры запроса
            ttl: Время жизни переопределение
        """
        if not self.redis:
            return None
        
        self.cache_stats['total_requests'] += 1
        cache_key = self._generate_cache_key(query, params)
        
        try:
            # Try to get from cache
            cached_data = self.redis.get(cache_key)
            
            if cached_data is not None:
                # Cache hit
                self.cache_stats['hits'] += 1
                result = self._deserialize_result(cached_data)
                logger.debug(f"Cache hit for query: {query[:50]}...")
                return result
            else:
                # Cache miss
                self.cache_stats['misses'] += 1
                logger.debug(f"Cache miss for query: {query[:50]}...")
                return None
                
        except Exception as e:
            logger.error(f"Error getting from cache: {e}")
            self.cache_stats['misses'] += 1
            return None
    
    def set(self, query: str, result: Any, params: Dict = None, ttl: Optional[int] = None) -> bool:
        """
        Кэширует результат запроса
        
        Args:
            query: SQL запрос строка
            result: Результат запроса для кэширования
            params: Параметры запроса
            ttl: Время жизни в секундах
        """
        if not self.redis:
            return False
        
        cache_key = self._generate_cache_key(query, params)
        ttl = ttl or self.default_ttl
        
        try:
            # Serialize result
            serialized_result = self._serialize_result(result)
            
            # Store in cache with TTL
            success = self.redis.setex(cache_key, ttl, serialized_result)
            
            if success:
                self.cache_stats['sets'] += 1
                logger.debug(f"Cached result for query: {query[:50]}... (TTL: {ttl}s)")
            
            return bool(success)
            
        except Exception as e:
            logger.error(f"Error setting cache: {e}")
            return False
    
    def delete(self, query: str, params: Dict = None) -> bool:
        """Удаляет результат кэшированного запроса"""
        if not self.redis:
            return False
        
        cache_key = self._generate_cache_key(query, params)
        
        try:
            deleted = bool(self.redis.delete(cache_key))
            if deleted:
                self.cache_stats['deletes'] += 1
                logger.debug(f"Deleted cache for query: {query[:50]}...")
            return deleted
        except Exception as e:
            logger.error(f"Error deleting cache: {e}")
            return False
    
    def invalidate_pattern(self, pattern: str) -> int:
        """Аннулирует все записи кэша, соответствующие шаблону"""
        if not self.redis:
            return 0
        
        try:
            # Get all keys matching pattern
            keys = self.redis.keys(f"{self.cache_prefix}{pattern}*")
            
            if keys:
                # Delete all matching keys
                deleted_count = self.redis.delete(*keys)
                self.cache_stats['deletes'] += deleted_count
                self.cache_stats['evictions'] += deleted_count
                logger.info(f"Invalidated {deleted_count} cache entries matching pattern: {pattern}")
                return deleted_count
            
            return 0
        except Exception as e:
            logger.error(f"Error invalidating cache pattern: {e}")
            return 0
    
    def clear_all(self) -> int:
        """Очищает все записи кэша запросов"""
        if not self.redis:
            return 0
        
        try:
            # Get all cache keys
            pattern = f"{self.cache_prefix}*"
            keys = self.redis.keys(pattern)
            
            if keys:
                deleted_count = self.redis.delete(*keys)
                self.cache_stats['deletes'] += deleted_count
                logger.info(f"Cleared {deleted_count} cache entries")
                return deleted_count
            
            return 0
        except Exception as e:
            logger.error(f"Error clearing cache: {e}")
            return 0
    
    def get_cache_statistics(self) -> Dict[str, Any]:
        """Получает статистику производительности кэша"""
        if not self.redis:
            return {'error': 'Redis not available'}
        
        stats = self.cache_stats.copy()
        
        # Calculate hit ratio
        total_requests = stats['total_requests']
        if total_requests > 0:
            stats['hit_ratio'] = stats['hits'] / total_requests
        else:
            stats['hit_ratio'] = 0
        
        # Add Redis info
        try:
            redis_info = self.redis.info()
            stats['redis_info'] = {
                'used_memory': redis_info.get('used_memory_human', 'N/A'),
                'connected_clients': redis_info.get('connected_clients', 'N/A'),
                'total_commands_processed': redis_info.get('total_commands_processed', 'N/A'),
                'keyspace_hits': redis_info.get('keyspace_hits', 'N/A'),
                'keyspace_misses': redis_info.get('keyspace_misses', 'N/A')
            }
        except Exception as e:
            stats['redis_info'] = {'error': str(e)}
        
        # Add cache size info
        try:
            cache_keys = self.redis.keys(f"{self.cache_prefix}*")
            stats['cache_entries'] = len(cache_keys)
            
            # Sample some cache entries for size estimation
            if cache_keys:
                sample_size = min(10, len(cache_keys))
                sample_keys = cache_keys[:sample_size]
                total_size = 0
                
                for key in sample_keys:
                    total_size += len(self.redis.get(key) or b'')
                
                avg_size = total_size / sample_size if sample_size > 0 else 0
                stats['estimated_total_size'] = avg_size * len(cache_keys)
                stats['average_entry_size'] = avg_size
        except Exception as e:
            stats['cache_size_error'] = str(e)
        
        return stats

def cached_query(ttl: int = 300, key_prefix: str = '', invalidate_on: List[str] = None):
    """
    Декоратор для кэширования результатов запросов базы данных
    
    Args:
        ttl: Время жизни в секундах
        key_prefix: Префикс для ключа кэша
        invalidate_on: Список шаблонов для аннулирования когда этот запрос выполняется
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Get cache instance
            cache = None
            try:
                from flask import current_app
                cache = current_app.query_result_cache
            except:
                pass
            
            if not cache or not cache.redis:
                # Cache not available, execute function directly
                return func(*args, **kwargs)
            
            # Generate cache key
            func_name = f"{key_prefix}{func.__name__}"
            cache_key = f"{func_name}:{hash(str(args) + str(sorted(kwargs.items())))}"
            
            # Try to get from cache
            cached_result = cache.get(cache_key, ttl=ttl)
            if cached_result is not None:
                return cached_result
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            
            # Cache the result
            cache.set(cache_key, result, ttl=ttl)
            
            # Invalidate related caches if specified
            if invalidate_on and cache:
                for pattern in invalidate_on:
                    cache.invalidate_pattern(pattern)
            
            return result
        return wrapper
    return decorator

class CacheManager:
    """Интерфейс высокого уровня для управления кэшем"""
    
    def __init__(self, app=None):
        self.app = app
        self.query_cache = None
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Инициализирует менеджер кэша с Flask приложением"""
        self.app = app
        self.query_cache = QueryResultCache(app)
        app.cache_manager = self
    
    def cache_user_data(self, user_id: int, data: Any, key: str, ttl: int = 1800):
        """Кэширует данные конкретного пользователя"""
        if not self.query_cache:
            return False
        
        cache_key = f"user:{user_id}:{key}"
        return self.query_cache.set(cache_key, data, ttl=ttl)
    
    def get_user_data(self, user_id: int, key: str):
        """Получает кэшированные данные конкретного пользователя"""
        if not self.query_cache:
            return None
        
        cache_key = f"user:{user_id}:{key}"
        return self.query_cache.get(cache_key)
    
    def cache_query_result(self, query: str, result: Any, params: Dict = None, ttl: int = 300):
        """Кэширует результат запроса базы данных"""
        if not self.query_cache:
            return False
        return self.query_cache.set(query, result, params, ttl)
    
    def get_cached_query(self, query: str, params: Dict = None):
        """Получает результат кэшированного запроса"""
        if not self.query_cache:
            return None
        return self.query_cache.get(query, params)
    
    def invalidate_user_cache(self, user_id: int):
        """Аннулирует все записи кэша для пользователя"""
        if not self.query_cache:
            return 0
        return self.query_cache.invalidate_pattern(f"user:{user_id}:")
    
    def get_cache_report(self) -> Dict[str, Any]:
        """Получает комплексный отчет о производительности кэша"""
        if not self.query_cache:
            return {'error': 'Cache not initialized'}
        
        return {
            'query_cache_stats': self.query_cache.get_cache_statistics(),
            'timestamp': datetime.utcnow().isoformat()
        }

# Global instance
cache_manager = CacheManager()

# Flask CLI commands
def register_cache_result_commands(app):
    """Регистрирует CLI команды для кэширования результатов запросов"""
    import click
    from flask.cli import with_appcontext
    
    @app.cli.command('cache-stats')
    @with_appcontext
    def show_cache_stats():
        """Показывает статистику кэша результатов запросов"""
        if hasattr(app, 'cache_manager'):
            report = app.cache_manager.get_cache_report()
            click.echo("Query Result Cache Statistics:")
            click.echo(json.dumps(report, indent=2, default=str))
        else:
            click.echo("Cache manager not initialized")
    
    @app.cli.command('cache-clear')
    @click.confirmation_option(prompt='Are you sure you want to clear all query cache?')
    @with_appcontext
    def clear_cache():
        """Очищает весь кэш результатов запросов"""
        if hasattr(app, 'query_result_cache'):
            deleted = app.query_result_cache.clear_all()
            click.echo(f"Cleared {deleted} cache entries")
        else:
            click.echo("Query result cache not initialized")