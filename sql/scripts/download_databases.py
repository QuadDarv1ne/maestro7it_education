#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для автоматической загрузки баз данных SQLite
Автоматически скачивает и устанавливает популярные учебные базы данных
"""

import os
import requests
import sqlite3
from pathlib import Path
import zipfile
import io

class DatabaseDownloader:
    def __init__(self):
        self.databases = {
            'chinook': {
                'url': 'https://raw.githubusercontent.com/lerocha/chinook-database/master/ChinookDatabase/DataSources/Chinook_Sqlite.sqlite',
                'description': 'База данных музыкального магазина'
            },
            'northwind': {
                'url': 'https://github.com/jpwhite3/northwind-SQLite3/raw/master/dist/northwind.db',
                'description': 'База данных бизнеса/торговли'
            },
            'basketball': {
                'url': 'https://github.com/wyattowalsh/sports-analytics/raw/main/basketball/data/basketball.sqlite',
                'description': 'База данных спортивной аналитики'
            },
            'sakila': {
                'url': 'https://github.com/ivanceras/sakila/raw/master/sqlite-sakila-db/sakila.db',
                'description': 'База данных DVD-проката'
            }
        }
        self.data_dir = Path('data/databases')
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
    def download_database(self, db_name):
        """Скачивает указанную базу данных"""
        if db_name not in self.databases:
            print(f"❌ База данных '{db_name}' не найдена")
            return False
            
        db_info = self.databases[db_name]
        file_path = self.data_dir / f"{db_name}.db"
        
        try:
            print(f"📥 Скачивание {db_name}...")
            print(f"📄 {db_info['description']}")
            print(f"🔗 {db_info['url']}")
            
            response = requests.get(db_info['url'], timeout=30)
            response.raise_for_status()
            
            with open(file_path, 'wb') as f:
                f.write(response.content)
            
            # Проверяем целостность базы данных
            if self.validate_database(file_path):
                print(f"✅ {db_name} успешно загружена в {file_path}")
                self.show_database_info(file_path)
                return True
            else:
                print(f"❌ Ошибка: загруженный файл не является корректной базой данных SQLite")
                os.remove(file_path)
                return False
                
        except requests.RequestException as e:
            print(f"❌ Ошибка загрузки: {e}")
            return False
        except Exception as e:
            print(f"❌ Неожиданная ошибка: {e}")
            return False
    
    def validate_database(self, db_path):
        """Проверяет, что файл является корректной базой данных SQLite"""
        try:
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            conn.close()
            return len(tables) > 0
        except Exception:
            return False
    
    def show_database_info(self, db_path):
        """Показывает информацию о базе данных"""
        try:
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            
            # Получаем список таблиц
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            print(f"📊 Найдено таблиц: {len(tables)}")
            if len(tables) <= 10:
                for table in tables:
                    print(f"   • {table[0]}")
            else:
                for table in tables[:5]:
                    print(f"   • {table[0]}")
                print(f"   ... и ещё {len(tables) - 5} таблиц")
            
            conn.close()
        except Exception as e:
            print(f"⚠️  Не удалось получить информацию о базе данных: {e}")
    
    def download_all(self):
        """Скачивает все доступные базы данных"""
        print("🚀 Начинаем загрузку всех баз данных...\n")
        
        success_count = 0
        total_count = len(self.databases)
        
        for db_name in self.databases:
            print(f"\n{'='*50}")
            if self.download_database(db_name):
                success_count += 1
            print(f"{'='*50}")
        
        print(f"\n🏁 Завершено: {success_count}/{total_count} баз данных успешно загружено")
        print(f"📁 Файлы сохранены в: {self.data_dir}")

def main():
    print("📦 Автоматическая загрузка учебных баз данных SQLite")
    print("=" * 60)
    
    downloader = DatabaseDownloader()
    
    while True:
        print("\nВыберите действие:")
        print("1. Загрузить все базы данных")
        print("2. Загрузить конкретную базу данных")
        print("3. Показать список доступных баз данных")
        print("4. Выход")
        
        choice = input("\nВведите номер действия: ").strip()
        
        if choice == '1':
            downloader.download_all()
        elif choice == '2':
            print("\nДоступные базы данных:")
            for i, (name, info) in enumerate(downloader.databases.items(), 1):
                print(f"{i}. {name} - {info['description']}")
            
            try:
                db_choice = int(input("\nВыберите номер базы данных: ")) - 1
                db_names = list(downloader.databases.keys())
                if 0 <= db_choice < len(db_names):
                    downloader.download_database(db_names[db_choice])
                else:
                    print("❌ Неверный номер")
            except ValueError:
                print("❌ Введите корректный номер")
        elif choice == '3':
            print("\n📋 Доступные базы данных:")
            for name, info in downloader.databases.items():
                print(f"• {name}: {info['description']}")
                print(f"  URL: {info['url']}\n")
        elif choice == '4':
            print("👋 До свидания!")
            break
        else:
            print("❌ Неверный выбор")

if __name__ == "__main__":
    main()