import os
import shutil
import sqlite3
import json
from datetime import datetime
from pathlib import Path
import logging
import zipfile
from typing import Optional


class DatabaseBackupManager:
    """Класс для управления резервным копированием базы данных"""
    
    def __init__(self, db_path: str, backup_dir: str = "backups"):
        self.db_path = db_path
        self.backup_dir = Path(backup_dir)
        self.logger = logging.getLogger(__name__)
        
        # Создаем директорию для бэкапов если не существует
        self.backup_dir.mkdir(exist_ok=True)
    
    def create_backup(self, backup_name: Optional[str] = None) -> str:
        """
        Создать резервную копию базы данных
        
        Args:
            backup_name: Имя бэкапа (если не указано, генерируется автоматически)
            
        Returns:
            Путь к созданному бэкапу
        """
        try:
            if not backup_name:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_name = f"chess_calendar_backup_{timestamp}.db"
            
            backup_path = self.backup_dir / backup_name
            
            # Создаем резервную копию
            shutil.copy2(self.db_path, backup_path)
            
            self.logger.info(f"Бэкап базы данных создан: {backup_path}")
            return str(backup_path)
        
        except Exception as e:
            self.logger.error(f"Ошибка при создании бэкапа: {e}")
            raise
    
    def create_compressed_backup(self, backup_name: Optional[str] = None) -> str:
        """
        Создать сжатую резервную копию базы данных
        
        Args:
            backup_name: Имя бэкапа (если не указано, генерируется автоматически)
            
        Returns:
            Путь к созданному сжатому бэкапу
        """
        try:
            if not backup_name:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_name = f"chess_calendar_backup_{timestamp}.zip"
            
            backup_path = self.backup_dir / backup_name
            
            # Создаем ZIP архив с бэкапом
            with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(self.db_path, os.path.basename(self.db_path))
            
            self.logger.info(f"Сжатый бэкап базы данных создан: {backup_path}")
            return str(backup_path)
        
        except Exception as e:
            self.logger.error(f"Ошибка при создании сжатого бэкапа: {e}")
            raise
    
    def restore_backup(self, backup_path: str) -> bool:
        """
        Восстановить базу данных из бэкапа
        
        Args:
            backup_path: Путь к файлу бэкапа
            
        Returns:
            Успешность восстановления
        """
        try:
            backup_file = Path(backup_path)
            
            if not backup_file.exists():
                self.logger.error(f"Файл бэкапа не найден: {backup_path}")
                return False
            
            # Если это ZIP файл, распаковываем его
            if backup_file.suffix.lower() == '.zip':
                with zipfile.ZipFile(backup_file, 'r') as zipf:
                    # Извлекаем файл базы данных
                    for member in zipf.namelist():
                        if member.endswith('.db'):
                            zipf.extract(member, self.backup_dir)
                            extracted_db = self.backup_dir / member
                            # Копируем извлеченную базу в нужное место
                            shutil.copy2(extracted_db, self.db_path)
                            # Удаляем временный файл
                            extracted_db.unlink()
                            break
            else:
                # Просто копируем файл базы данных
                shutil.copy2(backup_file, self.db_path)
            
            self.logger.info(f"База данных восстановлена из: {backup_path}")
            return True
        
        except Exception as e:
            self.logger.error(f"Ошибка при восстановлении бэкапа: {e}")
            return False
    
    def list_backups(self) -> list:
        """
        Получить список доступных бэкапов
        
        Returns:
            Список файлов бэкапов
        """
        try:
            backups = []
            for file in self.backup_dir.glob("*"):
                if file.is_file() and (file.suffix.lower() == '.db' or file.suffix.lower() == '.zip'):
                    backups.append({
                        'name': file.name,
                        'size': file.stat().st_size,
                        'modified': datetime.fromtimestamp(file.stat().st_mtime),
                        'path': str(file)
                    })
            
            # Сортируем по времени модификации (новые первыми)
            backups.sort(key=lambda x: x['modified'], reverse=True)
            return backups
        
        except Exception as e:
            self.logger.error(f"Ошибка при получении списка бэкапов: {e}")
            return []
    
    def cleanup_old_backups(self, keep_count: int = 5) -> int:
        """
        Удалить старые бэкапы, оставив только последние n
        
        Args:
            keep_count: Количество бэкапов для сохранения
            
        Returns:
            Количество удаленных бэкапов
        """
        try:
            backups = self.list_backups()
            
            if len(backups) <= keep_count:
                return 0
            
            backups_to_delete = backups[keep_count:]
            deleted_count = 0
            
            for backup in backups_to_delete:
                try:
                    Path(backup['path']).unlink()
                    deleted_count += 1
                    self.logger.info(f"Удален старый бэкап: {backup['name']}")
                except Exception as e:
                    self.logger.error(f"Ошибка при удалении бэкапа {backup['name']}: {e}")
            
            return deleted_count
        
        except Exception as e:
            self.logger.error(f"Ошибка при очистке старых бэкапов: {e}")
            return 0


