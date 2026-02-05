"""
Расширенное кэширование Redis с продвинутыми функциями и поддержкой failover
"""
import redis
import json
import pickle
import hashlib
import logging
from datetime import datetime, timedelta
from functools import wraps
from typing import Any, Optional, Dict, List, Union
import os

logger = logging.getLogger(__name__)

class RedisCacheManager:
    """Продвинутый менеджер кэша Redis с failover и мониторингом"""
    
    def __init__(self, app=None):
        self.app = app
        self.redis_client = None
        self.redis_available = False
        self.cache_stats = {
            'hits': 0,
            'misses': 0,
            'errors': 0,
            'fallback_used': 0
        }
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Инициализация кэша Redis с Flask приложением"""
        self.app = app
        
        # Получение конфигурации Redis
        redis_url = app.config.get('CACHE_REDIS_URL', 'redis://localhost:6379/0')
        redis_password = os.environ.get('REDIS_PASSWORD')
        
        # Создание соединения Redis
        try:
            self.redis_client = redis.from_url(
                redis_url,
                password=redis_password,
                socket_connect_timeout=5,
                socket_timeout=5,
                retry_on_timeout=True,
                health_check_interval=30
            )
            
            # Тестирование соединения
            self.redis_client.ping()
            self.redis_available = True
            logger.info("Кэш Redis успешно инициализирован")
            
        except Exception as e:
            logger.warning(f"Соединение Redis не удалось, переход к кэшу в памяти: {e}")
            self.redis_available = False
            self.redis_client = None
    
    def _generate_cache_key(self, key: str, prefix: str = '') -> str:
        """Генерация ключа кэша с опциональным префиксом"""
        if prefix:
            return f"{prefix}:{key}"
        return key
    
    def _serialize_data(self, data: Any) -> bytes:
        """Сериализация данных для хранения"""
        try:
            return pickle.dumps(data)
        except Exception as e:
            logger.warning(f"Не удалось сериализовать данные pickle, используем JSON: {e}")
            return json.dumps(data, default=str).encode('utf-8')
    
    def _deserialize_data(self, data: bytes) -> Any:
        """Десериализация данных из хранилища"""
        try:
            return pickle.loads(data)
        except Exception:
            try:
                return json.loads(data.decode('utf-8'))
            except Exception as e:
                logger.error(f"Не удалось десериализовать данные: {e}")
                return None
    
    def get(self, key: str, prefix: str = '') -> Any:
        """Получение значения из кэша"""
        cache_key = self._generate_cache_key(key, prefix)
        
        if not self.redis_available:
            self.cache_stats['misses'] += 1
            return None
        
        try:
            cached_data = self.redis_client.get(cache_key)
            if cached_data is not None:
                self.cache_stats['hits'] += 1
                return self._deserialize_data(cached_data)
            else:
                self.cache_stats['misses'] += 1
                return None
                
        except Exception as e:
            self.cache_stats['errors'] += 1
            logger.error(f"Ошибка получения из кэша для ключа {cache_key}: {e}")
            return None
    
    def set(self, key: str, value: Any, timeout: int = 300, prefix: str = '') -> bool:
        """Установка значения в кэш"""
        cache_key = self._generate_cache_key(key, prefix)
        
        if not self.redis_available:
            return False
        
        try:
            serialized_data = self._serialize_data(value)
            result = self.redis_client.setex(cache_key, timeout, serialized_data)
            return result is not None
        except Exception as e:
            self.cache_stats['errors'] += 1
            logger.error(f"Ошибка установки в кэш для ключа {cache_key}: {e}")
            return False
    
    def delete(self, key: str, prefix: str = '') -> bool:
        """Удаление значения из кэша"""
        cache_key = self._generate_cache_key(key, prefix)
        
        if not self.redis_available:
            return False
        
        try:
            result = self.redis_client.delete(cache_key)
            return result > 0
        except Exception as e:
            self.cache_stats['errors'] += 1
            logger.error(f"Ошибка удаления из кэша для ключа {cache_key}: {e}")
            return False
    
    def exists(self, key: str, prefix: str = '') -> bool:
        """Проверка существования ключа в кэше"""
        cache_key = self._generate_cache_key(key, prefix)
        
        if not self.redis_available:
            return False
        
        try:
            return self.redis_client.exists(cache_key) > 0
        except Exception as e:
            logger.error(f"Ошибка проверки существования ключа {cache_key}: {e}")
            return False
    
    def get_multi(self, keys: List[str], prefix: str = '') -> Dict[str, Any]:
        """Получение нескольких значений из кэша"""
        if not self.redis_available:
            return {}
        
        try:
            pipeline = self.redis_client.pipeline()
            for key in keys:
                cache_key = self._generate_cache_key(key, prefix)
                pipeline.get(cache_key)
            
            results = pipeline.execute()
            return_dict = {}
            
            for i, key in enumerate(keys):
                if results[i] is not None:
                    return_dict[key] = self._deserialize_data(results[i])
            
            return return_dict
        except Exception as e:
            self.cache_stats['errors'] += 1
            logger.error(f"Ошибка множественного получения из кэша: {e}")
            return {}
    
    def set_multi(self, mapping: Dict[str, Any], timeout: int = 300, prefix: str = '') -> bool:
        """Установка нескольких значений в кэш"""
        if not self.redis_available:
            return False
        
        try:
            pipeline = self.redis_client.pipeline()
            for key, value in mapping.items():
                cache_key = self._generate_cache_key(key, prefix)
                serialized_data = self._serialize_data(value)
                pipeline.setex(cache_key, timeout, serialized_data)
            
            pipeline.execute()
            return True
        except Exception as e:
            self.cache_stats['errors'] += 1
            logger.error(f"Ошибка множественной установки в кэш: {e}")
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Получение статистики кэша"""
        stats = self.cache_stats.copy()
        
        if self.redis_available:
            try:
                info = self.redis_client.info()
                stats.update({
                    'redis_info': {
                        'used_memory': info.get('used_memory_human', 'N/A'),
                        'connected_clients': info.get('connected_clients', 'N/A'),
                        'uptime_seconds': info.get('uptime_in_seconds', 'N/A')
                    }
                })
            except Exception as e:
                logger.error(f"Не удалось получить информацию Redis: {e}")
        
        return stats
    
    def clear_pattern(self, pattern: str) -> int:
        """Очистка всех ключей по шаблону"""
        if not self.redis_available:
            return 0
        
        try:
            keys = self.redis_client.keys(pattern)
            if keys:
                return self.redis_client.delete(*keys)
            return 0
        except Exception as e:
            logger.error(f"Ошибка очистки кэша по шаблону {pattern}: {e}")
            return 0
    
    def get_cache_decorator(self, timeout: int = 300, key_prefix: str = ''):
        """
        Создание декоратора кэша с пользовательским таймаутом и префиксом
        """
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Генерация ключа кэша из сигнатуры функции
                func_args = str(args) + str(sorted(kwargs.items()))
                cache_key = hashlib.md5(func_args.encode()).hexdigest()
                full_key = f"{key_prefix}:{func.__name__}:{cache_key}"
                
                # Попытка получить из кэша
                cached_result = self.get(full_key)
                if cached_result is not None:
                    return cached_result
                
                # Выполнение функции и кэширование результата
                result = func(*args, **kwargs)
                self.set(full_key, result, timeout)
                return result
            return wrapper
        return decorator

