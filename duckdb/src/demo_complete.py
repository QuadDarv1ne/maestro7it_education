# -*- coding: utf-8 -*-
"""
Полная демонстрация проекта анализа товаров Ozon с помощью DuckDB

Этот скрипт демонстрирует все возможности проекта в одном примере.
"""

import os
import sys
from pathlib import Path

# Добавить путь к проекту для импорта модулей
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from config import LOG_LEVEL
from utils import setup_logging, get_logger
from ozon_db_setup import populate_database
from analytics import OzonAnalytics
from data_validator import DataValidator
from performance_monitor import PerformanceMonitor
from backup_manager import BackupManager


def main():
    """Основная функция для демонстрации всех возможностей проекта."""
    # Настроить логирование
    setup_logging(LOG_LEVEL)
    logger = get_logger(__name__)
    
    print("🎯 ПОЛНАЯ ДЕМОНСТРАЦИЯ ПРОЕКТА АНАЛИЗА ТОВАРОВ OZON")
    print("="*60)
    logger.info("Запуск полной демонстрации проекта")
    
    try:
        # 1. Инициализация базы данных
        print("\n1. 🗄️  ИНИЦИАЛИЗАЦИЯ БАЗЫ ДАННЫХ")
        print("-" * 40)
        populate_database()
        print("✅ База данных инициализирована")
        
        # Ждать немного времени, чтобы освободить файл базы данных
        import time
        time.sleep(2)
        
        # Принудительно выполнить сборку мусора и закрыть все возможные соединения
        import gc
        gc.collect()
        
        # 2. Валидация данных
        print("\n2. ✅ ПРОВЕРКА КАЧЕСТВА ДАННЫХ")
        print("-" * 40)
        validator = DataValidator()
        report = validator.generate_data_quality_report()
        # Вывести только сводку
        lines = report.split('\n')
        summary_started = False
        for line in lines:
            if 'СВОДКА:' in line:
                summary_started = True
            if summary_started:
                print(line)
        print("✅ Проверка качества данных завершена")
        
        # 3. Мониторинг производительности
        print("\n3. ⚡ МОНИТОРИНГ ПРОИЗВОДИТЕЛЬНОСТИ")
        print("-" * 40)
        monitor = PerformanceMonitor()
        
        # Тестировать производительность основных запросов
        queries = [
            ("SELECT COUNT(*) FROM ozon_products;", "Подсчет товаров"),
            ("SELECT * FROM ozon_products ORDER BY price DESC LIMIT 5;", "Топ дорогих"),
            ("SELECT brand, AVG(price) FROM ozon_products GROUP BY brand;", "Цены по брендам")
        ]
        
        for query, desc in queries:
            print(f"  Тест: {desc}")
            monitor.measure_query_performance(query)
        
        print(monitor.get_performance_summary())
        print("✅ Мониторинг производительности завершен")
        
        # 4. Аналитика
        print("\n4. 📊 КОМПЛЕКСНЫЙ АНАЛИЗ")
        print("-" * 40)
        analytics = OzonAnalytics()
        with analytics:
            # Получить основные отчеты
            top_products = analytics.get_top_products_by_price(limit=5)
            high_rated = analytics.get_products_by_rating(min_rating=4.5, limit=5)
            categories = analytics.get_category_statistics()
            
            print(f"  Топ-5 товаров по цене: {len(top_products)} найдено")
            print(f"  Товары с высоким рейтингом: {len(high_rated)} найдено")
            print(f"  Статистика по категориям: {len(categories)} категорий")
            
            # Экспорт результатов
            analytics.export_to_csv(top_products, "demo_top_products.csv")
            analytics.export_to_json(categories, "demo_categories.json")
            print("  ✅ Результаты анализа экспортированы")
        
        # Явно закрыть соединение и убедиться, что база данных освобождена
        del analytics
        import gc
        gc.collect()
        import time
        time.sleep(1)
        
        print("✅ Комплексный анализ завершен")
        
        # 5. Резервное копирование
        print("\n5. 💾 РЕЗЕРВНОЕ КОПИРОВАНИЕ")
        print("-" * 40)
        backup_manager = BackupManager()
        backup_path = backup_manager.create_backup("demo_backup.zip")
        print(f"  ✅ Резервная копия создана: {backup_path}")
        
        # Показать список резервных копий
        backups = backup_manager.list_backups()
        print(f"  Всего резервных копий: {len(backups)}")
        
        print("✅ Резервное копирование завершено")
        
        # 6. Сводка по всем операциям
        print("\n6. 📋 ИТОГОВАЯ СВОДКА")
        print("-" * 40)
        print("✅ Все компоненты проекта успешно продемонстрированы:")
        print("  - Инициализация базы данных")
        print("  - Проверка качества данных") 
        print("  - Мониторинг производительности")
        print("  - Комплексный аналитический отчет")
        print("  - Экспорт данных")
        print("  - Резервное копирование")
        
        print(f"\n✨ ПОЛНАЯ ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА УСПЕШНО!")
        print("Теперь вы можете использовать любой компонент проекта отдельно.")
        
    except Exception as e:
        logger.error(f"Ошибка в процессе демонстрации: {e}")
        print(f"❌ Ошибка: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)