class DataExportManager:
    """Класс для экспорта данных в различные форматы"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
    
    def export_tournaments_to_json(self, output_path: str) -> bool:
        """
        Экспортировать турниры в JSON формат
        
        Args:
            output_path: Путь для сохранения JSON файла
            
        Returns:
            Успешность экспорта
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Получаем все турниры
            cursor.execute("""
                SELECT id, name, start_date, end_date, location, 
                       category, status, fide_id, source_url, 
                       created_at, updated_at
                FROM tournament
                ORDER BY start_date
            """)
            
            columns = [description[0] for description in cursor.description]
            rows = cursor.fetchall()
            
            # Преобразуем в список словарей
            tournaments = []
            for row in rows:
                tournament = {}
                for i, column in enumerate(columns):
                    tournament[column] = row[i]
                tournaments.append(tournament)
            
            # Сохраняем в JSON
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(tournaments, f, ensure_ascii=False, indent=2, default=str)
            
            conn.close()
            self.logger.info(f"Турниры экспортированы в JSON: {output_path}")
            return True
        
        except Exception as e:
            self.logger.error(f"Ошибка при экспорте турниров в JSON: {e}")
            return False
    
    def export_tournaments_to_csv(self, output_path: str) -> bool:
        """
        Экспортировать турниры в CSV формат
        
        Args:
            output_path: Путь для сохранения CSV файла
            
        Returns:
            Успешность экспорта
        """
        try:
            import csv
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Получаем все турниры
            cursor.execute("""
                SELECT id, name, start_date, end_date, location, 
                       category, status, fide_id, source_url, 
                       created_at, updated_at
                FROM tournament
                ORDER BY start_date
            """)
            
            columns = [description[0] for description in cursor.description]
            rows = cursor.fetchall()
            
            # Сохраняем в CSV
            with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(columns)  # Заголовки
                writer.writerows(rows)    # Данные
            
            conn.close()
            self.logger.info(f"Турниры экспортированы в CSV: {output_path}")
            return True
        
        except Exception as e:
            self.logger.error(f"Ошибка при экспорте турниров в CSV: {e}")
            return False


# Глобальный экземпляр менеджера бэкапов
backup_manager = DatabaseBackupManager("chess_calendar.db")


def schedule_regular_backups():
    """Настроить регулярное создание бэкапов"""
    import schedule
    import time
    import threading
    
    def backup_job():
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"auto_backup_{timestamp}.zip"
            backup_manager.create_compressed_backup(backup_name)
            
            # Оставляем только последние 7 бэкапов
            backup_manager.cleanup_old_backups(keep_count=7)
            
        except Exception as e:
            logging.error(f"Ошибка при автоматическом создании бэкапа: {e}")
    
    # Создаем бэкап каждый день в 02:00
    schedule.every().day.at("02:00").do(backup_job)
    
    def run_scheduler():
        while True:
            schedule.run_pending()
            time.sleep(60)  # Проверяем каждую минуту
    
    # Запускаем планировщик в отдельном потоке
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()


# Инициализация автоматических бэкапов
try:
    schedule_regular_backups()
except Exception as e:
    logging.error(f"Ошибка при инициализации автоматических бэкапов: {e}")