"""
Database Configuration
Поддержка SQLite и PostgreSQL с автоматическим определением
"""

import os
from urllib.parse import urlparse


class DatabaseConfig:
    """Конфигурация базы данных с поддержкой SQLite и PostgreSQL"""
    
    @staticmethod
    def get_database_url():
        """
        Получить URL базы данных из переменных окружения
        
        Поддерживаемые форматы:
        - SQLite: sqlite:///path/to/database.db
        - PostgreSQL: postgresql://user:password@host:port/database
        - PostgreSQL (альтернативный): postgres://user:password@host:port/database
        """
        database_url = os.environ.get('DATABASE_URL')
        
        if not database_url:
            # По умолчанию используем SQLite
            return 'sqlite:///chess_calendar.db'
        
        # Heroku использует postgres://, но SQLAlchemy требует postgresql://
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        
        return database_url
    
    @staticmethod
    def get_engine_options():
        """
        Получить опции для SQLAlchemy engine в зависимости от типа БД
        
        Returns:
            dict: Опции для create_engine
        """
        database_url = DatabaseConfig.get_database_url()
        parsed = urlparse(database_url)
        
        if parsed.scheme == 'sqlite':
            # Опции для SQLite
            return {
                'pool_pre_ping': True,
                'pool_recycle': 3600,
                'connect_args': {
                    'check_same_thread': False,
                    'timeout': 30
                }
            }
        
        elif parsed.scheme in ('postgresql', 'postgres'):
            # Опции для PostgreSQL
            return {
                'pool_size': int(os.environ.get('DB_POOL_SIZE', 20)),
                'max_overflow': int(os.environ.get('DB_MAX_OVERFLOW', 40)),
                'pool_timeout': int(os.environ.get('DB_POOL_TIMEOUT', 30)),
                'pool_recycle': int(os.environ.get('DB_POOL_RECYCLE', 3600)),
                'pool_pre_ping': True,
                'connect_args': {
                    'connect_timeout': 10,
                    'options': '-c timezone=Europe/Moscow'
                }
            }
        
        else:
            # Базовые опции для других БД
            return {
                'pool_pre_ping': True,
                'pool_recycle': 3600
            }
    
    @staticmethod
    def is_postgresql():
        """Проверка, используется ли PostgreSQL"""
        database_url = DatabaseConfig.get_database_url()
        parsed = urlparse(database_url)
        return parsed.scheme in ('postgresql', 'postgres')
    
    @staticmethod
    def is_sqlite():
        """Проверка, используется ли SQLite"""
        database_url = DatabaseConfig.get_database_url()
        parsed = urlparse(database_url)
        return parsed.scheme == 'sqlite'
    
    @staticmethod
    def get_database_info():
        """Получить информацию о текущей БД"""
        database_url = DatabaseConfig.get_database_url()
        parsed = urlparse(database_url)
        
        return {
            'type': parsed.scheme,
            'host': parsed.hostname,
            'port': parsed.port,
            'database': parsed.path.lstrip('/') if parsed.path else None,
            'username': parsed.username,
            'is_postgresql': DatabaseConfig.is_postgresql(),
            'is_sqlite': DatabaseConfig.is_sqlite()
        }


# Экспорт для удобного использования
DATABASE_URL = DatabaseConfig.get_database_url()
ENGINE_OPTIONS = DatabaseConfig.get_engine_options()
IS_POSTGRESQL = DatabaseConfig.is_postgresql()
IS_SQLITE = DatabaseConfig.is_sqlite()
