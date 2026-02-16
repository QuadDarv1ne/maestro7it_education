"""
Система автоматического резервного копирования базы данных
"""
import os
import shutil
import gzip
from datetime import datetime, timedelta
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class BackupManager:
    """Менеджер резервного копирования"""
    
    def __init__(self, app=None):
        self.app = app
        self.backup_dir = None
        self.max_backups = 30
        self.compress = True
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Инициализация менеджера"""
        self.backup_dir = app.config.get('BACKUP_DIR', 'backups')
        self.max_backups = app.config.get('MAX_BACKUPS', 30)
        self.compress = app.config.get('COMPRESS_BACKUPS', True)
        
        # Создание директории для бэкапов
        Path(self.backup_dir).mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Backup manager initialized: {self.backup_dir}")
    
    def create_backup(self, db_path=None):
        """Создать резервную копию базы данных"""
        try:
            if not db_path:
                db_path = 'instance/chess_calendar.db'
            
            if not os.path.exists(db_path):
                logger.error(f"Database file not found: {db_path}")
                return None
            
            # Генерация имени файла
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_name = f"backup_{timestamp}.db"
            backup_path = os.path.join(self.backup_dir, backup_name)
            
            # Копирование базы данных
            shutil.copy2(db_path, backup_path)
            logger.info(f"Backup created: {backup_path}")
            
            # Сжатие если включено
            if self.compress:
                compressed_path = f"{backup_path}.gz"
                with open(backup_path, 'rb') as f_in:
                    with gzip.open(compressed_path, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                
                # Удаление несжатой версии
                os.remove(backup_path)
                backup_path = compressed_path
                logger.info(f"Backup compressed: {compressed_path}")
            
            # Очистка старых бэкапов
            self.cleanup_old_backups()
            
            return backup_path
            
        except Exception as e:
            logger.error(f"Backup creation failed: {e}")
            return None
    
    def restore_backup(self, backup_file, db_path=None):
        """Восстановить базу данных из резервной копии"""
        try:
            if not db_path:
                db_path = 'instance/chess_calendar.db'
            
            backup_path = os.path.join(self.backup_dir, backup_file)
            
            if not os.path.exists(backup_path):
                logger.error(f"Backup file not found: {backup_path}")
                return False
            
            # Создание резервной копии текущей БД перед восстановлением
            if os.path.exists(db_path):
                current_backup = f"{db_path}.before_restore"
                shutil.copy2(db_path, current_backup)
                logger.info(f"Current DB backed up to: {current_backup}")
            
            # Распаковка если сжато
            if backup_path.endswith('.gz'):
                temp_path = backup_path[:-3]
                with gzip.open(backup_path, 'rb') as f_in:
                    with open(temp_path, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                backup_path = temp_path
            
            # Восстановление
            shutil.copy2(backup_path, db_path)
            logger.info(f"Database restored from: {backup_file}")
            
            # Удаление временного файла
            if backup_path.endswith('.db') and not backup_path.startswith(self.backup_dir):
                os.remove(backup_path)
            
            return True
            
        except Exception as e:
            logger.error(f"Backup restoration failed: {e}")
            return False
    
    def list_backups(self):
        """Получить список всех резервных копий"""
        try:
            backups = []
            
            for filename in os.listdir(self.backup_dir):
                if filename.startswith('backup_') and (filename.endswith('.db') or filename.endswith('.db.gz')):
                    filepath = os.path.join(self.backup_dir, filename)
                    stat = os.stat(filepath)
                    
                    backups.append({
                        'filename': filename,
                        'size': stat.st_size,
                        'size_mb': round(stat.st_size / 1024 / 1024, 2),
                        'created': datetime.fromtimestamp(stat.st_ctime),
                        'compressed': filename.endswith('.gz')
                    })
            
            # Сортировка по дате создания (новые первые)
            backups.sort(key=lambda x: x['created'], reverse=True)
            
            return backups
            
        except Exception as e:
            logger.error(f"Failed to list backups: {e}")
            return []
    
    def cleanup_old_backups(self):
        """Удалить старые резервные копии"""
        try:
            backups = self.list_backups()
            
            if len(backups) <= self.max_backups:
                return
            
            # Удаление старых бэкапов
            backups_to_delete = backups[self.max_backups:]
            
            for backup in backups_to_delete:
                filepath = os.path.join(self.backup_dir, backup['filename'])
                os.remove(filepath)
                logger.info(f"Old backup deleted: {backup['filename']}")
            
            logger.info(f"Cleaned up {len(backups_to_delete)} old backups")
            
        except Exception as e:
            logger.error(f"Backup cleanup failed: {e}")
    
    def get_backup_stats(self):
        """Получить статистику резервных копий"""
        backups = self.list_backups()
        
        total_size = sum(b['size'] for b in backups)
        
        return {
            'total_backups': len(backups),
            'total_size_mb': round(total_size / 1024 / 1024, 2),
            'oldest_backup': backups[-1]['created'] if backups else None,
            'newest_backup': backups[0]['created'] if backups else None,
            'backup_dir': self.backup_dir,
            'max_backups': self.max_backups,
            'compression_enabled': self.compress
        }
    
    def schedule_automatic_backups(self, scheduler, interval_hours=24):
        """Настроить автоматическое резервное копирование"""
        try:
            from apscheduler.triggers.interval import IntervalTrigger
            
            scheduler.add_job(
                func=self.create_backup,
                trigger=IntervalTrigger(hours=interval_hours),
                id='automatic_backup',
                name='Automatic database backup',
                replace_existing=True
            )
            
            logger.info(f"Automatic backups scheduled every {interval_hours} hours")
            return True
            
        except Exception as e:
            logger.error(f"Failed to schedule automatic backups: {e}")
            return False


# Глобальный экземпляр
backup_manager = BackupManager()
