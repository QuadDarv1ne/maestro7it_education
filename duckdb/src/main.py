#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Главный модуль проекта анализа товаров Ozon с помощью DuckDB

Этот модуль служит центральной точкой входа для всего проекта.
"""

import argparse
import sys
import os
from pathlib import Path

# Добавить путь к проекту для импорта модулей
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from config import DATABASE_NAME, DEBUG_MODE, LOG_LEVEL
from utils import setup_logging, get_logger
from ozon_db_setup import populate_database
from analytics import OzonAnalytics


def parse_arguments():
    """Разобрать аргументы командной строки."""
    parser = argparse.ArgumentParser(
        description="Проект анализа товаров Ozon с помощью DuckDB"
    )
    
    parser.add_argument(
        '--init-db',
        action='store_true',
        help='Инициализировать базу данных с начальными данными'
    )
    
    parser.add_argument(
        '--run-analytics',
        action='store_true',
        help='Запустить аналитические отчеты'
    )
    
    parser.add_argument(
        '--export-data',
        action='store_true',
        help='Экспортировать данные в различные форматы'
    )
    
    parser.add_argument(
        '--full-analysis',
        action='store_true',
        help='Выполнить полный анализ (инициализация + аналитика + экспорт)'
    )
    
    parser.add_argument(
        '--db-path',
        type=str,
        default=DATABASE_NAME,
        help=f'Путь к базе данных (по умолчанию: {DATABASE_NAME})'
    )
    
    parser.add_argument(
        '--log-level',
        type=str,
        default=LOG_LEVEL,
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        help=f'Уровень логирования (по умолчанию: {LOG_LEVEL})'
    )
    
    return parser.parse_args()


def initialize_database(db_path: str):
    """Инициализировать базу данных с начальными данными."""
    logger = get_logger(__name__)
    logger.info(f"Инициализация базы данных: {db_path}")
    
    try:
        populate_database(db_path)
        logger.info("База данных успешно инициализирована")
        return True
    except Exception as e:
        logger.error(f"Ошибка при инициализации базы данных: {e}")
        return False


def run_analytics(db_path: str):
    """Запустить аналитические отчеты."""
    logger = get_logger(__name__)
    logger.info(f"Запуск аналитики для базы данных: {db_path}")
    
    try:
        with OzonAnalytics(db_path) as analytics:
            report = analytics.run_comprehensive_report()
            logger.info("Аналитика успешно выполнена")
            return report
    except Exception as e:
        logger.error(f"Ошибка при выполнении аналитики: {e}")
        return None


def export_data(db_path: str):
    """Экспортировать данные из базы."""
    logger = get_logger(__name__)
    logger.info(f"Экспорт данных из базы: {db_path}")
    
    try:
        with OzonAnalytics(db_path) as analytics:
            # Пример экспорта различных отчетов
            top_products = analytics.get_top_products_by_price(limit=20)
            high_rated = analytics.get_products_by_rating(min_rating=4.5, limit=20)
            categories_stats = analytics.get_category_statistics()
            
            # Экспорт в различные форматы
            analytics.export_to_csv(top_products, "exported_top_products.csv")
            analytics.export_to_csv(high_rated, "exported_high_rated_products.csv")
            analytics.export_to_json(categories_stats, "exported_category_stats.json")
            
            logger.info("Данные успешно экспортированы")
            return True
    except Exception as e:
        logger.error(f"Ошибка при экспорте данных: {e}")
        return False


def main():
    """Основная функция приложения."""
    # Разобрать аргументы командной строки
    args = parse_arguments()
    
    # Настроить логирование
    setup_logging(args.log_level)
    logger = get_logger(__name__)
    
    logger.info("Запуск проекта анализа товаров Ozon с помощью DuckDB")
    logger.info(f"Режим отладки: {DEBUG_MODE}")
    
    success = True
    
    # Выполнить запрошенные действия
    if args.init_db or args.full_analysis:
        logger.info("Шаг 1: Инициализация базы данных")
        success &= initialize_database(args.db_path)
    
    if (args.run_analytics or args.full_analysis) and success:
        logger.info("Шаг 2: Выполнение аналитики")
        analytics_result = run_analytics(args.db_path)
        if analytics_result is None:
            success = False
    
    if (args.export_data or args.full_analysis) and success:
        logger.info("Шаг 3: Экспорт данных")
        success &= export_data(args.db_path)
    
    if success:
        logger.info("Все операции завершены успешно!")
        print("\n✅ Все операции завершены успешно!")
        return 0
    else:
        logger.error("Один или несколько этапов завершились с ошибкой")
        print("\n❌ Один или несколько этапов завершились с ошибкой")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)