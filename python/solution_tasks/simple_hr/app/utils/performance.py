"""
Улучшения производительности и оптимизация запросов
"""
from functools import wraps
from flask import request
from app import cache
import hashlib
import json

def cached_query(timeout=300):
    """
    Декоратор для кеширования результатов запросов к базе данных
    
    Args:
        timeout: время жизни кеша в секундах (по умолчанию 5 минут)
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Создаем уникальный ключ кеша на основе функции и аргументов
            cache_key = f"query_{f.__name__}_{hashlib.md5(str(args).encode() + str(kwargs).encode()).hexdigest()}"
            
            # Проверяем наличие данных в кеше
            cached_data = cache.get(cache_key)
            if cached_data is not None:
                return cached_data
            
            # Выполняем функцию и кешируем результат
            result = f(*args, **kwargs)
            cache.set(cache_key, result, timeout=timeout)
            return result
        
        return decorated_function
    return decorator

def cache_key_with_params(*param_names):
    """
    Создает ключ кеша на основе параметров запроса
    
    Args:
        param_names: список имен параметров для включения в ключ
    """
    params = {name: request.args.get(name) for name in param_names if request.args.get(name)}
    return hashlib.md5(json.dumps(params, sort_keys=True).encode()).hexdigest()

def invalidate_cache(pattern):
    """
    Инвалидирует кеш по паттерну
    
    Args:
        pattern: паттерн для поиска ключей кеша
    """
    try:
        cache.delete_memoized(pattern)
    except Exception:
        # Если не удалось удалить по паттерну, очищаем весь кеш
        cache.clear()

class QueryOptimizer:
    """Оптимизация SQL запросов"""
    
    @staticmethod
    def eager_load_relationships(query, *relationships):
        """
        Добавляет eager loading для указанных связей
        
        Args:
            query: SQLAlchemy query объект
            relationships: список имен связей для загрузки
        """
        from sqlalchemy.orm import joinedload
        
        for rel in relationships:
            query = query.options(joinedload(rel))
        
        return query
    
    @staticmethod
    def paginate_efficiently(query, page=1, per_page=20):
        """
        Эффективная пагинация с минимальным количеством запросов
        
        Args:
            query: SQLAlchemy query объект
            page: номер страницы
            per_page: количество элементов на странице
        """
        # Используем offset/limit вместо slice для лучшей производительности
        total = query.count()
        items = query.offset((page - 1) * per_page).limit(per_page).all()
        
        return {
            'items': items,
            'total': total,
            'page': page,
            'per_page': per_page,
            'pages': (total + per_page - 1) // per_page
        }

class PerformanceMonitor:
    """Мониторинг производительности приложения"""
    
    @staticmethod
    def log_slow_queries(threshold=1.0):
        """
        Логирование медленных SQL запросов
        
        Args:
            threshold: порог времени выполнения в секундах
        """
        from sqlalchemy import event
        from sqlalchemy.engine import Engine
        import time
        import logging
        
        logger = logging.getLogger(__name__)
        
        @event.listens_for(Engine, "before_cursor_execute")
        def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
            conn.info.setdefault('query_start_time', []).append(time.time())
        
        @event.listens_for(Engine, "after_cursor_execute")
        def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
            total_time = time.time() - conn.info['query_start_time'].pop()
            if total_time > threshold:
                logger.warning(f"Slow query detected ({total_time:.2f}s): {statement}")

def batch_process(items, batch_size=100, callback=None):
    """
    Пакетная обработка элементов
    
    Args:
        items: список элементов для обработки
        batch_size: размер пакета
        callback: функция обратного вызова для каждого пакета
    """
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        if callback:
            callback(batch)
        yield batch