# Глобальный экземпляр
redis_cache_manager = RedisCacheManager()

# Flask CLI команды для управления кэшем
def register_cache_commands(app):
    """Регистрация CLI команд управления кэшем"""
    import click
    from flask.cli import with_appcontext
    
    @app.cli.command('cache-stats')
    @with_appcontext
    def cache_statistics():
        """Показать статистику кэша"""
        stats = redis_cache_manager.get_stats()
        click.echo("Статистика кэша:")
        click.echo(f"  Попаданий: {stats.get('hits', 0)}")
        click.echo(f"  Промахов: {stats.get('misses', 0)}")
        click.echo(f"  Ошибок: {stats.get('errors', 0)}")
        click.echo(f"  Использован fallback: {stats.get('fallback_used', 0)}")
        
        if 'redis_info' in stats:
            redis_info = stats['redis_info']
            click.echo("Информация Redis:")
            click.echo(f"  Использование памяти: {redis_info.get('used_memory', 'N/A')}")
            click.echo(f"  Подключенные клиенты: {redis_info.get('connected_clients', 'N/A')}")
    
    @app.cli.command('cache-clear')
    @with_appcontext
    def clear_cache():
        """Очистить все записи кэша"""
        cleared = redis_cache_manager.clear_pattern('*')
        click.echo(f"Очищено {cleared} записей кэша")