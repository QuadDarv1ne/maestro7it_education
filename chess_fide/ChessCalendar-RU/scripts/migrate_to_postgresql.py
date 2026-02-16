#!/usr/bin/env python
"""
Скрипт миграции данных из SQLite в PostgreSQL
Использование: python scripts/migrate_to_postgresql.py
"""

import sys
import os
from pathlib import Path

# Добавляем корневую директорию в путь
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DatabaseMigrator:
    """Класс для миграции данных между базами данных"""
    
    def __init__(self, source_url, target_url):
        """
        Инициализация мигратора
        
        Args:
            source_url: URL источника (SQLite)
            target_url: URL назначения (PostgreSQL)
        """
        self.source_url = source_url
        self.target_url = target_url
        
        # Создаем движки
        self.source_engine = create_engine(source_url)
        self.target_engine = create_engine(target_url)
        
        # Создаем сессии
        SourceSession = sessionmaker(bind=self.source_engine)
        TargetSession = sessionmaker(bind=self.target_engine)
        
        self.source_session = SourceSession()
        self.target_session = TargetSession()
        
        # Метаданные
        self.source_metadata = MetaData()
        self.target_metadata = MetaData()
        
        logger.info("Database migrator initialized")
    
    def get_tables_to_migrate(self):
        """Получить список таблиц для миграции"""
        self.source_metadata.reflect(bind=self.source_engine)
        tables = list(self.source_metadata.tables.keys())
        
        # Исключаем служебные таблицы
        exclude_tables = ['alembic_version', 'sqlite_sequence']
        tables = [t for t in tables if t not in exclude_tables]
        
        logger.info(f"Found {len(tables)} tables to migrate: {', '.join(tables)}")
        return tables
    
    def create_target_schema(self):
        """Создать схему в целевой БД"""
        logger.info("Creating target database schema...")
        
        try:
            # Импортируем модели для создания схемы
            from app import db, create_app
            
            app = create_app()
            with app.app_context():
                # Устанавливаем URL PostgreSQL
                app.config['SQLALCHEMY_DATABASE_URI'] = self.target_url
                db.engine = self.target_engine
                
                # Создаем все таблицы
                db.create_all()
                
            logger.info("Target schema created successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error creating target schema: {e}")
            return False
    
    def migrate_table(self, table_name):
        """
        Мигрировать данные одной таблицы
        
        Args:
            table_name: Имя таблицы
        """
        logger.info(f"Migrating table: {table_name}")
        
        try:
            # Получаем таблицу из источника
            source_table = Table(table_name, self.source_metadata, autoload_with=self.source_engine)
            
            # Получаем таблицу из назначения
            target_table = Table(table_name, self.target_metadata, autoload_with=self.target_engine)
            
            # Читаем данные из источника
            source_data = self.source_session.execute(source_table.select()).fetchall()
            
            if not source_data:
                logger.info(f"  No data in table {table_name}")
                return True
            
            logger.info(f"  Found {len(source_data)} rows")
            
            # Вставляем данные в назначение
            batch_size = 1000
            for i in range(0, len(source_data), batch_size):
                batch = source_data[i:i + batch_size]
                
                # Конвертируем Row в dict
                batch_dicts = [dict(row._mapping) for row in batch]
                
                # Вставляем батч
                self.target_session.execute(target_table.insert(), batch_dicts)
                self.target_session.commit()
                
                logger.info(f"  Migrated {min(i + batch_size, len(source_data))}/{len(source_data)} rows")
            
            logger.info(f"Table {table_name} migrated successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error migrating table {table_name}: {e}")
            self.target_session.rollback()
            return False
    
    def migrate_all(self):
        """Мигрировать все данные"""
        logger.info("=" * 60)
        logger.info("Starting database migration")
        logger.info(f"Source: {self.source_url}")
        logger.info(f"Target: {self.target_url}")
        logger.info("=" * 60)
        
        start_time = datetime.now()
        
        # Создаем схему в целевой БД
        if not self.create_target_schema():
            logger.error("Failed to create target schema. Aborting migration.")
            return False
        
        # Получаем список таблиц
        tables = self.get_tables_to_migrate()
        
        # Определяем порядок миграции (с учетом внешних ключей)
        # Сначала независимые таблицы, потом зависимые
        table_order = [
            'user',
            'tournament',
            'tournament_rating',
            'favorite_tournament',
            'notification',
            'subscription',
            'tournament_reminder',
            'report',
            'audit_log',
            'forum_post',
            'forum_comment',
            'tournament_subscription',
            'preference'
        ]
        
        # Добавляем таблицы, которых нет в списке
        for table in tables:
            if table not in table_order:
                table_order.append(table)
        
        # Мигрируем таблицы в порядке
        success_count = 0
        failed_tables = []
        
        for table_name in table_order:
            if table_name in tables:
                if self.migrate_table(table_name):
                    success_count += 1
                else:
                    failed_tables.append(table_name)
        
        # Итоги
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        logger.info("=" * 60)
        logger.info("Migration completed")
        logger.info(f"Duration: {duration:.2f} seconds")
        logger.info(f"Successfully migrated: {success_count}/{len(tables)} tables")
        
        if failed_tables:
            logger.warning(f"Failed tables: {', '.join(failed_tables)}")
            return False
        else:
            logger.info("All tables migrated successfully!")
            return True
    
    def verify_migration(self):
        """Проверить результаты миграции"""
        logger.info("=" * 60)
        logger.info("Verifying migration...")
        logger.info("=" * 60)
        
        tables = self.get_tables_to_migrate()
        all_match = True
        
        for table_name in tables:
            try:
                # Подсчитываем строки в источнике
                source_table = Table(table_name, self.source_metadata, autoload_with=self.source_engine)
                source_count = self.source_session.execute(
                    sa.select(sa.func.count()).select_from(source_table)
                ).scalar()
                
                # Подсчитываем строки в назначении
                target_table = Table(table_name, self.target_metadata, autoload_with=self.target_engine)
                target_count = self.target_session.execute(
                    sa.select(sa.func.count()).select_from(target_table)
                ).scalar()
                
                match = source_count == target_count
                status = "✓" if match else "✗"
                
                logger.info(f"{status} {table_name}: {source_count} -> {target_count}")
                
                if not match:
                    all_match = False
                    
            except Exception as e:
                logger.error(f"Error verifying table {table_name}: {e}")
                all_match = False
        
        logger.info("=" * 60)
        if all_match:
            logger.info("Verification passed! All data migrated correctly.")
        else:
            logger.warning("Verification failed! Some data may be missing.")
        
        return all_match
    
    def close(self):
        """Закрыть соединения"""
        self.source_session.close()
        self.target_session.close()
        self.source_engine.dispose()
        self.target_engine.dispose()
        logger.info("Database connections closed")


