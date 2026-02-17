#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Database Initialization and Verification Module
Модуль автоматической инициализации и проверки базы данных
"""

import os
import logging
from sqlalchemy import inspect, text
from flask import Flask

logger = logging.getLogger(__name__)


class DatabaseInitializer:
    """Класс для инициализации и проверки базы данных"""
    
    def __init__(self, app: Flask, db):
        self.app = app
        self.db = db
        self.required_tables = [
            'user',
            'tournament',
            'tournament_rating',
            'favorite_tournament',
            'subscription',
            'notification',
            'user_preference',
            'user_interaction',
            'audit_log',
            'login_attempt',
            'two_factor_secret',
            'forum_thread',
            'forum_post',
            'report',
            'tournament_reminder',
            'tournament_subscription'
        ]
        
        # Новые колонки, добавленные в модель Tournament
        self.tournament_new_columns = {
            'view_count': 'INTEGER DEFAULT 0',
            'participants_count': 'INTEGER',
            'rating_type': 'VARCHAR(50)'
        }
    
    def check_database_exists(self) -> bool:
        """Проверить, существует ли файл базы данных"""
        db_path = self.app.config.get('SQLALCHEMY_DATABASE_URI', '')
        
        if db_path.startswith('sqlite:///'):
            # Извлекаем путь к файлу
            db_file = db_path.replace('sqlite:///', '')
            
            # Проверяем абсолютный или относительный путь
            if not os.path.isabs(db_file):
                db_file = os.path.join(os.getcwd(), db_file)
            
            exists = os.path.exists(db_file)
            logger.info(f"Database file check: {db_file} - {'EXISTS' if exists else 'NOT FOUND'}")
            return exists
        
        # Для других типов БД (PostgreSQL, MySQL) считаем, что БД существует
        return True
    
    def check_tables_exist(self) -> tuple[bool, list]:
        """
        Проверить, существуют ли все необходимые таблицы
        
        Returns:
            tuple: (все_таблицы_существуют, список_отсутствующих_таблиц)
        """
        try:
            inspector = inspect(self.db.engine)
            existing_tables = inspector.get_table_names()
            
            missing_tables = [
                table for table in self.required_tables 
                if table not in existing_tables
            ]
            
            if missing_tables:
                logger.warning(f"Missing tables: {', '.join(missing_tables)}")
                return False, missing_tables
            
            logger.info(f"All required tables exist ({len(existing_tables)} tables)")
            return True, []
            
        except Exception as e:
            logger.error(f"Error checking tables: {e}")
            return False, self.required_tables
    
    def check_tournament_columns(self) -> tuple[bool, list]:
        """
        Проверить, существуют ли новые колонки в таблице tournament
        
        Returns:
            tuple: (все_колонки_существуют, список_отсутствующих_колонок)
        """
        try:
            inspector = inspect(self.db.engine)
            
            # Проверяем, существует ли таблица tournament
            if 'tournament' not in inspector.get_table_names():
                return False, list(self.tournament_new_columns.keys())
            
            # Получаем список колонок
            columns = [col['name'] for col in inspector.get_columns('tournament')]
            
            # Проверяем наличие новых колонок
            missing_columns = [
                col for col in self.tournament_new_columns.keys()
                if col not in columns
            ]
            
            if missing_columns:
                logger.warning(f"Missing columns in tournament table: {', '.join(missing_columns)}")
                return False, missing_columns
            
            logger.info("All required columns exist in tournament table")
            return True, []
            
        except Exception as e:
            logger.error(f"Error checking tournament columns: {e}")
            return False, list(self.tournament_new_columns.keys())
    
    def create_all_tables(self):
        """Создать все таблицы"""
        try:
            logger.info("Creating all database tables...")
            self.db.create_all()
            logger.info("✓ All tables created successfully")
            return True
        except Exception as e:
            logger.error(f"Error creating tables: {e}")
            return False
    
    def add_missing_columns(self, missing_columns: list):
        """
        Добавить отсутствующие колонки в таблицу tournament
        
        Args:
            missing_columns: список отсутствующих колонок
        """
        try:
            for column in missing_columns:
                if column in self.tournament_new_columns:
                    column_def = self.tournament_new_columns[column]
                    sql = f"ALTER TABLE tournament ADD COLUMN {column} {column_def}"
                    
                    logger.info(f"Adding column: {column}")
                    self.db.session.execute(text(sql))
            
            self.db.session.commit()
            logger.info(f"✓ Added {len(missing_columns)} missing columns")
            return True
            
        except Exception as e:
            logger.error(f"Error adding columns: {e}")
            self.db.session.rollback()
            return False
    
    def initialize_database(self) -> bool:
        """
        Полная инициализация базы данных
        
        Returns:
            bool: успешность инициализации
        """
        try:
            logger.info("=" * 60)
            logger.info("DATABASE INITIALIZATION CHECK")
            logger.info("=" * 60)
            
            # Шаг 1: Проверка существования файла БД
            db_exists = self.check_database_exists()
            
            if not db_exists:
                logger.info("Database file not found. Creating new database...")
                self.create_all_tables()
            
            # Шаг 2: Проверка существования таблиц
            tables_exist, missing_tables = self.check_tables_exist()
            
            if not tables_exist:
                logger.info(f"Creating {len(missing_tables)} missing tables...")
                self.create_all_tables()
            
            # Шаг 3: Проверка колонок в таблице tournament
            columns_exist, missing_columns = self.check_tournament_columns()
            
            if not columns_exist:
                logger.info(f"Adding {len(missing_columns)} missing columns to tournament table...")
                self.add_missing_columns(missing_columns)
            
            # Финальная проверка
            tables_exist, _ = self.check_tables_exist()
            columns_exist, _ = self.check_tournament_columns()
            
            if tables_exist and columns_exist:
                logger.info("=" * 60)
                logger.info("✓ DATABASE INITIALIZATION COMPLETE")
                logger.info("=" * 60)
                return True
            else:
                logger.error("Database initialization failed")
                return False
                
        except Exception as e:
            logger.error(f"Critical error during database initialization: {e}")
            return False
    
    def get_database_info(self) -> dict:
        """
        Получить информацию о базе данных
        
        Returns:
            dict: информация о БД
        """
        try:
            inspector = inspect(self.db.engine)
            tables = inspector.get_table_names()
            
            info = {
                'database_uri': self.app.config.get('SQLALCHEMY_DATABASE_URI', 'Unknown'),
                'total_tables': len(tables),
                'tables': tables,
                'engine': str(self.db.engine.name),
                'status': 'OK'
            }
            
            # Получаем количество записей в основных таблицах
            try:
                if 'tournament' in tables:
                    result = self.db.session.execute(text("SELECT COUNT(*) FROM tournament"))
                    info['tournament_count'] = result.scalar()
                
                if 'user' in tables:
                    result = self.db.session.execute(text("SELECT COUNT(*) FROM user"))
                    info['user_count'] = result.scalar()
            except:
                pass
            
            return info
            
        except Exception as e:
            logger.error(f"Error getting database info: {e}")
            return {'status': 'ERROR', 'error': str(e)}
    
    def verify_database_integrity(self) -> bool:
        """
        Проверить целостность базы данных
        
        Returns:
            bool: база данных в порядке
        """
        try:
            # Проверяем, что можем выполнить простой запрос
            self.db.session.execute(text("SELECT 1"))
            
            # Проверяем все таблицы
            tables_exist, _ = self.check_tables_exist()
            
            # Проверяем колонки tournament
            columns_exist, _ = self.check_tournament_columns()
            
            return tables_exist and columns_exist
            
        except Exception as e:
            logger.error(f"Database integrity check failed: {e}")
            return False


def init_database(app: Flask, db) -> bool:
    """
    Инициализировать базу данных при запуске приложения
    
    Args:
        app: Flask приложение
        db: SQLAlchemy объект
    
    Returns:
        bool: успешность инициализации
    """
    with app.app_context():
        initializer = DatabaseInitializer(app, db)
        success = initializer.initialize_database()
        
        if success:
            # Выводим информацию о БД
            info = initializer.get_database_info()
            logger.info(f"Database: {info.get('engine', 'Unknown')}")
            logger.info(f"Tables: {info.get('total_tables', 0)}")
            
            if 'tournament_count' in info:
                logger.info(f"Tournaments: {info['tournament_count']}")
            if 'user_count' in info:
                logger.info(f"Users: {info['user_count']}")
        
        return success


def verify_database(app: Flask, db) -> bool:
    """
    Быстрая проверка базы данных
    
    Args:
        app: Flask приложение
        db: SQLAlchemy объект
    
    Returns:
        bool: база данных в порядке
    """
    with app.app_context():
        initializer = DatabaseInitializer(app, db)
        return initializer.verify_database_integrity()
