"""
Утилиты для оптимизации работы с базой данных
"""
from sqlalchemy import event, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import joinedload, selectinload, subqueryload
from flask_sqlalchemy import SQLAlchemy
import time
import logging

logger = logging.getLogger(__name__)


class QueryOptimizer:
    """Оптимизатор запросов к БД"""
    
    @staticmethod
    def enable_query_logging(app):
        """Включить логирование медленных запросов"""
        
        @event.listens_for(Engine, "before_cursor_execute")
        def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
            conn.info.setdefault('query_start_time', []).append(time.time())
        
        @event.listens_for(Engine, "after_cursor_execute")
        def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
            total = time.time() - conn.info['query_start_time'].pop(-1)
            
            # Логируем медленные запросы (> 100ms)
            if total > 0.1:
                logger.warning(f"Slow query ({total:.3f}s): {statement[:200]}")
        
        logger.info("Query logging enabled")
    
    @staticmethod
    def enable_connection_pooling(app, pool_size=10, max_overflow=20):
        """Настройка connection pooling"""
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
            'pool_size': pool_size,
            'pool_recycle': 3600,
            'pool_pre_ping': True,
            'max_overflow': max_overflow,
            'pool_timeout': 30
        }
        logger.info(f"Connection pooling configured: pool_size={pool_size}, max_overflow={max_overflow}")
    
    @staticmethod
    def optimize_postgresql(db: SQLAlchemy):
        """Оптимизация для PostgreSQL"""
        with db.engine.connect() as conn:
            # Включаем параллельные запросы
            conn.execute(text("SET max_parallel_workers_per_gather = 4"))
            
            # Оптимизация планировщика
            conn.execute(text("SET random_page_cost = 1.1"))
            conn.execute(text("SET effective_cache_size = '1GB'"))
            
            conn.commit()
        
        logger.info("PostgreSQL optimizations applied")


class EagerLoadingMixin:
    """Mixin для автоматической загрузки связанных данных"""
    
    @classmethod
    def with_relationships(cls, *relationships):
        """
        Загрузить объекты со связанными данными
        
        Пример:
            Tournament.with_relationships('ratings', 'favorites').all()
        """
        query = cls.query
        for rel in relationships:
            query = query.options(joinedload(getattr(cls, rel)))
        return query
    
    @classmethod
    def with_selectin(cls, *relationships):
        """
        Загрузить объекты со связанными данными через SELECT IN
        Лучше для one-to-many отношений
        """
        query = cls.query
        for rel in relationships:
            query = query.options(selectinload(getattr(cls, rel)))
        return query


class PaginationHelper:
    """Помощник для пагинации с оптимизацией"""
    
    @staticmethod
    def paginate(query, page=1, per_page=20, max_per_page=100):
        """
        Оптимизированная пагинация
        
        Args:
            query: SQLAlchemy query
            page: Номер страницы
            per_page: Элементов на странице
            max_per_page: Максимум элементов на странице
        
        Returns:
            dict с результатами и метаданными
        """
        if per_page > max_per_page:
            per_page = max_per_page
        
        # Используем offset/limit вместо slice для лучшей производительности
        total = query.count()
        items = query.offset((page - 1) * per_page).limit(per_page).all()
        
        return {
            'items': items,
            'total': total,
            'page': page,
            'per_page': per_page,
            'pages': (total + per_page - 1) // per_page,
            'has_next': page * per_page < total,
            'has_prev': page > 1
        }
    
    @staticmethod
    def cursor_paginate(query, cursor=None, per_page=20):
        """
        Cursor-based пагинация (лучше для больших датасетов)
        
        Args:
            query: SQLAlchemy query (должен быть отсортирован по id)
            cursor: ID последнего элемента с предыдущей страницы
            per_page: Элементов на странице
        
        Returns:
            dict с результатами и курсором
        """
        if cursor:
            query = query.filter(query.column_descriptions[0]['type'].id > cursor)
        
        items = query.limit(per_page + 1).all()
        
        has_next = len(items) > per_page
        if has_next:
            items = items[:-1]
        
        next_cursor = items[-1].id if items and has_next else None
        
        return {
            'items': items,
            'next_cursor': next_cursor,
            'has_next': has_next
        }


class BulkOperations:
    """Массовые операции с БД"""
    
    @staticmethod
    def bulk_insert(db: SQLAlchemy, model_class, data_list, batch_size=1000):
        """
        Массовая вставка данных
        
        Args:
            db: SQLAlchemy instance
            model_class: Класс модели
            data_list: Список словарей с данными
            batch_size: Размер батча
        """
        total = len(data_list)
        inserted = 0
        
        for i in range(0, total, batch_size):
            batch = data_list[i:i + batch_size]
            db.session.bulk_insert_mappings(model_class, batch)
            db.session.commit()
            inserted += len(batch)
            logger.info(f"Bulk insert progress: {inserted}/{total}")
        
        logger.info(f"Bulk insert completed: {total} records")
        return total
    
    @staticmethod
    def bulk_update(db: SQLAlchemy, model_class, data_list, batch_size=1000):
        """
        Массовое обновление данных
        
        Args:
            db: SQLAlchemy instance
            model_class: Класс модели
            data_list: Список словарей с данными (должны содержать id)
            batch_size: Размер батча
        """
        total = len(data_list)
        updated = 0
        
        for i in range(0, total, batch_size):
            batch = data_list[i:i + batch_size]
            db.session.bulk_update_mappings(model_class, batch)
            db.session.commit()
            updated += len(batch)
            logger.info(f"Bulk update progress: {updated}/{total}")
        
        logger.info(f"Bulk update completed: {total} records")
        return total
    
    @staticmethod
    def bulk_delete(db: SQLAlchemy, model_class, ids, batch_size=1000):
        """
        Массовое удаление по ID
        
        Args:
            db: SQLAlchemy instance
            model_class: Класс модели
            ids: Список ID для удаления
            batch_size: Размер батча
        """
        total = len(ids)
        deleted = 0
        
        for i in range(0, total, batch_size):
            batch = ids[i:i + batch_size]
            model_class.query.filter(model_class.id.in_(batch)).delete(synchronize_session=False)
            db.session.commit()
            deleted += len(batch)
            logger.info(f"Bulk delete progress: {deleted}/{total}")
        
        logger.info(f"Bulk delete completed: {total} records")
        return total


