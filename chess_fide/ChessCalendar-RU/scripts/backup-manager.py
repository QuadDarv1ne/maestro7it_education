#!/usr/bin/env python
"""
Менеджер резервного копирования
Использование: python scripts/backup-manager.py [action]
"""
import sys
import os
import argparse
import logging
import subprocess
import shutil
from datetime import datetime, timedelta
from pathlib import Path
import json
import gzip

# Добавляем корневую директорию в путь
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class BackupManager:
    """Менеджер резервного копирования"""
    
    def __init__(self, backup_dir: str = 'backups'):
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(exist_ok=True)
    
    def create_database_backup(self, db_url: str, compress: bool = True) -> str:
        """
        Создать резервную копию базы данных
        
        Args:
            db_url: URL базы данных
            compress: сжать backup
            
        Returns:
            путь к файлу backup
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Определяем тип БД
        if 'postgresql' in db_url:
            return self._backup_postgresql(db_url, timestamp, compress)
        elif 'sqlite' in db_url:
            return self._backup_sqlite(db_url, timestamp, compress)
        else:
            raise ValueError(f"Unsupported database: {db_url}")
    
    def _backup_postgresql(self, db_url: str, timestamp: str, compress: bool) -> str:
        """Backup PostgreSQL"""
        # Парсим URL
        from urllib.parse import urlparse
        parsed = urlparse(db_url)
        
        filename = f"postgres_backup_{timestamp}.sql"
        if compress:
            filename += '.gz'
        
        backup_path = self.backup_dir / filename
        
        # Формируем команду pg_dump
        env = os.environ.copy()
        env['PGPASSWORD'] = parsed.password or ''
        
        cmd = [
            'pg_dump',
            '-h', parsed.hostname or 'localhost',
            '-p', str(parsed.port or 5432),
            '-U', parsed.username or 'postgres',
            '-d', parsed.path.lstrip('/'),
            '--no-owner',
            '--no-acl'
        ]
        
        logger.info(f"Creating PostgreSQL backup: {backup_path}")
        
        try:
            if compress:
                # Сжимаем на лету
                with gzip.open(backup_path, 'wb') as f:
                    result = subprocess.run(
                        cmd,
                        env=env,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        check=True
                    )
                    f.write(result.stdout)
            else:
                with open(backup_path, 'wb') as f:
                    subprocess.run(
                        cmd,
                        env=env,
                        stdout=f,
                        stderr=subprocess.PIPE,
                        check=True
                    )
            
            logger.info(f"Backup created: {backup_path}")
            return str(backup_path)
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Backup failed: {e.stderr.decode()}")
            raise
    
    def _backup_sqlite(self, db_url: str, timestamp: str, compress: bool) -> str:
        """Backup SQLite"""
        # Извлекаем путь к файлу БД
        db_path = db_url.replace('sqlite:///', '')
        
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"Database file not found: {db_path}")
        
        filename = f"sqlite_backup_{timestamp}.db"
        if compress:
            filename += '.gz'
        
        backup_path = self.backup_dir / filename
        
        logger.info(f"Creating SQLite backup: {backup_path}")
        
        try:
            if compress:
                with open(db_path, 'rb') as f_in:
                    with gzip.open(backup_path, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
            else:
                shutil.copy2(db_path, backup_path)
            
            logger.info(f"Backup created: {backup_path}")
            return str(backup_path)
            
        except Exception as e:
            logger.error(f"Backup failed: {e}")
            raise
    
    def restore_database_backup(self, backup_file: str, db_url: str):
        """
        Восстановить базу данных из backup
        
        Args:
            backup_file: путь к файлу backup
            db_url: URL базы данных
        """
        if not os.path.exists(backup_file):
            raise FileNotFoundError(f"Backup file not found: {backup_file}")
        
        # Определяем тип БД
        if 'postgresql' in db_url:
            self._restore_postgresql(backup_file, db_url)
        elif 'sqlite' in db_url:
            self._restore_sqlite(backup_file, db_url)
        else:
            raise ValueError(f"Unsupported database: {db_url}")
    
    def _restore_postgresql(self, backup_file: str, db_url: str):
        """Восстановление PostgreSQL"""
        from urllib.parse import urlparse
        parsed = urlparse(db_url)
        
        env = os.environ.copy()
        env['PGPASSWORD'] = parsed.password or ''
        
        cmd = [
            'psql',
            '-h', parsed.hostname or 'localhost',
            '-p', str(parsed.port or 5432),
            '-U', parsed.username or 'postgres',
            '-d', parsed.path.lstrip('/')
        ]
        
        logger.info(f"Restoring PostgreSQL from: {backup_file}")
        
        try:
            if backup_file.endswith('.gz'):
                # Распаковываем на лету
                with gzip.open(backup_file, 'rb') as f:
                    subprocess.run(
                        cmd,
                        env=env,
                        stdin=f,
                        stderr=subprocess.PIPE,
                        check=True
                    )
            else:
                with open(backup_file, 'rb') as f:
                    subprocess.run(
                        cmd,
                        env=env,
                        stdin=f,
                        stderr=subprocess.PIPE,
                        check=True
                    )
            
            logger.info("Database restored successfully")
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Restore failed: {e.stderr.decode()}")
            raise
    
    def _restore_sqlite(self, backup_file: str, db_url: str):
        """Восстановление SQLite"""
        db_path = db_url.replace('sqlite:///', '')
        
        logger.info(f"Restoring SQLite from: {backup_file}")
        
        try:
            # Создаем backup текущей БД
            if os.path.exists(db_path):
                backup_current = f"{db_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                shutil.copy2(db_path, backup_current)
                logger.info(f"Current database backed up to: {backup_current}")
            
            # Восстанавливаем
            if backup_file.endswith('.gz'):
                with gzip.open(backup_file, 'rb') as f_in:
                    with open(db_path, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
            else:
                shutil.copy2(backup_file, db_path)
            
            logger.info("Database restored successfully")
            
        except Exception as e:
            logger.error(f"Restore failed: {e}")
            raise
    
    def list_backups(self) -> list:
        """Список всех backups"""
        backups = []
        
        for file in self.backup_dir.glob('*_backup_*'):
            stat = file.stat()
            backups.append({
                'filename': file.name,
                'path': str(file),
                'size': stat.st_size,
                'size_mb': round(stat.st_size / (1024 * 1024), 2),
                'created': datetime.fromtimestamp(stat.st_ctime).isoformat()
            })
        
        # Сортируем по дате создания (новые первые)
        backups.sort(key=lambda x: x['created'], reverse=True)
        
        return backups
    
    def cleanup_old_backups(self, keep_days: int = 30, keep_count: int = 10):
        """
        Очистка старых backups
        
        Args:
            keep_days: хранить backups за последние N дней
            keep_count: минимальное количество backups для хранения
        """
        backups = self.list_backups()
        
        if len(backups) <= keep_count:
            logger.info(f"Only {len(backups)} backups, keeping all")
            return
        
        cutoff_date = datetime.now() - timedelta(days=keep_days)
        deleted_count = 0
        
        # Оставляем последние keep_count backups
        for backup in backups[keep_count:]:
            created = datetime.fromisoformat(backup['created'])
            
            if created < cutoff_date:
                try:
                    os.remove(backup['path'])
                    deleted_count += 1
                    logger.info(f"Deleted old backup: {backup['filename']}")
                except Exception as e:
                    logger.error(f"Failed to delete {backup['filename']}: {e}")
        
        logger.info(f"Cleanup completed: {deleted_count} backups deleted")
    
    def create_full_backup(self, db_url: str, include_files: list = None) -> str:
        """
        Создать полный backup (БД + файлы)
        
        Args:
            db_url: URL базы данных
            include_files: список директорий для включения
            
        Returns:
            путь к архиву
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f"full_backup_{timestamp}"
        backup_path = self.backup_dir / backup_name
        backup_path.mkdir(exist_ok=True)
        
        logger.info(f"Creating full backup: {backup_path}")
        
        # Backup БД
        db_backup = self.create_database_backup(db_url, compress=True)
        shutil.move(db_backup, backup_path / Path(db_backup).name)
        
        # Backup файлов
        if include_files:
            for directory in include_files:
                if os.path.exists(directory):
                    dest = backup_path / Path(directory).name
                    shutil.copytree(directory, dest, dirs_exist_ok=True)
                    logger.info(f"Backed up directory: {directory}")
        
        # Создаем метаданные
        metadata = {
            'timestamp': timestamp,
            'database_url': db_url.split('@')[-1],  # Скрываем credentials
            'included_directories': include_files or [],
            'created_at': datetime.now().isoformat()
        }
        
        with open(backup_path / 'metadata.json', 'w') as f:
            json.dump(metadata, f, indent=2)
        
        # Архивируем
        archive_path = f"{backup_path}.tar.gz"
        shutil.make_archive(str(backup_path), 'gztar', self.backup_dir, backup_name)
        
        # Удаляем временную директорию
        shutil.rmtree(backup_path)
        
        logger.info(f"Full backup created: {archive_path}")
        return archive_path


