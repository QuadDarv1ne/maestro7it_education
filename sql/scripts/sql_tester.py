#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для проверки и тестирования SQL-запросов
Позволяет запускать запросы и проверять результаты
Автоматическое тестирование с ожидаемыми результатами
"""

import sqlite3
import os
from pathlib import Path
import json

class SQLTester:
    def __init__(self, db_path):
        self.db_path = Path(db_path)
        self.conn = None
        self.ensure_connection()
    
    def ensure_connection(self):
        """Устанавливает соединение с базой данных"""
        try:
            if self.conn is None or self.conn.closed:
                self.conn = sqlite3.connect(str(self.db_path))
                self.conn.row_factory = sqlite3.Row  # Для доступа к колонкам по именам
        except Exception as e:
            print(f"❌ Ошибка подключения к базе данных: {e}")
            raise
    
    def execute_query(self, query, params=None):
        """Выполняет SQL-запрос"""
        try:
            self.ensure_connection()
            cursor = self.conn.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            # Для SELECT запросов возвращаем результаты
            if query.strip().upper().startswith('SELECT'):
                results = cursor.fetchall()
                return results
            else:
                # Для INSERT/UPDATE/DELETE сохраняем изменения
                self.conn.commit()
                return cursor.rowcount
            
        except Exception as e:
            print(f"❌ Ошибка выполнения запроса: {e}")
            print(f"🔍 Запрос: {query}")
            return None
    
    def test_query_with_expected(self, query, expected_count=None, expected_columns=None):
        """Тестирует запрос с ожидаемыми результатами"""
        print(f"🔍 Тестирование запроса...")
        print(f"📋 Запрос: {query}")
        
        results = self.execute_query(query)
        
        if results is None:
            return False
        
        print(f"📊 Получено результатов: {len(results)}")
        
        # Проверяем количество результатов
        if expected_count is not None:
            if len(results) == expected_count:
                print(f"✅ Ожидаемое количество результатов: {expected_count}")
            else:
                print(f"❌ Ожидалось: {expected_count}, Получено: {len(results)}")
                return False
        
        # Проверяем колонки
        if expected_columns and len(results) > 0:
            actual_columns = list(results[0].keys())
            if set(actual_columns) == set(expected_columns):
                print(f"✅ Ожидаемые колонки найдены: {expected_columns}")
            else:
                print(f"❌ Несовпадение колонок")
                print(f"   Ожидалось: {expected_columns}")
                print(f"   Получено: {actual_columns}")
                return False
        
        # Показываем примеры результатов
        if results and len(results) > 0:
            print(f"📋 Примеры результатов (первые 3 строки):")
            for i, row in enumerate(results[:3]):
                print(f"   {i+1}. {dict(row)}")
        
        return True

def run_test_suite(db_name, test_file):
    """Запускает набор тестов из файла"""
    db_path = Path(f'data/databases/{db_name}.db')
    if not db_path.exists():
        print(f"❌ База данных {db_name}.db не найдена")
        return False
    
    tester = SQLTester(db_path)
    test_file_path = Path(test_file)
    
    if not test_file_path.exists():
        print(f"❌ Файл тестов {test_file} не найден")
        return False
    
    print(f"🧪 Запуск тестов для {db_name} из {test_file}")
    print("=" * 60)
    
    with open(test_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Парсим тесты (ожидаем формат: -- TEST: название | ожидаемое_количество)
    lines = content.split('\n')
    current_test = None
    current_query = []
    passed = 0
    failed = 0
    
    for line in lines:
        line = line.strip()
        
        if line.startswith('-- TEST:'):
            # Сохраняем предыдущий тест
            if current_test and current_query:
                query = '\n'.join(current_query)
                if run_single_test(tester, current_test, query):
                    passed += 1
                else:
                    failed += 1
            
            # Начинаем новый тест
            test_info = line[8:].strip()  # Убираем '-- TEST: '
            if '|' in test_info:
                name, expected = test_info.split('|')
                current_test = {
                    'name': name.strip(),
                    'expected_count': int(expected.strip())
                }
            else:
                current_test = {'name': test_info, 'expected_count': None}
            current_query = []
        
        elif line and current_test:
            current_query.append(line)
    
    # Запускаем последний тест
    if current_test and current_query:
        query = '\n'.join(current_query)
        if run_single_test(tester, current_test, query):
            passed += 1
        else:
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"🏁 Результаты: {passed} пройдено, {failed} провалено")
    return failed == 0

def run_single_test(tester, test_info, query):
    """Запускает один тест"""
    print(f"\n🔍 Тест: {test_info['name']}")
    print(f"📋 Запрос: {query[:100]}{'...' if len(query) > 100 else ''}")
    
    results = tester.execute_query(query)
    
    if results is None:
        print("❌ Тест провален: ошибка выполнения")
        return False
    
    if isinstance(results, list):
        actual_count = len(results)
        print(f"📊 Результатов: {actual_count}")
        
        if test_info['expected_count'] is not None:
            expected = test_info['expected_count']
            if actual_count == expected:
                print("✅ Тест пройден")
                return True
            else:
                print(f"❌ Тест провален: ожидалось {expected}, получено {actual_count}")
                return False
        else:
            print("✅ Тест пройден (количество не проверяется)")
            return True
    else:
        print(f"✅ Тест пройден (затронуто строк: {results})")
        return True

def main():
    print("🧪 SQL Тестер - проверка запросов")
    print("=" * 50)
    
    # Ищем доступные базы данных
    db_dir = Path('data/databases')
    if not db_dir.exists():
        print("📁 Каталог data/databases не найден")
        print("📥 Пожалуйста, сначала загрузите базы данных скриптом download_databases.py")
        return
    
    # Показываем доступные базы данных
    db_files = list(db_dir.glob('*.db'))
    if not db_files:
        print("❌ Нет доступных баз данных")
        print("📥 Пожалуйста, сначала загрузите базы данных")
        return
    
    print("📋 Доступные базы данных:")
    for i, db_file in enumerate(db_files, 1):
        print(f"{i}. {db_file.name}")
    
    try:
        choice = int(input("\nВыберите базу данных (номер): ")) - 1
        if 0 <= choice < len(db_files):
            selected_db = db_files[choice]
        else:
            print("❌ Неверный номер")
            return
    except ValueError:
        print("❌ Введите корректный номер")
        return
    
    # Создаем тестер
    tester = SQLTester(selected_db)
    
    print(f"\n✅ Подключено к: {selected_db.name}")
    print("📝 Введите SQL-запросы (введите 'выход' для завершения)")
    
    while True:
        print("\nВыберите действие:")
        print("1. Интерактивный режим")
        print("2. Запустить тесты для Chinook")
        print("3. Запустить тесты для NorthWind")
        print("4. Запустить тесты для Basketball")
        print("5. Выход")
        
        choice = input("\nВведите номер: ").strip()
        
        if choice == '1':
            # Интерактивный режим
            db_files = list(db_dir.glob('*.db'))
            if not db_files:
                print("❌ Нет доступных баз данных")
                continue
            
            print("\n📋 Доступные базы данных:")
            for i, db_file in enumerate(db_files, 1):
                print(f"{i}. {db_file.name}")
            
            try:
                db_choice = int(input("\nВыберите базу данных (номер): ")) - 1
                if 0 <= db_choice < len(db_files):
                    selected_db = db_files[db_choice]
                else:
                    print("❌ Неверный номер")
                    continue
            except ValueError:
                print("❌ Введите корректный номер")
                continue
            
            tester = SQLTester(selected_db)
            print(f"\n✅ Подключено к: {selected_db.name}")
            print("📝 Введите SQL-запросы (введите 'выход' для завершения)")
            
            while True:
                print("\n" + "-" * 40)
                query = input("SQL> ").strip()
                
                if query.lower() in ['выход', 'exit', 'quit']:
                    break
                
                if not query:
                    continue
                    
                results = tester.execute_query(query)
                
                if results is not None:
                    if isinstance(results, list):
                        print(f"📊 Результатов: {len(results)}")
                        if results:
                            columns = list(results[0].keys())
                            print(f"📋 Колонки: {columns}")
                            print("📋 Первые результаты:")
                            for i, row in enumerate(results[:5]):
                                print(f"   {i+1}. {dict(row)}")
                            if len(results) > 5:
                                print(f"   ... и ещё {len(results) - 5} строк")
                    else:
                        print(f"✅ Затронуто строк: {results}")
        
        elif choice == '2':
            run_test_suite('chinook', 'tests/chinook_tests.sql')
        elif choice == '3':
            run_test_suite('northwind', 'tests/northwind_tests.sql')
        elif choice == '4':
            run_test_suite('basketball', 'tests/basketball_tests.sql')
        elif choice == '5':
            print("👋 До свидания!")
            break
        else:
            print("❌ Неверный выбор")

if __name__ == "__main__":
    main()