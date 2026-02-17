#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Декораторы для кэширования запросов к БД
"""

import logging
import hashlib
import json
from functools import wraps
from typing import Any, Callable, Optional
from flask import request

logger = logging.getLogger('chess_calendar')


def cache_key_from_args(*args, **kwargs) -> str:
    """
    Генерация ключа кэша из аргументов функции
    
    Args:
        *args: Позиционные аргументы
        **kwargs: Именованные аргументы
    
    Returns:
        Хэш строка для использования как ключ кэша
    """
    # Создаём строку из аргументов
    key_parts = []
    
    for arg in args:
        if hasattr(arg, 'id'):  # Для объектов с ID
            key_parts.append(f"{type(arg).__name__}:{arg.id}")
        else:
            key_parts.append(str(arg))
    
    for k, v in sorted(kwargs.items()):
        if hasattr(v, 'id'):
            key_parts.append(f"{k}:{type(v).__name__}:{v.id}")
        else:
            key_parts.append(f"{k}:{v}")
    
    key_string = "|".join(key_parts)
    
    # Создаём хэш для короткого ключа
    return hashlib.md5(key_string.encode()).hexdigest()


def cached_query(timeout: int = 300, key_prefix: Optional[str] = None):
    """
    Декоратор для кэширования результатов запросов к БД
    
    Args:
        timeout: Время жизни кэша в секундах (по умолчанию 5 минут)
        key_prefix: Префикс для ключа кэша
    
    Example:
        @cached_query(timeout=600, key_prefix='tournaments')
        def get_tournaments_by_category(category):
            return Tournament.query.filter_by(category=category).all()
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Пытаемся получить кэш
            try:
                from app.utils.unified_cache import cache
                
                # Генерируем ключ кэша
                func_name = func.__name__
                args_key = cache_key_from_args(*args, **kwargs)
                
                if key_prefix:
                    cache_key = f"{key_prefix}:{func_name}:{args_key}"
                else:
                    cache_key = f"query:{func_name}:{args_key}"
                
                # Проверяем кэш
                cached_result = cache.get(cache_key)
                if cached_result is not None:
                    logger.debug(f"Cache hit: {cache_key}")
                    return cached_result
                
                # Выполняем функцию
                result = func(*args, **kwargs)
                
                # Сохраняем в кэш
                cache.set(cache_key, result, timeout)
                logger.debug(f"Cache set: {cache_key}")
                
                return result
                
            except Exception as e:
                # Если кэш недоступен, просто выполняем функцию
                logger.warning(f"Cache error in {func_name}: {e}")
                return func(*args, **kwargs)
        
        return wrapper
    return decorator


def invalidate_cache(key_pattern: str):
    """
    Инвалидация кэша по паттерну
    
    Args:
        key_pattern: Паттерн ключа для инвалидации
    
    Example:
        invalidate_cache('tournaments:*')
    """
    try:
        from app.utils.unified_cache import cache
        cache.delete_pattern(key_pattern)
        logger.info(f"Cache invalidated: {key_pattern}")
    except Exception as e:
        logger.error(f"Failed to invalidate cache: {e}")


def cache_page(timeout: int = 300, query_string: bool = False):
    """
    Декоратор для кэширования целых страниц/view функций
    
    Args:
        timeout: Время жизни кэша в секундах
        query_string: Учитывать ли query string в ключе кэша
    
    Example:
        @app.route('/tournaments')
        @cache_page(timeout=600, query_string=True)
        def tournaments_list():
            return render_template('tournaments.html')
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                from app.utils.unified_cache import cache
                
                # Генерируем ключ кэша на основе URL
                cache_key = f"page:{request.path}"
                
                if query_string and request.query_string:
                    cache_key += f"?{request.query_string.decode()}"
                
                # Проверяем кэш
                cached_result = cache.get(cache_key)
                if cached_result is not None:
                    logger.debug(f"Page cache hit: {cache_key}")
                    return cached_result
                
                # Выполняем функцию
                result = func(*args, **kwargs)
                
                # Сохраняем в кэш только успешные ответы
                if hasattr(result, 'status_code'):
                    if result.status_code == 200:
                        cache.set(cache_key, result, timeout)
                        logger.debug(f"Page cache set: {cache_key}")
                else:
                    cache.set(cache_key, result, timeout)
                    logger.debug(f"Page cache set: {cache_key}")
                
                return result
                
            except Exception as e:
                logger.warning(f"Page cache error: {e}")
                return func(*args, **kwargs)
        
        return wrapper
    return decorator


class CacheManager:
    """Менеджер кэша для управления инвалидацией"""
    
    @staticmethod
    def invalidate_tournament_cache(tournament_id: Optional[int] = None):
        """
        Инвалидация кэша турниров
        
        Args:
            tournament_id: ID конкретного турнира (опционально)
        """
        if tournament_id:
            invalidate_cache(f'tournaments:*:{tournament_id}:*')
            invalidate_cache(f'query:*tournament*:{tournament_id}*')
        else:
            invalidate_cache('tournaments:*')
            invalidate_cache('query:*tournament*')
            invalidate_cache('page:/tournaments*')
            invalidate_cache('page:/calendar*')
    
    @staticmethod
    def invalidate_user_cache(user_id: Optional[int] = None):
        """
        Инвалидация кэша пользователей
        
        Args:
            user_id: ID конкретного пользователя (опционально)
        """
        if user_id:
            invalidate_cache(f'users:*:{user_id}:*')
            invalidate_cache(f'query:*user*:{user_id}*')
        else:
            invalidate_cache('users:*')
            invalidate_cache('query:*user*')
    
    @staticmethod
    def invalidate_all():
        """Полная очистка кэша"""
        try:
            from app.utils.unified_cache import cache
            cache.clear()
            logger.info("All cache cleared")
        except Exception as e:
            logger.error(f"Failed to clear all cache: {e}")
    
    @staticmethod
    def get_cache_stats() -> dict:
        """
        Получить статистику кэша
        
        Returns:
            Словарь со статистикой
        """
        try:
            from app.utils.unified_cache import cache
            return cache.get_stats()
        except Exception as e:
            logger.error(f"Failed to get cache stats: {e}")
            return {'error': str(e)}


# Глобальный экземпляр
cache_manager = CacheManager()
