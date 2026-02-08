#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для валидации решений SQL-задач
Сравнивает пользовательские решения с эталонными ответами
"""

import sqlite3
import os
from pathlib import Path
import difflib
import json

class SolutionValidator:
    def __init__(self, db_path):
        self.db_path = Path(db_path)
        self.conn = None
        self.ensure_connection()
    
    def ensure_connection(self):
        """Устанавливает соединение с базой данных"""
        try:
            if self.conn is None:
                self.conn = sqlite3.connect(str(self.db_path))
                self.conn.row_factory = sqlite3.Row
        except Exception as e:
            print(f"❌ Ошибка подключения к базе данных: {e}")
            raise
    
    def execute_query(self, query):
        """Выполняет SQL-запрос и возвращает результаты"""
        try:
            self.ensure_connection()
            cursor = self.conn.cursor()
            cursor.execute(query)
            
            if query.strip().upper().startswith('SELECT'):
                results = cursor.fetchall()
                return [dict(row) for row in results]
            else:
                self.conn.commit()
                return cursor.rowcount
        except Exception as e:
            return f"ERROR: {str(e)}"
    
    def compare_results(self, user_result, expected_result, tolerance=0.01):
        """Сравнивает результаты запросов"""
        if isinstance(user_result, str) and user_result.startswith("ERROR"):
            return False, f"Ошибка выполнения: {user_result}"
        
        if isinstance(expected_result, str) and expected_result.startswith("ERROR"):
            return False, f"Ошибка в эталонном решении: {expected_result}"
        
        # Для числовых результатов
        if isinstance(user_result, (int, float)) and isinstance(expected_result, (int, float)):
            if abs(user_result - expected_result) <= tolerance:
                return True, "✅ Результаты совпадают"
            else:
                return False, f"❌ Различие в результатах: ожидаем {expected_result}, получено {user_result}"
        
        # Для списков результатов
        if isinstance(user_result, list) and isinstance(expected_result, list):
            if len(user_result) != len(expected_result):
                return False, f"❌ Разное количество строк: ожидаем {len(expected_result)}, получено {len(user_result)}"
            
            # Сравниваем структуру первой строки
            if user_result and expected_result:
                user_keys = set(user_result[0].keys())
                expected_keys = set(expected_result[0].keys())
                
                if user_keys != expected_keys:
                    missing = expected_keys - user_keys
                    extra = user_keys - expected_keys
                    msg = "❌ Несовпадение структуры:"
                    if missing:
                        msg += f" отсутствуют колонки {missing}"
                    if extra:
                        msg += f" лишние колонки {extra}"
                    return False, msg
            
            return True, f"✅ Получено {len(user_result)} строк"
        
        return False, "❌ Невозможно сравнить результаты"
    
    def validate_solution(self, task_name, user_query, expected_query):
        """Валидирует решение задачи"""
        print(f"\n🔍 Проверка задачи: {task_name}")
        print(f"📝 Ваш запрос: {user_query}")
        
        # Выполняем оба запроса
        user_result = self.execute_query(user_query)
        expected_result = self.execute_query(expected_query)
        
        # Сравниваем результаты
        is_correct, message = self.compare_results(user_result, expected_result)
        
        if is_correct:
            print("✅ Решение верное!")
            if isinstance(user_result, list) and user_result:
                print(f"📊 Пример результата: {user_result[0]}")
        else:
            print(message)
            print(f"📝 Эталонный запрос: {expected_query}")
            
            # Показываем эталонные результаты
            if not isinstance(expected_result, str):
                print(f"📊 Ожидаемый результат: {expected_result[:3] if isinstance(expected_result, list) else expected_result}")
        
        return is_correct

def load_solutions(solution_file):
    """Загружает эталонные решения из файла"""
    solutions = {}
    
    with open(solution_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    current_task = None
    current_solution = []
    
    for line in lines:
        line = line.strip()
        
        if line.startswith('-- SOLUTION:'):
            if current_task and current_solution:
                solutions[current_task] = '\n'.join(current_solution)
            
            current_task = line[12:].strip()  # Убираем '-- SOLUTION: '
            current_solution = []
        elif line and current_task:
            current_solution.append(line)
    
    # Добавляем последнее решение
    if current_task and current_solution:
        solutions[current_task] = '\n'.join(current_solution)
    
    return solutions

def main():
    print("🎯 Валидатор решений SQL-задач")
    print("=" * 50)
    
    # Выбор базы данных
    db_dir = Path('data/databases')
    if not db_dir.exists():
        print("❌ Каталог data/databases не найден")
        return
    
    db_files = list(db_dir.glob('*.db'))
    if not db_files:
        print("❌ Нет доступных баз данных")
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
    
    # Выбор файла решений
    solutions_dir = Path('solutions')
    solution_files = list(solutions_dir.glob('*_solutions.sql'))
    
    if not solution_files:
        print("❌ Нет файлов решений")
        return
    
    print("\n📋 Доступные файлы решений:")
    for i, sol_file in enumerate(solution_files, 1):
        print(f"{i}. {sol_file.name}")
    
    try:
        sol_choice = int(input("\nВыберите файл решений (номер): ")) - 1
        if 0 <= sol_choice < len(solution_files):
            selected_solution_file = solution_files[sol_choice]
        else:
            print("❌ Неверный номер")
            return
    except ValueError:
        print("❌ Введите корректный номер")
        return
    
    # Загружаем эталонные решения
    solutions = load_solutions(selected_solution_file)
    if not solutions:
        print("❌ Нет решений в файле")
        return
    
    print(f"\n✅ Загружено {len(solutions)} задач")
    
    # Создаем валидатор
    validator = SolutionValidator(selected_db)
    
    # Интерактивная проверка
    while True:
        print("\n" + "=" * 50)
        print("Выберите действие:")
        print("1. Проверить конкретную задачу")
        print("2. Проверить все задачи")
        print("3. Показать список задач")
        print("4. Выход")
        
        choice = input("\nВведите номер: ").strip()
        
        if choice == '1':
            print("\n📋 Доступные задачи:")
            for i, task_name in enumerate(solutions.keys(), 1):
                print(f"{i}. {task_name}")
            
            try:
                task_choice = int(input("\nВыберите задачу (номер): ")) - 1
                task_names = list(solutions.keys())
                if 0 <= task_choice < len(task_names):
                    selected_task = task_names[task_choice]
                    expected_query = solutions[selected_task]
                    
                    print(f"\n📝 Задача: {selected_task}")
                    print(f"📝 Эталонный запрос: {expected_query}")
                    
                    user_query = input("\nВведите ваш SQL-запрос: ").strip()
                    if user_query:
                        validator.validate_solution(selected_task, user_query, expected_query)
                else:
                    print("❌ Неверный номер")
            except ValueError:
                print("❌ Введите корректный номер")
        
        elif choice == '2':
            correct = 0
            total = len(solutions)
            
            for task_name, expected_query in solutions.items():
                print(f"\n📝 Задача: {task_name}")
                user_query = input("Введите ваш SQL-запрос (или 'пропустить'): ").strip()
                
                if user_query.lower() == 'пропустить':
                    continue
                
                if user_query:
                    if validator.validate_solution(task_name, user_query, expected_query):
                        correct += 1
            
            print(f"\n🏁 Результаты: {correct}/{total} задач решено верно")
            
        elif choice == '3':
            print("\n📋 Список задач:")
            for i, task_name in enumerate(solutions.keys(), 1):
                print(f"{i}. {task_name}")
        
        elif choice == '4':
            print("👋 До свидания!")
            break
        
        else:
            print("❌ Неверный выбор")

if __name__ == "__main__":
    main()