def main():
    """Главная функция"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Migrate data from SQLite to PostgreSQL')
    parser.add_argument(
        '--source',
        default='sqlite:///chess_calendar.db',
        help='Source database URL (default: sqlite:///chess_calendar.db)'
    )
    parser.add_argument(
        '--target',
        default=None,
        help='Target PostgreSQL URL (e.g., postgresql://user:pass@localhost/dbname)'
    )
    parser.add_argument(
        '--verify-only',
        action='store_true',
        help='Only verify existing migration'
    )
    
    args = parser.parse_args()
    
    # Проверяем наличие target URL
    if not args.target:
        # Пытаемся получить из переменной окружения
        args.target = os.environ.get('POSTGRESQL_URL')
        
        if not args.target:
            logger.error("Target PostgreSQL URL not provided!")
            logger.error("Use --target option or set POSTGRESQL_URL environment variable")
            logger.error("Example: postgresql://user:password@localhost:5432/chess_calendar")
            sys.exit(1)
    
    # Создаем мигратор
    migrator = DatabaseMigrator(args.source, args.target)
    
    try:
        if args.verify_only:
            # Только проверка
            success = migrator.verify_migration()
        else:
            # Полная миграция
            success = migrator.migrate_all()
            
            if success:
                # Проверяем результаты
                migrator.verify_migration()
        
        migrator.close()
        
        if success:
            logger.info("Migration completed successfully!")
            sys.exit(0)
        else:
            logger.error("Migration failed!")
            sys.exit(1)
            
    except KeyboardInterrupt:
        logger.warning("Migration interrupted by user")
        migrator.close()
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        migrator.close()
        sys.exit(1)


if __name__ == '__main__':
    main()
