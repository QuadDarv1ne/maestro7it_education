#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Database Management CLI
Утилита для управления базой данных
"""

import sys
import argparse
from app import create_app, db
from app.utils.db_init import DatabaseInitializer


def init_db():
    """Инициализировать базу данных"""
    print("=" * 60)
    print("DATABASE INITIALIZATION")
    print("=" * 60)
    
    app = create_app()
    with app.app_context():
        initializer = DatabaseInitializer(app, db)
        success = initializer.initialize_database()
        
        if success:
            print("\n✓ Database initialized successfully!")
            
            # Показываем информацию
            info = initializer.get_database_info()
            print(f"\nDatabase Info:")
            print(f"  Engine: {info.get('engine', 'Unknown')}")
            print(f"  Tables: {info.get('total_tables', 0)}")
            
            if 'tournament_count' in info:
                print(f"  Tournaments: {info['tournament_count']}")
            if 'user_count' in info:
                print(f"  Users: {info['user_count']}")
            
            return 0
        else:
            print("\n✗ Database initialization failed!")
            return 1


def check_db():
    """Проверить состояние базы данных"""
    print("=" * 60)
    print("DATABASE CHECK")
    print("=" * 60)
    
    app = create_app()
    with app.app_context():
        initializer = DatabaseInitializer(app, db)
        
        # Проверка файла БД
        db_exists = initializer.check_database_exists()
        print(f"\nDatabase file: {'✓ EXISTS' if db_exists else '✗ NOT FOUND'}")
        
        # Проверка таблиц
        tables_exist, missing_tables = initializer.check_tables_exist()
        if tables_exist:
            print(f"Tables: ✓ ALL EXIST ({len(initializer.required_tables)} tables)")
        else:
            print(f"Tables: ✗ MISSING {len(missing_tables)} tables")
            print(f"  Missing: {', '.join(missing_tables)}")
        
        # Проверка колонок tournament
        columns_exist, missing_columns = initializer.check_tournament_columns()
        if columns_exist:
            print("Tournament columns: ✓ ALL EXIST")
        else:
            print(f"Tournament columns: ✗ MISSING {len(missing_columns)} columns")
            print(f"  Missing: {', '.join(missing_columns)}")
        
        # Проверка целостности
        integrity_ok = initializer.verify_database_integrity()
        print(f"\nDatabase integrity: {'✓ OK' if integrity_ok else '✗ FAILED'}")
        
        # Информация о БД
        info = initializer.get_database_info()
        if info.get('status') == 'OK':
            print(f"\nDatabase Info:")
            print(f"  Engine: {info.get('engine', 'Unknown')}")
            print(f"  Total tables: {info.get('total_tables', 0)}")
            
            if 'tournament_count' in info:
                print(f"  Tournaments: {info['tournament_count']}")
            if 'user_count' in info:
                print(f"  Users: {info['user_count']}")
        
        return 0 if (db_exists and tables_exist and columns_exist and integrity_ok) else 1


def info_db():
    """Показать информацию о базе данных"""
    print("=" * 60)
    print("DATABASE INFORMATION")
    print("=" * 60)
    
    app = create_app()
    with app.app_context():
        initializer = DatabaseInitializer(app, db)
        info = initializer.get_database_info()
        
        if info.get('status') == 'OK':
            print(f"\nDatabase URI: {info.get('database_uri', 'Unknown')}")
            print(f"Engine: {info.get('engine', 'Unknown')}")
            print(f"Total tables: {info.get('total_tables', 0)}")
            
            print(f"\nTables:")
            for table in sorted(info.get('tables', [])):
                print(f"  - {table}")
            
            if 'tournament_count' in info:
                print(f"\nRecords:")
                print(f"  Tournaments: {info['tournament_count']}")
            if 'user_count' in info:
                print(f"  Users: {info['user_count']}")
            
            return 0
        else:
            print(f"\n✗ Error: {info.get('error', 'Unknown error')}")
            return 1


def reset_db():
    """Пересоздать базу данных (ОПАСНО!)"""
    print("=" * 60)
    print("DATABASE RESET - WARNING!")
    print("=" * 60)
    print("\nThis will DELETE ALL DATA and recreate the database!")
    
    confirm = input("\nType 'YES' to confirm: ")
    
    if confirm != 'YES':
        print("Operation cancelled.")
        return 0
    
    app = create_app()
    with app.app_context():
        try:
            print("\nDropping all tables...")
            db.drop_all()
            print("✓ All tables dropped")
            
            print("\nCreating all tables...")
            db.create_all()
            print("✓ All tables created")
            
            print("\n✓ Database reset successfully!")
            return 0
            
        except Exception as e:
            print(f"\n✗ Error resetting database: {e}")
            import traceback
            traceback.print_exc()
            return 1


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Database Management CLI for ChessCalendar-RU',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python manage_db.py init     # Initialize database
  python manage_db.py check    # Check database status
  python manage_db.py info     # Show database information
  python manage_db.py reset    # Reset database (WARNING: deletes all data!)
        """
    )
    
    parser.add_argument(
        'command',
        choices=['init', 'check', 'info', 'reset'],
        help='Command to execute'
    )
    
    args = parser.parse_args()
    
    # Выполняем команду
    if args.command == 'init':
        return init_db()
    elif args.command == 'check':
        return check_db()
    elif args.command == 'info':
        return info_db()
    elif args.command == 'reset':
        return reset_db()
    else:
        parser.print_help()
        return 1


if __name__ == '__main__':
    sys.exit(main())
