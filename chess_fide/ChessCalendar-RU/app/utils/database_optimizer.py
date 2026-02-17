"""
Оптимизация работы с базой данных
"""
import logging
from typing import List, Dict, Any, Optional
from contextlib import contextmanager
from sqlalchemy import text, event
from sqlalchemy.engine import Engine
from sqlalchemy.pool import Pool
import time

logger = logging.getLogger(__name__)


class DatabaseOptimizer:
    """Оптимизация запросов и работы с БД"""
    
    def __init__(self, db):
        self.db = db
        self.slow_query_threshold = 1.0  # секунды
        
    def enable_query_logging(self):
        """Включить логирование медленных запросов"""
        @event.listens_for(Engine, "before_cursor_execute")
        def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
            conn.info.setdefault('query_start_time', []).append(time.time())
        
        @event.listens_for(Engine, "after_cursor_execute")
        def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
            total = time.time() - conn.info['query_start_time'].pop(-1)
            if total > self.slow_query_threshold:
                logger.warning(
                    f"Slow query detected ({total:.2f}s): {statement[:200]}..."
                )
    
    def analyze_table(self, table_name: str):
        """Анализ таблицы для оптимизации"""
        try:
            # PostgreSQL
            self.db.session.execute(text(f"ANALYZE {table_name}"))
            self.db.session.commit()
            logger.info(f"Table {table_name} analyzed")
        except Exception as e:
            logger.error(f"Failed to analyze table {table_name}: {e}")
            self.db.session.rollback()
    
    def vacuum_table(self, table_name: str, full: bool = False):
        """VACUUM для PostgreSQL"""
        try:
            vacuum_cmd = f"VACUUM {'FULL' if full else ''} {table_name}"
            self.db.session.execute(text(vacuum_cmd))
            self.db.session.commit()
            logger.info(f"Table {table_name} vacuumed")
        except Exception as e:
            logger.error(f"Failed to vacuum table {table_name}: {e}")
            self.db.session.rollback()
    
    def get_table_stats(self, table_name: str) -> Dict[str, Any]:
        """Получить статистику таблицы"""
        try:
            # Размер таблицы
            size_query = text(f"""
                SELECT 
                    pg_size_pretty(pg_total_relation_size('{table_name}')) as total_size,
                    pg_size_pretty(pg_relation_size('{table_name}')) as table_size,
                    pg_size_pretty(pg_indexes_size('{table_name}')) as indexes_size
            """)
            size_result = self.db.session.execute(size_query).fetchone()
            
            # Количество строк
            count_query = text(f"SELECT COUNT(*) FROM {table_name}")
            count_result = self.db.session.execute(count_query).fetchone()
            
            return {
                'table_name': table_name,
                'total_size': size_result[0] if size_result else 'N/A',
                'table_size': size_result[1] if size_result else 'N/A',
                'indexes_size': size_result[2] if size_result else 'N/A',
                'row_count': count_result[0] if count_result else 0
            }
        except Exception as e:
            logger.error(f"Failed to get table stats for {table_name}: {e}")
            return {}
    
    def get_missing_indexes(self) -> List[Dict[str, Any]]:
        """Найти потенциально отсутствующие индексы (PostgreSQL)"""
        try:
            query = text("""
                SELECT 
                    schemaname,
                    tablename,
                    attname,
                    n_distinct,
                    correlation
                FROM pg_stats
                WHERE schemaname = 'public'
                AND n_distinct > 100
                AND correlation < 0.1
                ORDER BY n_distinct DESC
                LIMIT 20
            """)
            
            results = self.db.session.execute(query).fetchall()
            
            suggestions = []
            for row in results:
                suggestions.append({
                    'table': row[1],
                    'column': row[2],
                    'distinct_values': row[3],
                    'correlation': row[4],
                    'suggestion': f"CREATE INDEX idx_{row[1]}_{row[2]} ON {row[1]}({row[2]})"
                })
            
            return suggestions
        except Exception as e:
            logger.error(f"Failed to get missing indexes: {e}")
            return []
    
    def get_unused_indexes(self) -> List[Dict[str, Any]]:
        """Найти неиспользуемые индексы (PostgreSQL)"""
        try:
            query = text("""
                SELECT 
                    schemaname,
                    tablename,
                    indexname,
                    idx_scan,
                    pg_size_pretty(pg_relation_size(indexrelid)) as index_size
                FROM pg_stat_user_indexes
                WHERE idx_scan = 0
                AND indexrelname NOT LIKE '%_pkey'
                ORDER BY pg_relation_size(indexrelid) DESC
            """)
            
            results = self.db.session.execute(query).fetchall()
            
            unused = []
            for row in results:
                unused.append({
                    'schema': row[0],
                    'table': row[1],
                    'index': row[2],
                    'scans': row[3],
                    'size': row[4],
                    'suggestion': f"DROP INDEX {row[2]}"
                })
            
            return unused
        except Exception as e:
            logger.error(f"Failed to get unused indexes: {e}")
            return []
    
    def get_slow_queries(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Получить медленные запросы (требует pg_stat_statements)"""
        try:
            query = text("""
                SELECT 
                    query,
                    calls,
                    total_exec_time,
                    mean_exec_time,
                    max_exec_time,
                    rows
                FROM pg_stat_statements
                ORDER BY mean_exec_time DESC
                LIMIT :limit
            """)
            
            results = self.db.session.execute(query, {'limit': limit}).fetchall()
            
            slow_queries = []
            for row in results:
                slow_queries.append({
                    'query': row[0][:200],
                    'calls': row[1],
                    'total_time_ms': round(row[2], 2),
                    'mean_time_ms': round(row[3], 2),
                    'max_time_ms': round(row[4], 2),
                    'rows': row[5]
                })
            
            return slow_queries
        except Exception as e:
            logger.error(f"Failed to get slow queries: {e}")
            return []
    
    def optimize_all_tables(self):
        """Оптимизировать все таблицы"""
        try:
            # Получаем список всех таблиц
            query = text("""
                SELECT tablename 
                FROM pg_tables 
                WHERE schemaname = 'public'
            """)
            
            tables = self.db.session.execute(query).fetchall()
            
            for table in tables:
                table_name = table[0]
                self.analyze_table(table_name)
                logger.info(f"Optimized table: {table_name}")
            
            logger.info("All tables optimized")
        except Exception as e:
            logger.error(f"Failed to optimize all tables: {e}")


class ConnectionPoolMonitor:
    """Мониторинг пула подключений"""
    
    def __init__(self, engine):
        self.engine = engine
        
    def get_pool_status(self) -> Dict[str, Any]:
        """Получить статус пула подключений"""
        try:
            pool = self.engine.pool
            
            return {
                'size': pool.size(),
                'checked_in': pool.checkedin(),
                'checked_out': pool.checkedout(),
                'overflow': pool.overflow(),
                'total_connections': pool.size() + pool.overflow(),
                'available': pool.size() - pool.checkedout(),
                'status': 'healthy' if pool.checkedout() < pool.size() else 'degraded'
            }
        except Exception as e:
            logger.error(f"Failed to get pool status: {e}")
            return {'status': 'error', 'error': str(e)}
    
    def enable_pool_logging(self):
        """Включить логирование событий пула"""
        @event.listens_for(Pool, "connect")
        def receive_connect(dbapi_conn, connection_record):
            logger.debug("New database connection established")
        
        @event.listens_for(Pool, "checkout")
        def receive_checkout(dbapi_conn, connection_record, connection_proxy):
            logger.debug("Connection checked out from pool")
        
        @event.listens_for(Pool, "checkin")
        def receive_checkin(dbapi_conn, connection_record):
            logger.debug("Connection returned to pool")


class QueryBatcher:
    """Батчинг запросов для оптимизации"""
    
    def __init__(self, db, batch_size: int = 100):
        self.db = db
        self.batch_size = batch_size
    
    def bulk_insert(self, model_class, data: List[Dict[str, Any]]):
        """Массовая вставка данных"""
        try:
            total = len(data)
            inserted = 0
            
            for i in range(0, total, self.batch_size):
                batch = data[i:i + self.batch_size]
                self.db.session.bulk_insert_mappings(model_class, batch)
                self.db.session.commit()
                inserted += len(batch)
                logger.debug(f"Inserted {inserted}/{total} records")
            
            logger.info(f"Bulk insert completed: {total} records")
            return total
        except Exception as e:
            logger.error(f"Bulk insert failed: {e}")
            self.db.session.rollback()
            return 0
    
    def bulk_update(self, model_class, data: List[Dict[str, Any]]):
        """Массовое обновление данных"""
        try:
            total = len(data)
            updated = 0
            
            for i in range(0, total, self.batch_size):
                batch = data[i:i + self.batch_size]
                self.db.session.bulk_update_mappings(model_class, batch)
                self.db.session.commit()
                updated += len(batch)
                logger.debug(f"Updated {updated}/{total} records")
            
            logger.info(f"Bulk update completed: {total} records")
            return total
        except Exception as e:
            logger.error(f"Bulk update failed: {e}")
            self.db.session.rollback()
            return 0


@contextmanager
def query_timer(query_name: str):
    """Контекстный менеджер для измерения времени запроса"""
    start = time.time()
    try:
        yield
    finally:
        elapsed = time.time() - start
        logger.info(f"Query '{query_name}' took {elapsed:.3f}s")


class IndexManager:
    """Управление индексами"""
    
    def __init__(self, db):
        self.db = db
    
    def create_index(self, table_name: str, column_name: str, 
                    index_name: Optional[str] = None, unique: bool = False):
        """Создать индекс"""
        try:
            if not index_name:
                index_name = f"idx_{table_name}_{column_name}"
            
            unique_str = "UNIQUE" if unique else ""
            query = text(f"CREATE {unique_str} INDEX {index_name} ON {table_name}({column_name})")
            
            self.db.session.execute(query)
            self.db.session.commit()
            logger.info(f"Index {index_name} created")
            return True
        except Exception as e:
            logger.error(f"Failed to create index: {e}")
            self.db.session.rollback()
            return False
    
    def drop_index(self, index_name: str):
        """Удалить индекс"""
        try:
            query = text(f"DROP INDEX IF EXISTS {index_name}")
            self.db.session.execute(query)
            self.db.session.commit()
            logger.info(f"Index {index_name} dropped")
            return True
        except Exception as e:
            logger.error(f"Failed to drop index: {e}")
            self.db.session.rollback()
            return False
    
    def rebuild_index(self, index_name: str):
        """Перестроить индекс (PostgreSQL)"""
        try:
            query = text(f"REINDEX INDEX {index_name}")
            self.db.session.execute(query)
            self.db.session.commit()
            logger.info(f"Index {index_name} rebuilt")
            return True
        except Exception as e:
            logger.error(f"Failed to rebuild index: {e}")
            self.db.session.rollback()
            return False
