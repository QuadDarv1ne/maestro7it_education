#!/usr/bin/env python
"""
Скрипт для обслуживания базы данных
Использование: python scripts/db-maintenance.py [action]
"""
import sys
import os
import argparse
import logging
from datetime import datetime, timedelta

# Добавляем корневую директорию в путь
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.utils.database_optimizer import DatabaseOptimizer, ConnectionPoolMonitor, IndexManager

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def analyze_tables(app):
    """Анализ всех таблиц"""
    logger.info("Starting table analysis...")
    
    with app.app_context():
        optimizer = DatabaseOptimizer(db)
        optimizer.optimize_all_tables()
    
    logger.info("Table analysis completed")


def check_indexes(app):
    """Проверка индексов"""
    logger.info("Checking indexes...")
    
    with app.app_context():
        optimizer = DatabaseOptimizer(db)
        
        # Неиспользуемые индексы
        unused = optimizer.get_unused_indexes()
        if unused:
            logger.warning(f"Found {len(unused)} unused indexes:")
            for idx in unused:
                logger.warning(f"  - {idx['index']} on {idx['table']} ({idx['size']})")
                logger.warning(f"    Suggestion: {idx['suggestion']}")
        else:
            logger.info("No unused indexes found")
        
        # Отсутствующие индексы
        missing = optimizer.get_missing_indexes()
        if missing:
            logger.warning(f"Found {len(missing)} potential missing indexes:")
            for idx in missing:
                logger.warning(f"  - {idx['table']}.{idx['column']}")
                logger.warning(f"    Suggestion: {idx['suggestion']}")
        else:
            logger.info("No missing indexes detected")


def check_slow_queries(app):
    """Проверка медленных запросов"""
    logger.info("Checking slow queries...")
    
    with app.app_context():
        optimizer = DatabaseOptimizer(db)
        slow_queries = optimizer.get_slow_queries(limit=10)
        
        if slow_queries:
            logger.warning(f"Found {len(slow_queries)} slow queries:")
            for i, query in enumerate(slow_queries, 1):
                logger.warning(f"\n{i}. Query: {query['query']}")
                logger.warning(f"   Calls: {query['calls']}")
                logger.warning(f"   Mean time: {query['mean_time_ms']}ms")
                logger.warning(f"   Max time: {query['max_time_ms']}ms")
        else:
            logger.info("No slow queries found (pg_stat_statements may not be enabled)")


def get_table_stats(app):
    """Получить статистику таблиц"""
    logger.info("Getting table statistics...")
    
    with app.app_context():
        optimizer = DatabaseOptimizer(db)
        
        # Получаем список таблиц
        from sqlalchemy import text
        result = db.session.execute(text("""
            SELECT tablename 
            FROM pg_tables 
            WHERE schemaname = 'public'
            ORDER BY tablename
        """))
        
        tables = [row[0] for row in result]
        
        logger.info(f"\nTable Statistics:")
        logger.info("-" * 80)
        
        for table in tables:
            stats = optimizer.get_table_stats(table)
            if stats:
                logger.info(f"\n{table}:")
                logger.info(f"  Rows: {stats['row_count']:,}")
                logger.info(f"  Total size: {stats['total_size']}")
                logger.info(f"  Table size: {stats['table_size']}")
                logger.info(f"  Indexes size: {stats['indexes_size']}")


def check_pool_status(app):
    """Проверить статус пула подключений"""
    logger.info("Checking connection pool status...")
    
    with app.app_context():
        monitor = ConnectionPoolMonitor(db.engine)
        status = monitor.get_pool_status()
        
        logger.info(f"\nConnection Pool Status:")
        logger.info(f"  Status: {status.get('status', 'unknown')}")
        logger.info(f"  Pool size: {status.get('size', 0)}")
        logger.info(f"  Checked out: {status.get('checked_out', 0)}")
        logger.info(f"  Checked in: {status.get('checked_in', 0)}")
        logger.info(f"  Overflow: {status.get('overflow', 0)}")
        logger.info(f"  Available: {status.get('available', 0)}")


