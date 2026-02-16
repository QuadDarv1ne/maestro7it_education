#!/usr/bin/env python
"""
Скрипт миграции данных из SQLite в PostgreSQL
Использование: python scripts/migrate_to_postgresql.py
"""

import os
import sys
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
    """Миграция данных между базами данных"""
    
    def __init__(self, source_url: str, target_url: str):
        """
        Инициализация мигратора
        
        Args:
            source_url: URL исходной БД (SQLite)
            target_url: URL целевой БД (PostgreSQL)
        """
        self.source_url = source_url
        self.target_url = target_url
        
        # Создаем движки
        self.source_engine = create_engine(source_url)
    