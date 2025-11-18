"""
Оптимизация производительности Simple HR
==========================================

Этот модуль содержит вспомогательные функции для оптимизации производительности приложения.
"""

from functools import wraps
from flask import g
from sqlalchemy.orm import joinedload, selectinload
from app import cache
import time
import logging

logger = logging.getLogger(__name__)


def measure_time(func):
    """Декоратор для измерения времени выполнения функции"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        
        if execution_time > 1.0:  # Логируем только медленные запросы (>1 сек)
            logger.warning(f"Slow function {func.__name__}: {execution_time:.2f}s")
        
        return result
    return wrapper


def cache_for(timeout=300):
    """
    Декоратор для кэширования результатов функции с использованием Flask-Caching
    
    Args:
        timeout: Время жизни кэша в секундах (по умолчанию 5 минут)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Создаем ключ кэша на основе имени функции и аргументов
            cache_key = f"{func.__name__}_{hash(str(args) + str(sorted(kwargs.items())))}"
            
            # Проверяем кэш
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                logger.debug(f"Cache hit for {func.__name__}")
                return cached_result
            
            # Выполняем функцию и сохраняем результат в кэш
            result = func(*args, **kwargs)
            cache.set(cache_key, result, timeout=timeout)
            logger.debug(f"Cache set for {func.__name__}")
            
            return result
        return wrapper
    return decorator


def get_optimized_employee_query():
    """
    Возвращает оптимизированный запрос для сотрудников с eager loading
    
    Использует joinedload для предотвращения N+1 проблемы при загрузке
    связанных department и position
    """
    from app.models import Employee
    
    return Employee.query.options(
        joinedload(Employee.department),
        joinedload(Employee.position)
    )


def get_optimized_vacation_query():
    """
    Возвращает оптимизированный запрос для отпусков с eager loading
    """
    from app.models import Vacation
    
    return Vacation.query.options(
        joinedload(Vacation.employee).joinedload('department'),
        joinedload(Vacation.employee).joinedload('position')
    )


def get_optimized_order_query():
    """
    Возвращает оптимизированный запрос для приказов с eager loading
    """
    from app.models import Order
    
    return Order.query.options(
        joinedload(Order.employee).joinedload('department'),
        joinedload(Order.employee).joinedload('position'),
        joinedload(Order.new_department),
        joinedload(Order.new_position)
    )


def bulk_insert(model_class, data_list):
    """
    Массовая вставка записей для улучшения производительности
    
    Args:
        model_class: Класс модели SQLAlchemy
        data_list: Список словарей с данными для вставки
    
    Returns:
        Количество вставленных записей
    """
    from app import db
    
    try:
        objects = [model_class(**data) for data in data_list]
        db.session.bulk_save_objects(objects)
        db.session.commit()
        logger.info(f"Bulk inserted {len(objects)} {model_class.__name__} records")
        return len(objects)
    except Exception as e:
        db.session.rollback()
        logger.error(f"Bulk insert error: {str(e)}")
        raise


def paginate_efficiently(query, page=1, per_page=20):
    """
    Эффективная пагинация с подсчетом только при необходимости
    
    Args:
        query: SQLAlchemy query объект
        page: Номер страницы
        per_page: Количество элементов на странице
    
    Returns:
        Объект пагинации
    """
    # Используем limit/offset вместо slice для лучшей производительности
    items = query.limit(per_page).offset((page - 1) * per_page).all()
    
    # Подсчитываем total только если это первая страница или нет элементов
    if page == 1 or not items:
        total = query.count()
    else:
        # Для последующих страниц используем приблизительную оценку
        total = page * per_page + 1
    
    return {
        'items': items,
        'page': page,
        'per_page': per_page,
        'total': total,
        'pages': (total + per_page - 1) // per_page,
        'has_next': len(items) == per_page,
        'has_prev': page > 1
    }


class QueryTimer:
    """Контекстный менеджер для измерения времени выполнения запросов"""
    
    def __init__(self, description="Query"):
        self.description = description
        self.start_time = None
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        execution_time = time.time() - self.start_time
        if execution_time > 0.1:  # Логируем запросы >100мс
            logger.info(f"{self.description}: {execution_time:.3f}s")


def invalidate_employee_cache():
    """Инвалидация кэша, связанного с сотрудниками"""
    keys_to_delete = [
        'get_cached_employee_data',
        'employee_list',
        'employee_statistics'
    ]
    for key in keys_to_delete:
        try:
            cache.delete(key)
        except Exception as e:
            logger.error(f"Error invalidating cache key {key}: {str(e)}")


def preload_common_data():
    """
    Предзагрузка часто используемых данных в кэш при старте приложения
    """
    from app.models import Department, Position
    
    try:
        # Кэшируем список департаментов
        departments = Department.query.all()
        cache.set('departments_list', departments, timeout=3600)
        
        # Кэшируем список должностей
        positions = Position.query.all()
        cache.set('positions_list', positions, timeout=3600)
        
        logger.info("Common data preloaded into cache")
    except Exception as e:
        logger.error(f"Error preloading common data: {str(e)}")


# SQL Query optimization helpers

def optimize_query_with_hints(query):
    """
    Добавляет подсказки оптимизатору для улучшения производительности
    (работает с некоторыми СУБД)
    """
    # Для MySQL можно добавить USE INDEX hints
    # Для PostgreSQL можно использовать pg_hint_plan
    # Для SQLite подсказки не поддерживаются
    return query


def get_index_usage_stats():
    """
    Получает статистику использования индексов (для PostgreSQL)
    Помогает определить неиспользуемые индексы
    """
    from app import db
    
    try:
        result = db.session.execute("""
            SELECT 
                schemaname,
                tablename,
                indexname,
                idx_scan as scans,
                idx_tup_read as tuples_read,
                idx_tup_fetch as tuples_fetched
            FROM pg_stat_user_indexes
            ORDER BY idx_scan ASC
            LIMIT 20
        """)
        return result.fetchall()
    except Exception as e:
        logger.info(f"Index stats not available (possibly not PostgreSQL): {str(e)}")
        return []


def analyze_slow_queries():
    """
    Анализирует медленные запросы (для PostgreSQL)
    """
    from app import db
    
    try:
        result = db.session.execute("""
            SELECT 
                calls,
                total_time,
                mean_time,
                max_time,
                query
            FROM pg_stat_statements
            WHERE mean_time > 100
            ORDER BY mean_time DESC
            LIMIT 10
        """)
        return result.fetchall()
    except Exception as e:
        logger.info(f"Query analysis not available: {str(e)}")
        return []
