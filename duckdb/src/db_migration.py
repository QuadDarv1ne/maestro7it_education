# -*- coding: utf-8 -*-
"""
Модуль миграции базы данных для проекта товаров Ozon

Этот модуль предоставляет инструменты для управления версиями схемы базы данных 
и выполнения миграций между версиями.
"""

import duckdb
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Callable
from config import DATABASE_NAME
from utils import get_logger


logger = get_logger(__name__)


class DatabaseMigration:
    """Класс для управления миграциями базы данных."""
    
    def __init__(self, db_path: str = DATABASE_NAME, migrations_dir: str = "migrations"):
        """
        Инициализировать систему миграций базы данных.
        
        Args:
            db_path: Путь к базе данных
            migrations_dir: Директория для файлов миграций
        """
        self.db_path = db_path
        self.migrations_dir = Path(migrations_dir)
        self.migrations_dir.mkdir(exist_ok=True)
        
        # Подключиться к базе данных
        self.con = duckdb.connect(db_path)
        
        # Создать таблицу для отслеживания миграций
        self._create_migration_table()
        
        logger.info(f"Система миграций инициализирована для базы: {db_path}")
    
    def __del__(self):
        """Закрыть соединение при удалении объекта."""
        if hasattr(self, 'con'):
            self.con.close()
    
    def _create_migration_table(self):
        """Создать таблицу для отслеживания выполненных миграций."""
        try:
            self.con.execute("""
                CREATE TABLE IF NOT EXISTS schema_migrations (
                    id INTEGER PRIMARY KEY,
                    version VARCHAR UNIQUE,
                    name VARCHAR,
                    description VARCHAR,
                    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    checksum VARCHAR
                );
            """)
            logger.info("Таблица миграций создана или уже существует")
        except Exception as e:
            logger.error(f"Ошибка при создании таблицы миграций: {e}")
            raise
    
    def create_migration(self, name: str, description: str = "", 
                         up_sql: str = "", down_sql: str = "") -> str:
        """
        Создать новый файл миграции.
        
        Args:
            name: Имя миграции
            description: Описание миграции
            up_sql: SQL-код для применения миграции
            down_sql: SQL-код для отката миграции
            
        Returns:
            Путь к созданному файлу миграции
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{name.replace(' ', '_').lower()}.sql"
        filepath = self.migrations_dir / filename
        
        # Создать содержимое файла миграции
        migration_content = f"""-- Миграция: {name}
-- Описание: {description}
-- Дата создания: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

-- UP: Применение миграции
-- Начало UP
{up_sql or '-- Здесь должен быть SQL-код для применения миграции'}
-- Конец UP