class QueryCache:
    """Кэширование результатов запросов"""
    
    def __init__(self, cache_manager):
        self.cache = cache_manager
    
    def cached_query(self, query, cache_key, timeout=300):
        """
        Выполнить запрос с кэшированием
        
        Args:
            query: SQLAlchemy query
            cache_key: Ключ кэша
            timeout: Время жизни кэша
        
        Returns:
            Результаты запроса
        """
        # Проверяем кэш
        cached_result = self.cache.get(cache_key)
        if cached_result is not None:
            logger.debug(f"Query cache hit: {cache_key}")
            return cached_result
        
        # Выполняем запрос
        result = query.all()
        
        # Кэшируем результат
        self.cache.set(cache_key, result, timeout)
        logger.debug(f"Query cached: {cache_key}")
        
        return result
    
    def invalidate_query(self, cache_key):
        """Инвалидировать кэш запроса"""
        self.cache.delete(cache_key)


class DatabaseAnalyzer:
    """Анализатор производительности БД"""
    
    @staticmethod
    def analyze_table(db: SQLAlchemy, table_name: str):
        """
        Анализ таблицы (PostgreSQL)
        
        Args:
            db: SQLAlchemy instance
            table_name: Имя таблицы
        """
        with db.engine.connect() as conn:
            # ANALYZE для обновления статистики
            conn.execute(text(f"ANALYZE {table_name}"))
            conn.commit()
        
        logger.info(f"Table analyzed: {table_name}")
    
    @staticmethod
    def get_table_stats(db: SQLAlchemy, table_name: str):
        """
        Получить статистику таблицы
        
        Args:
            db: SQLAlchemy instance
            table_name: Имя таблицы
        
        Returns:
            dict со статистикой
        """
        with db.engine.connect() as conn:
            # Размер таблицы
            result = conn.execute(text(f"""
                SELECT 
                    pg_size_pretty(pg_total_relation_size('{table_name}')) as total_size,
                    pg_size_pretty(pg_relation_size('{table_name}')) as table_size,
                    pg_size_pretty(pg_indexes_size('{table_name}')) as indexes_size
            """))
            
            row = result.fetchone()
            
            return {
                'total_size': row[0],
                'table_size': row[1],
                'indexes_size': row[2]
            }
    
    @staticmethod
    def get_slow_queries(db: SQLAlchemy, limit=10):
        """
        Получить медленные запросы (PostgreSQL с pg_stat_statements)
        
        Args:
            db: SQLAlchemy instance
            limit: Количество запросов
        
        Returns:
            list медленных запросов
        """
        with db.engine.connect() as conn:
            result = conn.execute(text(f"""
                SELECT 
                    query,
                    calls,
                    total_time,
                    mean_time,
                    max_time
                FROM pg_stat_statements
                ORDER BY mean_time DESC
                LIMIT {limit}
            """))
            
            return [dict(row) for row in result]
    
    @staticmethod
    def vacuum_analyze(db: SQLAlchemy, table_name: str = None):
        """
        VACUUM ANALYZE для оптимизации (PostgreSQL)
        
        Args:
            db: SQLAlchemy instance
            table_name: Имя таблицы (опционально)
        """
        with db.engine.connect() as conn:
            if table_name:
                conn.execute(text(f"VACUUM ANALYZE {table_name}"))
            else:
                conn.execute(text("VACUUM ANALYZE"))
            conn.commit()
        
        logger.info(f"VACUUM ANALYZE completed for {table_name or 'all tables'}")


# Декораторы для оптимизации
def with_eager_loading(*relationships):
    """
    Декоратор для автоматической загрузки связанных данных
    
    Пример:
        @with_eager_loading('ratings', 'favorites')
        def get_tournament(id):
            return Tournament.query.get(id)
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Модифицируем query если он возвращается
            result = func(*args, **kwargs)
            if hasattr(result, 'options'):
                for rel in relationships:
                    result = result.options(joinedload(rel))
            return result
        return wrapper
    return decorator


def readonly_query(func):
    """
    Декоратор для read-only запросов
    Использует read replica если доступна
    """
    def wrapper(*args, **kwargs):
        # Здесь можно добавить логику для использования read replica
        return func(*args, **kwargs)
    return wrapper
