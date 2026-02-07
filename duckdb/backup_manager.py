# -*- coding: utf-8 -*-
"""
Менеджер резервного копирования для базы данных товаров Ozon

Этот модуль предоставляет функции для создания и восстановления 
резервных копий базы данных DuckDB.
"""

import os
import shutil
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Optional
import duckdb
from config import DATABASE_NAME
from utils import get_logger, get_current_datetime_str


logger = get_logger(__name__)


class BackupManager:
    """Класс для управления резервными копиями базы данных."""
    
    def __init__(self, db_path: str = DATABASE_NAME, backup_dir: str = "backups"):
        """
        Инициализировать менеджер резервного копирования.
        
        Args:
            db_path: Путь к основной базе данных
            backup_dir: Директория для хранения резервных копий
        """
        self.db_path = db_path
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(exist_ok=True)
        
        logger.info(f"Менеджер резервного копирования инициализирован: {db_path}")
    
    def create_backup(self, backup_name: Optional[str] = None) -> str:
        """
        Создать резервную копию базы данных.
            
        Args:
            backup_name: Имя резервной копии (опционально)
                
        Returns:
            Путь к созданной резервной копии
        """
        if backup_name is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"backup_{timestamp}.zip"
            
        backup_path = self.backup_dir / backup_name
            
        try:
            # Создать временный файл для резервной копии
            temp_db_path = f"{self.db_path}.temp"
                    
            # Ждать немного времени, чтобы освободить файл базы данных
            import time
            time.sleep(1)
                    
            # Просто скопировать файл базы данных напрямую
            # Это самый надежный способ сделать резервную копию DuckDB
            shutil.copy2(self.db_path, temp_db_path)
                    
            # Заархивировать базу данных
            with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(temp_db_path, os.path.basename(self.db_path))
                    
            # Удалить временный файл
            os.remove(temp_db_path)
            
            logger.info(f"Резервная копия создана: {backup_path}")
            return str(backup_path)
            
        except Exception as e:
            logger.error(f"Ошибка при создании резервной копии: {e}")
            raise
    
    def restore_from_backup(self, backup_path: str):
        """
        Восстановить базу данных из резервной копии.
        
        Args:
            backup_path: Путь к резервной копии
        """
        try:
            # Распаковать архив
            extract_dir = Path(backup_path).parent / "temp_extract"
            extract_dir.mkdir(exist_ok=True)
            
            with zipfile.ZipFile(backup_path, 'r') as zipf:
                zipf.extractall(extract_dir)
            
            # Найти файл базы данных в распакованной директории
            extracted_db = None
            for file_path in extract_dir.rglob("*.duckdb"):
                extracted_db = file_path
                break
            
            if extracted_db is None:
                raise FileNotFoundError("Файл базы данных не найден в архиве")
            
            # Заменить текущую базу данных
            shutil.copy2(extracted_db, self.db_path)
            
            # Удалить временные файлы
            shutil.rmtree(extract_dir)
            
            logger.info(f"База данных восстановлена из: {backup_path}")
            
        except Exception as e:
            logger.error(f"Ошибка при восстановлении из резервной копии: {e}")
            raise
    
    def list_backups(self) -> list:
        """
        Получить список доступных резервных копий.
        
        Returns:
            Список файлов резервных копий
        """
        backups = []
        for file_path in self.backup_dir.glob("*.zip"):
            stat = file_path.stat()
            backups.append({
                'name': file_path.name,
                'size': stat.st_size,
                'created': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            })
        
        # Сортировать по времени создания (новые первыми)
        backups.sort(key=lambda x: x['created'], reverse=True)
        logger.info(f"Найдено {len(backups)} резервных копий")
        return backups
    
    def cleanup_old_backups(self, keep_count: int = 5):
        """
        Удалить старые резервные копии, оставив только последние N.
        
        Args:
            keep_count: Количество резервных копий для сохранения
        """
        backups = self.list_backups()
        if len(backups) <= keep_count:
            logger.info(f"Нет необходимости очищать резервные копии. Всего: {len(backups)}, сохранить: {keep_count}")
            return
        
        backups_to_delete = backups[keep_count:]
        for backup_info in backups_to_delete:
            backup_path = self.backup_dir / backup_info['name']
            backup_path.unlink()
            logger.info(f"Удалена старая резервная копия: {backup_info['name']}")
        
        logger.info(f"Очистка завершена. Удалено: {len(backups_to_delete)} резервных копий")


def main():
    """Основная функция для демонстрации возможностей менеджера резервного копирования."""
    from config import LOG_LEVEL
    from utils import setup_logging
    
    # Настроить логирование
    setup_logging(LOG_LEVEL)
    
    logger.info("Запуск менеджера резервного копирования")
    
    try:
        backup_manager = BackupManager()
        
        print("📊 ДОСТУПНЫЕ РЕЗЕРВНЫЕ КОПИИ")
        print("="*50)
        backups = backup_manager.list_backups()
        if backups:
            for i, backup in enumerate(backups, 1):
                print(f"{i}. {backup['name']} ({backup['size']} байт, {backup['created']})")
        else:
            print("Нет доступных резервных копий")
        
        print(f"\n📦 СОЗДАНИЕ НОВОЙ РЕЗЕРВНОЙ КОПИИ")
        print("="*50)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"manual_backup_{timestamp}.zip"
        backup_path = backup_manager.create_backup(backup_name)
        print(f"✅ Резервная копия создана: {backup_path}")
        
        print(f"\n🧹 ОЧИСТКА СТАРЫХ РЕЗЕРВНЫХ КОПИЙ")
        print("="*50)
        backup_manager.cleanup_old_backups(keep_count=3)
        print("✅ Очистка завершена")
        
        print(f"\n✨ Работа менеджера резервного копирования завершена!")
        
    except Exception as e:
        logger.error(f"Ошибка в процессе резервного копирования: {e}")
        print(f"❌ Ошибка: {e}")


if __name__ == "__main__":
    main()