-- DOWN: Откат миграции
-- Начало DOWN
{down_sql or '-- Здесь должен быть SQL-код для отката миграции'}
-- Конец DOWN
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(migration_content)
        
        logger.info(f"Файл миграции создан: {filepath}")
        return str(filepath)
    
    def get_applied_migrations(self) -> List[Dict]:
        """
        Получить список примененных миграций.
        
        Returns:
            Список примененных миграций
        """
        try:
            result = self.con.execute(
                "SELECT version, name, description, applied_at FROM schema_migrations ORDER BY applied_at;"
            ).fetchall()
            
            migrations = []
            for row in result:
                migrations.append({
                    'version': row[0],
                    'name': row[1],
                    'description': row[2],
                    'applied_at': row[3]
                })
            
            logger.info(f"Найдено {len(migrations)} примененных миграций")
            return migrations
        except Exception as e:
            logger.error(f"Ошибка при получении списка миграций: {e}")
            return []
    
    def get_pending_migrations(self) -> List[Dict]:
        """
        Получить список ожидающих применения миграций.
        
        Returns:
            Список ожидающих миграций
        """
        applied_versions = {m['version'] for m in self.get_applied_migrations()}
        
        pending_migrations = []
        for migration_file in self.migrations_dir.glob("*.sql"):
            # Извлечь версию из имени файла (первые 14 символов YYYYMMDDHHMMSS)
            try:
                version = migration_file.name.split('_')[0]
                if version not in applied_versions:
                    pending_migrations.append({
                        'version': version,
                        'filename': migration_file.name,
                        'filepath': str(migration_file)
                    })
            except Exception:
                continue  # Пропустить файлы с неправильным форматом
        
        # Сортировать по версии (времени создания)
        pending_migrations.sort(key=lambda x: x['version'])
        
        logger.info(f"Найдено {len(pending_migrations)} ожидающих миграций")
        return pending_migrations
    
    def apply_migration(self, migration_path: str) -> bool:
        """
        Применить одну миграцию.
        
        Args:
            migration_path: Путь к файлу миграции
            
        Returns:
            Успешность применения
        """
        try:
            with open(migration_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Извлечь секцию UP из файла миграции
            up_start = content.find("-- Начало UP")
            up_end = content.find("-- Конец UP")
            
            if up_start == -1 or up_end == -1:
                logger.error(f"Не найдена секция UP в миграции: {migration_path}")
                return False
            
            up_sql = content[up_start + 12:up_end].strip()
            
            # Выполнить SQL команды из секции UP
            if up_sql:
                # Разделить команды по точке с запятой
                sql_commands = [cmd.strip() for cmd in up_sql.split(';') if cmd.strip()]
                
                for command in sql_commands:
                    if command:  # Пропустить пустые команды
                        self.con.execute(command)
            
            # Извлечь имя и описание миграции из начала файла
            lines = content.split('\n')
            name = "Unknown"
            description = ""
            
            for line in lines:
                if line.startswith('-- Миграция:'):
                    name = line.replace('-- Миграция:', '').strip()
                elif line.startswith('-- Описание:'):
                    description = line.replace('-- Описание:', '').strip()
                elif line.startswith('--'):  # Комментарии закончились
                    continue
                else:
                    break
            
            # Извлечь версию из имени файла
            version = Path(migration_path).name.split('_')[0]
            
            # Записать информацию о примененной миграции
            self.con.execute(
                "INSERT INTO schema_migrations (version, name, description) VALUES (?, ?, ?);",
                [version, name, description]
            )
            
            logger.info(f"Миграция применена: {name} (версия {version})")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка при применении миграции {migration_path}: {e}")
            return False
    
    def apply_all_migrations(self) -> bool:
        """
        Применить все ожидающие миграции.
        
        Returns:
            Успешность выполнения
        """
        pending_migrations = self.get_pending_migrations()
        
        if not pending_migrations:
            logger.info("Нет ожидающих миграций для применения")
            return True
        
        logger.info(f"Применение {len(pending_migrations)} миграций...")
        
        success_count = 0
        for migration in pending_migrations:
            logger.info(f"Применение миграции: {migration['filename']}")
            if self.apply_migration(migration['filepath']):
                success_count += 1
            else:
                logger.error(f"Не удалось применить миграцию: {migration['filename']}")
                return False  # Остановить при первой ошибке
        
        logger.info(f"Успешно применено {success_count} из {len(pending_migrations)} миграций")
        return True
    
    def rollback_migration(self, version: str) -> bool:
        """
        Откатить миграцию по версии.
        
        Args:
            version: Версия миграции для отката
            
        Returns:
            Успешность отката
        """
        try:
            # Найти файл миграции по версии
            migration_file = None
            for file in self.migrations_dir.glob("*.sql"):
                if file.name.startswith(version):
                    migration_file = file
                    break
            
            if not migration_file:
                logger.error(f"Файл миграции для версии {version} не найден")
                return False
            
            with open(migration_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Извлечь секцию DOWN из файла миграции
            down_start = content.find("-- Начало DOWN")
            down_end = content.find("-- Конец DOWN")
            
            if down_start == -1 or down_end == -1:
                logger.error(f"Не найдена секция DOWN в миграции: {migration_file}")
                return False
            
            down_sql = content[down_start + 13:down_end].strip()
            
            # Выполнить SQL команды из секции DOWN
            if down_sql:
                # Разделить команды по точке с запятой
                sql_commands = [cmd.strip() for cmd in down_sql.split(';') if cmd.strip()]
                
                for command in sql_commands:
                    if command:  # Пропустить пустые команды
                        self.con.execute(command)
            
            # Удалить запись о миграции
            self.con.execute(
                "DELETE FROM schema_migrations WHERE version = ?;",
                [version]
            )
            
            logger.info(f"Миграция откачена: {version}")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка при откате миграции {version}: {e}")
            return False
    
    def get_current_version(self) -> Optional[str]:
        """
        Получить текущую версию схемы базы данных.
        
        Returns:
            Текущая версия или None
        """
        try:
            result = self.con.execute(
                "SELECT version FROM schema_migrations ORDER BY applied_at DESC LIMIT 1;"
            ).fetchall()
            
            if result:
                return result[0][0]
            return None
        except Exception as e:
            logger.error(f"Ошибка при получении текущей версии: {e}")
            return None
    
    def status(self) -> Dict:
        """
        Получить статус миграций.
        
        Returns:
            Словарь со статусом миграций
        """
        applied = self.get_applied_migrations()
        pending = self.get_pending_migrations()
        current_version = self.get_current_version()
        
        status_info = {
            'current_version': current_version,
            'applied_migrations': len(applied),
            'pending_migrations': len(pending),
            'applied_details': applied,
            'pending_details': pending
        }
        
        return status_info


def main():
    """Основная функция для демонстрации возможностей системы миграций."""
    from config import LOG_LEVEL
    from utils import setup_logging
    
    # Настроить логирование
    setup_logging(LOG_LEVEL)
    
    logger.info("Запуск системы миграций базы данных")
    
    try:
        migrator = DatabaseMigration()
        
        print("🔄 СИСТЕМА МИГРАЦИЙ БАЗЫ ДАННЫХ")
        print("="*60)
        
        # Показать статус миграций
        print("1. Статус миграций:")
        status = migrator.status()
        print(f"   Текущая версия: {status['current_version'] or 'Нет'}")
        print(f"   Применено миграций: {status['applied_migrations']}")
        print(f"   Ожидающих миграций: {status['pending_migrations']}")
        
        # Показать примененные миграции
        if status['applied_details']:
            print("   Примененные миграции:")
            for migration in status['applied_details']:
                print(f"     - {migration['version']}: {migration['name']}")
        
        # Показать ожидающие миграции
        if status['pending_details']:
            print("   Ожидающие миграции:")
            for migration in status['pending_details']:
                print(f"     - {migration['version']}: {migration['filename']}")
        
        print(f"\n✨ Система миграций базы данных работает!")
        
    except Exception as e:
        logger.error(f"Ошибка в системе миграций: {e}")
        print(f"❌ Ошибка: {e}")


if __name__ == "__main__":
    main()