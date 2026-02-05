# -*- coding: utf-8 -*-
"""
Модуль расширенного кэширования для ПрофиТест
Предоставляет продвинутые возможности кэширования и оптимизации производительности
"""
import redis
import json
import pickle
import hashlib
from datetime import datetime, timedelta
from functools import wraps
from app import cache
import logging


class AdvancedCacheManager:
    """
    Расширенный менеджер кэширования для системы ПрофиТест.
    Обеспечивает интеллектуальное кэширование данных и оптимизацию производительности.
    """
    
    def __init__(self, redis_url=None):
        """
        Initialize the cache manager.
        
        Args:
            redis_url: Redis connection URL. If None, gets from app config.
        """
        self.logger = logging.getLogger(__name__)
        
        # Get Redis URL from app config if not provided
        if redis_url is None:
            from flask import current_app
            try:
                redis_url = current_app.config.get('CACHE_REDIS_URL', 'redis://localhost:6379/0')
            except RuntimeError:
                # Not in app context, use default
                redis_url = 'redis://localhost:6379/0'
        
        try:
            self.redis_client = redis.from_url(redis_url, decode_responses=False)  # Changed to decode_responses=False for binary data
            self.redis_available = True
            self.logger.info("Redis cache initialized successfully")
        except Exception as e:
            self.logger.warning(f"Redis недоступен: {str(e)}. Используется только Flask-Cache.")
            self.redis_client = None
            self.redis_available = False
    
    def cache_result(self, key_prefix, timeout=300, cache_args=True):
        """
        Декоратор для кэширования результатов функций.
        
        Args:
            key_prefix: Префикс для ключа кэша
            timeout: Время жизни кэша в секундах
            cache_args: Кэшировать ли аргументы функции
            
        Returns:
            function: Декорированная функция
        """
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Создание ключа кэша
                if cache_args:
                    cache_key = f"{key_prefix}:{self._generate_cache_key(args, kwargs)}"
                else:
                    cache_key = key_prefix
                
                # Попытка получить из кэша Redis
                if self.redis_available:
                    try:
                        cached_result = self.redis_client.get(cache_key)
                        if cached_result:
                            result = pickle.loads(cached_result)
                            self.logger.debug(f"Данные получены из Redis кэша: {cache_key}")
                            return result
                    except Exception as e:
                        self.logger.warning(f"Ошибка при получении из Redis кэша: {str(e)}")
                
                # Попытка получить из Flask-Cache
                flask_cache_result = cache.get(cache_key)
                if flask_cache_result is not None:
                    self.logger.debug(f"Данные получены из Flask-Cache: {cache_key}")
                    return flask_cache_result
                
                # Выполнение функции и сохранение результата
                result = func(*args, **kwargs)
                
                # Сохранение в Redis
                if self.redis_available:
                    try:
                        self.redis_client.setex(
                            cache_key,
                            timeout,
                            pickle.dumps(result)
                        )
                        self.logger.debug(f"Данные сохранены в Redis кэше: {cache_key}")
                    except Exception as e:
                        self.logger.warning(f"Ошибка при сохранении в Redis кэш: {str(e)}")
                
                # Сохранение во Flask-Cache
                cache.set(cache_key, result, timeout=timeout)
                self.logger.debug(f"Данные сохранены в Flask-Cache: {cache_key}")
                
                return result
            return wrapper
        return decorator
    
    def _generate_cache_key(self, args, kwargs):
        """
        Генерирует ключ кэша на основе аргументов функции.
        
        Args:
            args: Позиционные аргументы
            kwargs: Именованные аргументы
            
        Returns:
            str: Ключ кэша
        """
        try:
            # Хешируем аргументы для создания уникального ключа
            hash_input = str(args) + str(sorted(kwargs.items()))
            return hashlib.md5(hash_input.encode()).hexdigest()
        except Exception as e:
            self.logger.error(f"Ошибка при генерации ключа кэша: {str(e)}")
            return "default_key"
    
    def invalidate_cache(self, key_pattern):
        """
        Инвалидирует кэш по шаблону ключа.
        
        Args:
            key_pattern: Шаблон ключа для инвалидации
        """
        try:
            invalidated_count = 0
            
            if self.redis_available:
                # Инвалидация в Redis
                keys_to_delete = self.redis_client.keys(f"{key_pattern}*")
                if keys_to_delete:
                    self.redis_client.delete(*keys_to_delete)
                    invalidated_count += len(keys_to_delete)
                    self.logger.info(f"Инвалидировано {len(keys_to_delete)} ключей Redis по шаблону {key_pattern}")
            
            # Flask-Cache не поддерживает шаблоны, но мы можем попробовать инвалидировать
            # часто используемые ключи, если они соответствуют шаблону
            # Для этого мы добавим метод инвалидации конкретных ключей
            
            return invalidated_count
            
        except Exception as e:
            self.logger.error(f"Ошибка при инвалидации кэша: {str(e)}")
            return 0
    
    def invalidate_related_cache(self, entity_type, entity_id=None):
        """
        Инвалидирует связанные кэши при изменении сущности.
        
        Args:
            entity_type: Тип сущности (user, test_result, etc.)
            entity_id: ID сущности (опционально)
        """
        try:
            invalidated_total = 0
            
            # Определяем шаблоны кэша, которые зависят от типа сущности
            patterns = []
            if entity_type == 'user':
                patterns = [
                    f'user:{entity_id}:' if entity_id else 'user:*:',
                    f'*user*{entity_id}*' if entity_id else '*user*',
                    f'*user_id*{entity_id}*' if entity_id else '*user_id*',
                ]
            elif entity_type == 'test_result':
                patterns = [
                    f'*test_result*{entity_id}*' if entity_id else '*test_result*',
                    f'*result*{entity_id}*' if entity_id else '*result*',
                ]
            elif entity_type == 'notification':
                patterns = [
                    f'*notification*{entity_id}*' if entity_id else '*notification*',
                    f'*notification_user*{entity_id}*' if entity_id else '*notification*',
                ]
            
            # Инвалидируем каждый шаблон
            for pattern in patterns:
                count = self.invalidate_cache(pattern)
                invalidated_total += count
                
            self.logger.info(f"Инвалидировано {invalidated_total} связанных кэшей для {entity_type}:{entity_id if entity_id else 'all'}")
            return invalidated_total
            
        except Exception as e:
            self.logger.error(f"Ошибка при инвалидации связанных кэшей: {str(e)}")
            return 0
    
    def get_cache_stats(self):
        """
        Получает статистику использования кэша.
        
        Returns:
            dict: Статистика кэша
        """
        stats = {
            'redis_available': self.redis_available,
            'flask_cache_backend': cache.config.get('CACHE_TYPE', 'unknown')
        }
        
        if self.redis_available:
            try:
                redis_info = self.redis_client.info()
                stats['redis_stats'] = {
                    'used_memory': redis_info.get('used_memory_human', 'N/A'),
                    'connected_clients': redis_info.get('connected_clients', 'N/A'),
                    'total_commands_processed': redis_info.get('total_commands_processed', 'N/A'),
                    'keyspace_hits': redis_info.get('keyspace_hits', 'N/A'),
                    'keyspace_misses': redis_info.get('keyspace_misses', 'N/A'),
                    'hit_rate': self._calculate_redis_hit_rate(
                        redis_info.get('keyspace_hits', 0),
                        redis_info.get('keyspace_misses', 0)
                    )
                }
            except Exception as e:
                self.logger.error(f"Ошибка при получении статистики Redis: {str(e)}")
                stats['redis_stats'] = {'error': str(e)}
        
        return stats
    
    def _calculate_redis_hit_rate(self, hits, misses):
        """
        Вычисляет процент попаданий в кэш Redis.
        
        Args:
            hits: Количество попаданий
            misses: Количество промахов
            
        Returns:
            float: Процент попаданий
        """
        total = hits + misses
        if total == 0:
            return 0
        return round((hits / total) * 100, 2)
    
    def warm_up_cache(self, cache_warmers):
        """
        Прогревает кэш с помощью заданных функций.
        
        Args:
            cache_warmers: Список функций для прогрева кэша
        """
        try:
            self.logger.info("Начало прогрева кэша...")
            warmed_keys = 0
            
            for warmer_func in cache_warmers:
                try:
                    warmer_func()
                    warmed_keys += 1
                except Exception as e:
                    self.logger.warning(f"Ошибка при прогреве кэша функцией {warmer_func.__name__}: {str(e)}")
            
            self.logger.info(f"Прогрев кэша завершен. Прогрето {warmed_keys} функций.")
            
        except Exception as e:
            self.logger.error(f"Ошибка при прогреве кэша: {str(e)}")
    
    def create_cache_warmer(self, func, *args, **kwargs):
        """
        Создает функцию-прогреватель кэша.
        
        Args:
            func: Функция для кэширования
            *args: Аргументы функции
            **kwargs: Именованные аргументы функции
            
        Returns:
            function: Функция-прогреватель
        """
        def warmer():
            # Выполняем функцию для прогрева кэша
            result = func(*args, **kwargs)
            self.logger.debug(f"Прогрет кэш для функции {func.__name__}")
            return result
        
        return warmer
    
    def batch_cache_operation(self, operations, use_pipeline=True):
        """
        Выполняет пакетные операции с кэшем для повышения производительности.
        
        Args:
            operations: Список операций (кортежи вида (operation, key, value, timeout))
            use_pipeline: Использовать ли pipeline для Redis
            
        Returns:
            list: Результаты операций
        """
        results = []
        
        if self.redis_available and use_pipeline:
            try:
                pipe = self.redis_client.pipeline()
                for operation, key, value, timeout in operations:
                    if operation == 'set':
                        pipe.setex(key, timeout, pickle.dumps(value))
                    elif operation == 'get':
                        pipe.get(key)
                    elif operation == 'delete':
                        pipe.delete(key)
                
                redis_results = pipe.execute()
                results.extend(redis_results)
                
            except Exception as e:
                self.logger.error(f"Ошибка при пакетной операции Redis: {str(e)}")
        
        # Резервные операции через Flask-Cache
        for operation, key, value, timeout in operations:
            try:
                if operation == 'set':
                    cache.set(key, value, timeout=timeout)
                    results.append(True)
                elif operation == 'get':
                    result = cache.get(key)
                    results.append(result)
                elif operation == 'delete':
                    cache.delete(key)
                    results.append(True)
            except Exception as e:
                self.logger.warning(f"Ошибка при резервной операции кэша: {str(e)}")
                results.append(None)
        
        return results
    
    def cache_user_data(self, user_id, data_type, data, timeout=3600):
        """
        Кэширует данные пользователя.
        
        Args:
            user_id: ID пользователя
            data_type: Тип данных
            data: Данные для кэширования
            timeout: Время жизни кэша
        """
        cache_key = f"user:{user_id}:{data_type}"
        
        if self.redis_available:
            try:
                self.redis_client.setex(
                    cache_key,
                    timeout,
                    pickle.dumps(data)
                )
            except Exception as e:
                self.logger.warning(f"Ошибка при кэшировании данных пользователя в Redis: {str(e)}")
        
        cache.set(cache_key, data, timeout=timeout)
    
    def get_cached_user_data(self, user_id, data_type):
        """
        Получает кэшированные данные пользователя.
        
        Args:
            user_id: ID пользователя
            data_type: Тип данных
            
        Returns:
            Данные пользователя или None
        """
        cache_key = f"user:{user_id}:{data_type}"
        
        # Попытка получить из Redis
        if self.redis_available:
            try:
                cached_data = self.redis_client.get(cache_key)
                if cached_data:
                    return pickle.loads(cached_data)
            except Exception as e:
                self.logger.warning(f"Ошибка при получении данных пользователя из Redis: {str(e)}")
        
        # Попытка получить из Flask-Cache
        return cache.get(cache_key)
    
    def invalidate_user_cache(self, user_id):
        """
        Инвалидирует весь кэш пользователя.
        
        Args:
            user_id: ID пользователя
        """
        if self.redis_available:
            try:
                pattern = f"user:{user_id}:*"
                keys_to_delete = self.redis_client.keys(pattern)
                if keys_to_delete:
                    self.redis_client.delete(*keys_to_delete)
                    self.logger.info(f"Инвалидировано {len(keys_to_delete)} ключей пользователя {user_id}")
            except Exception as e:
                self.logger.error(f"Ошибка при инвалидации кэша пользователя в Redis: {str(e)}")
        
        # Flask-Cache не поддерживает шаблоны для удаления, поэтому инвалидируем
        # только известные ключи при необходимости


# Глобальный экземпляр
cache_manager = AdvancedCacheManager()