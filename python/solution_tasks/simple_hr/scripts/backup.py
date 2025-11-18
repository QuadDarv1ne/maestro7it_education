#!/usr/bin/env python
"""
Скрипт для создания резервных копий базы данных HR системы
"""

import sys
import os

# Добавляем путь к приложению в sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.utils.backup import backup_database, list_backups, cleanup_old_backups

def main():
    """Основная функция для создания резервной копии"""
    app = create_app()
    
    with app.app_context():
        print("Создание резервной копии базы данных...")
        try:
            result = backup_database()
            print(f"Резервная копия успешно создана:")
            print(f"- JSON файл: {result['json_file']}")
            print(f"- CSV директория: {result['csv_directory']}")
            print(f"- Временная метка: {result['timestamp']}")
            
            # Показываем список доступных бэкапов
            print("\nДоступные резервные копии:")
            backups = list_backups()
            for backup in backups[:5]:  # Показываем только последние 5
                print(f"- {backup['name']} ({backup['size']} bytes, {backup['modified']})")
            
            # Очищаем старые бэкапы (оставляем только за последние 30 дней)
            deleted_count = cleanup_old_backups()
            if deleted_count > 0:
                print(f"\nУдалено старых резервных копий: {deleted_count}")
                
            return 0
        except Exception as e:
            print(f"Ошибка при создании резервной копии: {e}")
            return 1

if __name__ == '__main__':
    sys.exit(main())