def main():
    parser = argparse.ArgumentParser(description='Backup manager')
    parser.add_argument(
        'action',
        choices=['create', 'restore', 'list', 'cleanup', 'full'],
        help='Action to perform'
    )
    parser.add_argument(
        '--db-url',
        help='Database URL'
    )
    parser.add_argument(
        '--backup-file',
        help='Backup file for restore'
    )
    parser.add_argument(
        '--backup-dir',
        default='backups',
        help='Backup directory (default: backups)'
    )
    parser.add_argument(
        '--compress',
        action='store_true',
        help='Compress backup'
    )
    parser.add_argument(
        '--keep-days',
        type=int,
        default=30,
        help='Keep backups for N days (default: 30)'
    )
    parser.add_argument(
        '--keep-count',
        type=int,
        default=10,
        help='Keep at least N backups (default: 10)'
    )
    parser.add_argument(
        '--include-files',
        nargs='+',
        help='Directories to include in full backup'
    )
    
    args = parser.parse_args()
    
    manager = BackupManager(args.backup_dir)
    
    try:
        if args.action == 'create':
            if not args.db_url:
                logger.error("--db-url is required for create action")
                return 1
            
            backup_file = manager.create_database_backup(args.db_url, args.compress)
            logger.info(f"✓ Backup created: {backup_file}")
        
        elif args.action == 'restore':
            if not args.db_url or not args.backup_file:
                logger.error("--db-url and --backup-file are required for restore action")
                return 1
            
            manager.restore_database_backup(args.backup_file, args.db_url)
            logger.info("✓ Database restored successfully")
        
        elif args.action == 'list':
            backups = manager.list_backups()
            
            if not backups:
                logger.info("No backups found")
            else:
                logger.info(f"\nFound {len(backups)} backups:")
                for backup in backups:
                    logger.info(f"  - {backup['filename']} ({backup['size_mb']} MB) - {backup['created']}")
        
        elif args.action == 'cleanup':
            manager.cleanup_old_backups(args.keep_days, args.keep_count)
            logger.info("✓ Cleanup completed")
        
        elif args.action == 'full':
            if not args.db_url:
                logger.error("--db-url is required for full backup")
                return 1
            
            archive = manager.create_full_backup(args.db_url, args.include_files)
            logger.info(f"✓ Full backup created: {archive}")
        
        return 0
        
    except Exception as e:
        logger.error(f"✗ Operation failed: {e}", exc_info=True)
        return 1


if __name__ == '__main__':
    sys.exit(main())