def vacuum_database(app, full=False):
    """VACUUM база данных"""
    logger.info(f"Running VACUUM {'FULL' if full else ''}...")
    
    with app.app_context():
        optimizer = DatabaseOptimizer(db)
        
        # Получаем список таблиц
        from sqlalchemy import text
        result = db.session.execute(text("""
            SELECT tablename 
            FROM pg_tables 
            WHERE schemaname = 'public'
        """))
        
        tables = [row[0] for row in result]
        
        for table in tables:
            logger.info(f"Vacuuming {table}...")
            optimizer.vacuum_table(table, full=full)
    
    logger.info("VACUUM completed")


def cleanup_old_data(app, days=30):
    """Очистка старых данных"""
    logger.info(f"Cleaning up data older than {days} days...")
    
    with app.app_context():
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        # Очистка старых уведомлений
        from app.models.notification import Notification
        old_notifications = Notification.query.filter(
            Notification.created_at < cutoff_date,
            Notification.read == True
        ).delete()
        
        # Очистка старых логов аудита
        from app.models.audit_log import AuditLog
        old_logs = AuditLog.query.filter(
            AuditLog.timestamp < cutoff_date
        ).delete()
        
        # Очистка старых AB test событий
        from app.models.ab_test_event import ABTestEvent
        old_events = ABTestEvent.query.filter(
            ABTestEvent.timestamp < cutoff_date
        ).delete()
        
        db.session.commit()
        
        logger.info(f"Cleaned up:")
        logger.info(f"  - {old_notifications} old notifications")
        logger.info(f"  - {old_logs} old audit logs")
        logger.info(f"  - {old_events} old AB test events")


def rebuild_indexes(app):
    """Перестроить все индексы"""
    logger.info("Rebuilding indexes...")
    
    with app.app_context():
        from sqlalchemy import text
        
        # Получаем список индексов
        result = db.session.execute(text("""
            SELECT indexname 
            FROM pg_indexes 
            WHERE schemaname = 'public'
            AND indexname NOT LIKE '%_pkey'
        """))
        
        indexes = [row[0] for row in result]
        
        manager = IndexManager(db)
        
        for index in indexes:
            logger.info(f"Rebuilding {index}...")
            manager.rebuild_index(index)
    
    logger.info("Index rebuild completed")


def full_maintenance(app):
    """Полное обслуживание БД"""
    logger.info("Starting full database maintenance...")
    
    analyze_tables(app)
    vacuum_database(app, full=False)
    check_indexes(app)
    check_slow_queries(app)
    get_table_stats(app)
    check_pool_status(app)
    
    logger.info("Full maintenance completed")


def main():
    parser = argparse.ArgumentParser(description='Database maintenance script')
    parser.add_argument(
        'action',
        choices=[
            'analyze', 'vacuum', 'vacuum-full', 'check-indexes',
            'check-slow-queries', 'stats', 'pool-status',
            'cleanup', 'rebuild-indexes', 'full'
        ],
        help='Maintenance action to perform'
    )
    parser.add_argument(
        '--days',
        type=int,
        default=30,
        help='Days for cleanup action (default: 30)'
    )
    
    args = parser.parse_args()
    
    # Создаем приложение
    app = create_app()
    
    # Выполняем действие
    actions = {
        'analyze': lambda: analyze_tables(app),
        'vacuum': lambda: vacuum_database(app, full=False),
        'vacuum-full': lambda: vacuum_database(app, full=True),
        'check-indexes': lambda: check_indexes(app),
        'check-slow-queries': lambda: check_slow_queries(app),
        'stats': lambda: get_table_stats(app),
        'pool-status': lambda: check_pool_status(app),
        'cleanup': lambda: cleanup_old_data(app, days=args.days),
        'rebuild-indexes': lambda: rebuild_indexes(app),
        'full': lambda: full_maintenance(app)
    }
    
    try:
        actions[args.action]()
        logger.info("✓ Maintenance completed successfully")
        return 0
    except Exception as e:
        logger.error(f"✗ Maintenance failed: {e}", exc_info=True)
        return 1


if __name__ == '__main__':
    sys.exit(main())
