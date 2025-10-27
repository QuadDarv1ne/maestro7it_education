#!/usr/bin/env python
"""
Скрипт для запуска автоматических проверок и напоминаний
Запускать ежедневно через cron или планировщик задач
"""

import sys
import os

# Добавляем путь к приложению в sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.utils.reminders import run_daily_checks

def main():
    """Основная функция для запуска проверок"""
    app = create_app()
    
    with app.app_context():
        print("Запуск ежедневных проверок...")
        results = run_daily_checks()
        
        if 'error' in results:
            print(f"Ошибка: {results['error']}")
            return 1
        
        print("Ежедневные проверки завершены успешно:")
        print(f"- Напоминаний о завершении отпусков: {results['vacation_endings']}")
        print(f"- Напоминаний о начале отпусков: {results['vacation_starts']}")
        print(f"- Удалено старых отпусков: {results['cleaned_vacations']}")
        
        stats = results['vacation_stats']
        print("\nСтатистика по отпускам:")
        print(f"- Всего отпусков: {stats['total']}")
        print(f"- Оплачиваемых: {stats['paid']}")
        print(f"- Неоплачиваемых: {stats['unpaid']}")
        print(f"- Больничных: {stats['sick']}")
        print(f"- Текущих: {stats['current']}")
        
        return 0

if __name__ == '__main__':
    sys.exit(main())