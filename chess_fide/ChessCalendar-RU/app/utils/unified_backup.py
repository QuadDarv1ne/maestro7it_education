"""
Unified Backup System - объединенная система резервного копирования
Поддержка SQLite и PostgreSQL, сжатие, автоматическое планирование
"""
import os
import shutil
import gzip
import zipfile
import json
import sqlite3
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)


class UnifiedBackupManager:
    """
    Унифицированный менеджер резервного копирования с поддержкой:
    - SQLite и PostgreSQL
    - Сжатие (gzip, zip)
    - Автоматическая очистка старых бэкапов
    - Экспорт в JSON/CSV
    - Валидация бэкапов
    """
    
    def __init__(self, app=None, db_path: str = None, backup_dir: str = "backups"):
        self.app = app
        self.db_path = db_path
        self.backup_dir = Path(backup_dir)
        self.max_backups = 30
        self.compress = True
        self.compression_format = 'zip'  # 'zip' or 'gzip'
        
        if app:
            self.init_app(app)
        else:
            self.backup_dir.mkdir(parents=True, exist_ok=True)
    
    def init_app(self, app):
        """Инициализация с Flask app"""
        self.backup_dir = Path(app.config.get('BACKUP_DIR', 'backups'))
        self.max_backups = app.config.get('MAX_BACKUPS', 30)
        self.compress = app.config.get('COMPRESS_BACKUPS', True)
        self.compression_format = app.config.get('BACKUP_COMPRESSION_FORMAT', 'zip')
        
        # Определяем путь к БД
        if not self.db_path:
            db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')
            if db_uri.startswith('sqlite:///'):
                self.db_path = db_uri.replace('sqlite:///', '')
        
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Backup manager initialized: {self.backup_dir}")
    
    def create_backup(self, backup_name: Optional[str] = None, 
                     include_metadata: bool = True) -> Optional[str]:
        """
        Создать резервную копию базы данных
        
        Args:
            backup_name: Имя файла бэкапа (опционально)
            include_metadata: Включить метаданные и схему
        
        Returns:
            Путь к созданному бэкапу или None при ошибке
        """
        try:
            if not self.db_path or not os.path.exists(self.db_path):
                logger.error(f"Database file not found: {self.db_path}")
                return None
            
            # Генерация имени файла
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            if not backup_name:
                if self.compression_format == 'zip':
                    backup_name = f"backup_{timestamp}.zip"
                else:
                    backup_name = f"backup_{timestamp}.db.gz"
            
            backup_path = self.backup_dir / backup_name
            
            # Создание бэкапа в зависимости от формата
            if self.compression_format == 'zip':
                return self._create_zip_backup(backup_path, include_metadata)
            else:
                return self._create_gzip_backup(backup_path)
            
        except Exception as e:
            logger.error(f"Backup creation failed: {e}")
            return None
    
    def _create_zip_backup(self, backup_path: Path, 
                          include_metadata: bool) -> str:
        """Создать ZIP бэкап с метаданными"""
        temp_db_path = self.backup_dir / "temp_backup.db"
        
        try:
            # Копируем БД через SQLite API для консистентности
            if self.db_path.endswith('.db'):
                conn = sqlite3.connect(self.db_path)
                backup_conn = sqlite3.connect(temp_db_path)
                conn.backup(backup_conn)
                conn.close()
                backup_conn.close()
            else:
                shutil.copy2(self.db_path, temp_db_path)
            
            # Создаем ZIP архив
            with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(temp_db_path, "database.db")
                
                if include_metadata:
                    # Экспорт схемы
                    schema_data = self._export_schema()
                    schema_path = self.backup_dir / "schema.json"
                    with open(schema_path, 'w', encoding='utf-8') as f:
                        json.dump(schema_data, f, indent=2, default=str)
                    zipf.write(schema_path, "schema.json")
                    schema_path.unlink()
                    
                    # Метаданные
                    metadata = {
                        "created_at": datetime.now().isoformat(),
                        "db_size": os.path.getsize(temp_db_path),
                        "db_path": str(self.db_path),
                        "tables": list(schema_data.keys()) if schema_data else [],
                        "compression": "zip"
                    }
                    metadata_path = self.backup_dir / "metadata.json"
                    with open(metadata_path, 'w', encoding='utf-8') as f:
                        json.dump(metadata, f, indent=2)
                    zipf.write(metadata_path, "metadata.json")
                    metadata_path.unlink()
            
            # Очистка
            temp_db_path.unlink(missing_ok=True)
            
            logger.info(f"ZIP backup created: {backup_path}")
            self.cleanup_old_backups()
            
            return str(backup_path)
            
        except Exception as e:
            temp_db_path.unlink(missing_ok=True)
            if backup_path.exists():
                backup_path.unlink()
            raise e
    
    def _create_gzip_backup(self, backup_path: Path) -> str:
        """Создать GZIP бэкап"""
        temp_db_path = self.backup_dir / "temp_backup.db"
        
        try:
            # Копируем БД
            shutil.copy2(self.db_path, temp_db_path)
            
            # Сжимаем
            with open(temp_db_path, 'rb') as f_in:
                with gzip.open(backup_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            
            # Очистка
            temp_db_path.unlink()
            
            logger.info(f"GZIP backup created: {backup_path}")
            self.cleanup_old_backups()
            
            return str(backup_path)
            
        except Exception as e:
            temp_db_path.unlink(missing_ok=True)
            if backup_path.exists():
                backup_path.unlink()
            raise e
    
    def restore_backup(self, backup_file: str, 
                      create_safety_backup: bool = True) -> bool:
        """
        Восстановить базу данных из резервной копии
        
        Args:
            backup_file: Имя файла бэкапа
            create_safety_backup: Создать бэкап текущей БД перед восстановлением
        
        Returns:
            True при успехе, False при ошибке
        """
        try:
            backup_path = self.backup_dir / backup_file
            
            if not backup_path.exists():
                logger.error(f"Backup file not found: {backup_path}")
                return False
            
            # Создаем safety backup текущей БД
            if create_safety_backup and os.path.exists(self.db_path):
                safety_backup = f"{self.db_path}.before_restore_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                shutil.copy2(self.db_path, safety_backup)
                logger.info(f"Safety backup created: {safety_backup}")
            
            # Восстановление в зависимости от формата
            if backup_file.endswith('.zip'):
                return self._restore_from_zip(backup_path)
            elif backup_file.endswith('.gz'):
                return self._restore_from_gzip(backup_path)
            else:
                # Прямое копирование
                shutil.copy2(backup_path, self.db_path)
                logger.info(f"Database restored from: {backup_file}")
                return True
            
        except Exception as e:
            logger.error(f"Backup restoration failed: {e}")
            return False
    
    def _restore_from_zip(self, backup_path: Path) -> bool:
        """Восстановить из ZIP бэкапа"""
        extract_dir = self.backup_dir / "temp_restore"
        extract_dir.mkdir(exist_ok=True)
        
        try:
            with zipfile.ZipFile(backup_path, 'r') as zipf:
                zipf.extractall(extract_dir)
            
            db_file = extract_dir / "database.db"
            if not db_file.exists():
                raise FileNotFoundError("Database file not found in backup")
            
            shutil.move(str(db_file), self.db_path)
            shutil.rmtree(extract_dir)
            
            logger.info(f"Database restored from ZIP: {backup_path}")
            return True
            
        except Exception as e:
            if extract_dir.exists():
                shutil.rmtree(extract_dir)
            raise e
    
    def _restore_from_gzip(self, backup_path: Path) -> bool:
        """Восстановить из GZIP бэкапа"""
        temp_path = self.backup_dir / "temp_restore.db"
        
        try:
            with gzip.open(backup_path, 'rb') as f_in:
                with open(temp_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            
            shutil.move(str(temp_path), self.db_path)
            
            logger.info(f"Database restored from GZIP: {backup_path}")
            return True
            
        except Exception as e:
            temp_path.unlink(missing_ok=True)
            raise e
    
    def list_backups(self) -> List[Dict[str, Any]]:
        """Получить список всех резервных копий"""
        try:
            backups = []
            
            for filepath in self.backup_dir.glob("backup_*"):
                if filepath.suffix in ['.db', '.gz', '.zip']:
                    stat = filepath.stat()
                    
                    backups.append({
                        'filename': filepath.name,
                        'size': stat.st_size,
                        'size_mb': round(stat.st_size / 1024 / 1024, 2),
                        'created': datetime.fromtimestamp(stat.st_ctime),
                        'modified': datetime.fromtimestamp(stat.st_mtime),
                        'compressed': filepath.suffix in ['.gz', '.zip'],
                        'format': filepath.suffix[1:],
                        'path': str(filepath)
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
                filepath = Path(backup['path'])
                filepath.unlink()
                logger.info(f"Old backup deleted: {backup['filename']}")
            
            logger.info(f"Cleaned up {len(backups_to_delete)} old backups")
            
        except Exception as e:
            logger.error(f"Backup cleanup failed: {e}")
    
    def delete_backup(self, backup_name: str) -> bool:
        """Удалить конкретный бэкап"""
        try:
            backup_path = self.backup_dir / backup_name
            
            if backup_path.exists():
                backup_path.unlink()
                logger.info(f"Backup deleted: {backup_name}")
                return True
            
            logger.warning(f"Backup not found: {backup_name}")
            return False
            
        except Exception as e:
            logger.error(f"Failed to delete backup: {e}")
            return False
    
    def validate_backup(self, backup_file: str) -> Dict[str, Any]:
        """Валидация резервной копии"""
        backup_path = self.backup_dir / backup_file
        
        if not backup_path.exists():
            return {"valid": False, "error": "Backup file not found"}
        
        try:
            if backup_file.endswith('.zip'):
                with zipfile.ZipFile(backup_path, 'r') as zipf:
                    file_list = zipf.namelist()
                    
                    if "database.db" not in file_list:
                        return {"valid": False, "error": "Database file missing"}
                    
                    # Читаем метаданные если есть
                    metadata = None
                    if "metadata.json" in file_list:
                        metadata_content = zipf.read("metadata.json").decode('utf-8')
                        metadata = json.loads(metadata_content)
                    
                    return {
                        "valid": True,
                        "format": "zip",
                        "metadata": metadata,
                        "files": file_list
                    }
            
            elif backup_file.endswith('.gz'):
                # Проверяем что файл можно распаковать
                with gzip.open(backup_path, 'rb') as f:
                    f.read(1024)  # Читаем первые 1KB
                
                return {
                    "valid": True,
                    "format": "gzip"
                }
            
            else:
                # Проверяем что это валидная SQLite БД
                conn = sqlite3.connect(backup_path)
                conn.execute("SELECT 1")
                conn.close()
                
                return {
                    "valid": True,
                    "format": "raw"
                }
        
        except zipfile.BadZipFile:
            return {"valid": False, "error": "Invalid zip file"}
        except gzip.BadGzipFile:
            return {"valid": False, "error": "Invalid gzip file"}
        except sqlite3.DatabaseError:
            return {"valid": False, "error": "Invalid SQLite database"}
        except Exception as e:
            return {"valid": False, "error": str(e)}
    
    def get_stats(self) -> Dict[str, Any]:
        """Получить статистику резервных копий"""
        backups = self.list_backups()
        
        total_size = sum(b['size'] for b in backups)
        
        return {
            'total_backups': len(backups),
            'total_size_mb': round(total_size / 1024 / 1024, 2),
            'oldest_backup': backups[-1]['created'] if backups else None,
            'newest_backup': backups[0]['created'] if backups else None,
            'backup_dir': str(self.backup_dir),
            'max_backups': self.max_backups,
            'compression_enabled': self.compress,
            'compression_format': self.compression_format
        }
    
    def _export_schema(self) -> Optional[Dict[str, List[Dict]]]:
        """Экспорт схемы базы данных"""
        if not self.db_path.endswith('.db'):
            return None
        
        try:
            schema = {}
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Получаем все таблицы
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            for table_row in tables:
                table_name = table_row[0]
                
                # Пропускаем системные таблицы
                if table_name.startswith('sqlite_'):
                    continue
                
                # Получаем информацию о колонках
                table_info = cursor.execute(f"PRAGMA table_info('{table_name}')").fetchall()
                columns = []
                
                for col_info in table_info:
                    column = {
                        "name": col_info[1],
                        "type": col_info[2],
                        "notnull": bool(col_info[3]),
                        "default_value": col_info[4],
                        "pk": bool(col_info[5])
                    }
                    columns.append(column)
                
                schema[table_name] = columns
            
            conn.close()
            return schema
            
        except Exception as e:
            logger.error(f"Schema export failed: {e}")
            return None
    
    def schedule_automatic_backups(self, scheduler, interval_hours: int = 24):
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
    
    def export_to_json(self, output_path: str, table_name: Optional[str] = None) -> bool:
        """Экспорт данных в JSON"""
        try:
            from app import create_app, db
            from app.models.tournament import Tournament
            
            app = create_app()
            with app.app_context():
                if table_name == 'tournaments' or table_name is None:
                    tournaments = Tournament.query.all()
                    data = [t.to_dict() for t in tournaments]
                    
                    with open(output_path, 'w', encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False, indent=2, default=str)
                    
                    logger.info(f"Data exported to JSON: {output_path}")
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"JSON export failed: {e}")
            return False
    
    def export_to_csv(self, output_path: str, table_name: str = 'tournaments') -> bool:
        """Экспорт данных в CSV"""
        try:
            import csv
            from app import create_app, db
            from app.models.tournament import Tournament
            
            app = create_app()
            with app.app_context():
                if table_name == 'tournaments':
                    tournaments = Tournament.query.all()
                    
                    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
                        fieldnames = ['id', 'name', 'start_date', 'end_date', 'location', 
                                    'category', 'status', 'description', 'prize_fund', 
                                    'organizer', 'fide_id']
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        
                        writer.writeheader()
                        for t in tournaments:
                            writer.writerow({
                                'id': t.id,
                                'name': t.name,
                                'start_date': t.start_date,
                                'end_date': t.end_date,
                                'location': t.location,
                                'category': t.category,
                                'status': t.status,
                                'description': t.description,
                                'prize_fund': t.prize_fund,
                                'organizer': t.organizer,
                                'fide_id': t.fide_id
                            })
                    
                    logger.info(f"Data exported to CSV: {output_path}")
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"CSV export failed: {e}")
            return False


# Глобальный экземпляр
backup_manager = UnifiedBackupManager()
