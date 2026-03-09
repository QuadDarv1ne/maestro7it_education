#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Расширенная аналитика для базы данных товаров Ozon

Этот модуль содержит расширенные аналитические функции для анализа
данных товаров Ozon с использованием DuckDB.
"""

import duckdb
import pandas as pd
import json
from typing import Dict, List, Optional, Tuple
from config import DATABASE_NAME, ANALYTICS_CONFIG, EXPORT_CONFIG
from utils import get_logger, format_currency, calculate_discount_percent, sanitize_filename, format_large_number
import os

logger = get_logger(__name__)


class OzonAnalytics:
    """Класс для выполнения аналитики над данными товаров Ozon."""
    
    def __init__(self, db_path: str = DATABASE_NAME):
        """
        Инициализировать аналитический класс.
        
        Args:
            db_path: Путь к базе данных DuckDB
        """
        self.db_path = db_path
        self.con = None
        logger.info(f"Инициализация аналитики с базой данных: {db_path}")
    
    def __enter__(self):
        """Контекстный менеджер входа."""
        self.con = duckdb.connect(self.db_path)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Контекстный менеджер выхода."""
        if self.con:
            self.con.close()
            logger.info("Соединение с базой данных закрыто")
    
    def connect(self):
        """Установить соединение с базой данных."""
        if self.con is None:
            self.con = duckdb.connect(self.db_path)
            logger.debug(f"Соединение установлено с {self.db_path}")
    
    def close(self):
        """Закрыть соединение с базой данных."""
        if self.con:
            self.con.close()
            self.con = None
            logger.debug("Соединение с базой данных закрыто")
    
    def get_top_products_by_price(self, limit: int = 10) -> pd.DataFrame:
        """
        Получить топ товаров по цене.
        
        Args:
            limit: Количество товаров для возврата
            
        Returns:
            DataFrame с топ товарами по цене
        """
        logger.info(f"Получение топ-{limit} товаров по цене")
        query = f"""
            SELECT 
                name,
                brand,
                category,
                price,
                rating,
                review_count,
                CASE 
                    WHEN old_price > price THEN ROUND(((old_price - price) / old_price) * 100, 2)
                    ELSE 0 
                END as discount_percent
            FROM ozon_products
            ORDER BY price DESC
            LIMIT {limit};
        """
        try:
            result = self.con.execute(query).fetchdf()
            logger.info(f"Получено {len(result)} товаров")
            return result
        except Exception as e:
            logger.error(f"Ошибка при получении топ товаров по цене: {e}")
            raise
    
    def get_products_by_rating(self, min_rating: float = 4.5, limit: int = 10) -> pd.DataFrame:
        """
        Получить товары с рейтингом выше указанного значения.

        Args:
            min_rating: Минимальный рейтинг
            limit: Количество товаров для возврата

        Returns:
            DataFrame с товарами по рейтингу
        """
        logger.info(f"Получение товаров с рейтингом выше {min_rating} (лимит: {limit})")
        query = """
            SELECT
                name,
                brand,
                category,
                price,
                rating,
                review_count
            FROM ozon_products
            WHERE rating >= ?
            ORDER BY rating DESC, review_count DESC
            LIMIT ?;
        """
        try:
            result = self.con.execute(query, [min_rating, limit]).fetchdf()
            logger.info(f"Получено {len(result)} товаров с высоким рейтингом")
            return result
        except Exception as e:
            logger.error(f"Ошибка при получении товаров по рейтингу: {e}")
            raise
    
    def get_discount_products(self, min_discount: float = 10.0, limit: int = 10) -> pd.DataFrame:
        """
        Получить товары со скидкой больше указанного значения.
        
        Args:
            min_discount: Минимальный процент скидки
            limit: Количество товаров для возврата
            
        Returns:
            DataFrame с товарами со скидками
        """
        logger.info(f"Получение товаров со скидкой больше {min_discount}% (лимит: {limit})")
        query = f"""
            SELECT 
                name,
                brand,
                category,
                price,
                old_price,
                ROUND(((old_price - price) / old_price) * 100, 2) as discount_percent,
                rating
            FROM ozon_products
            WHERE old_price > price AND ((old_price - price) / old_price) * 100 >= {min_discount}
            ORDER BY discount_percent DESC
            LIMIT {limit};
        """
        try:
            result = self.con.execute(query).fetchdf()
            logger.info(f"Получено {len(result)} товаров со скидками")
            return result
        except Exception as e:
            logger.error(f"Ошибка при получении товаров со скидками: {e}")
            raise
    
    def get_category_statistics(self) -> pd.DataFrame:
        """
        Получить статистику по категориям товаров.
        
        Returns:
            DataFrame со статистикой по категориям
        """
        logger.info("Получение статистики по категориям товаров")
        query = """
            SELECT 
                category,
                COUNT(*) as product_count,
                AVG(price) as avg_price,
                MIN(price) as min_price,
                MAX(price) as max_price,
                AVG(rating) as avg_rating,
                SUM(review_count) as total_reviews
            FROM ozon_products
            GROUP BY category
            ORDER BY product_count DESC;
        """
        try:
            result = self.con.execute(query).fetchdf()
            logger.info(f"Получена статистика для {len(result)} категорий")
            return result
        except Exception as e:
            logger.error(f"Ошибка при получении статистики по категориям: {e}")
            raise
    
    def get_brand_performance(self) -> pd.DataFrame:
        """
        Получить статистику по брендам.
        
        Returns:
            DataFrame со статистикой по брендам
        """
        logger.info("Получение статистики по брендам")
        query = """
            SELECT 
                brand,
                COUNT(*) as product_count,
                AVG(price) as avg_price,
                AVG(rating) as avg_rating,
                SUM(review_count) as total_reviews,
                AVG(CASE 
                    WHEN old_price > price THEN ((old_price - price) / old_price) * 100 
                    ELSE 0 
                END) as avg_discount_percent
            FROM ozon_products
            GROUP BY brand
            ORDER BY avg_rating DESC, product_count DESC;
        """
        try:
            result = self.con.execute(query).fetchdf()
            logger.info(f"Получена статистика для {len(result)} брендов")
            return result
        except Exception as e:
            logger.error(f"Ошибка при получении статистики по брендам: {e}")
            raise
    
    def get_inventory_status(self) -> pd.DataFrame:
        """
        Получить статус инвентаря (в наличии/нет на складе).
        
        Returns:
            DataFrame со статусом инвентаря
        """
        logger.info("Получение статуса инвентаря")
        query = """
            SELECT 
                is_in_stock,
                COUNT(*) as count,
                AVG(price) as avg_price,
                AVG(rating) as avg_rating
            FROM ozon_products
            GROUP BY is_in_stock
            ORDER BY is_in_stock DESC;
        """
        try:
            result = self.con.execute(query).fetchdf()
            logger.info(f"Получен статус инвентаря для {len(result)} групп")
            return result
        except Exception as e:
            logger.error(f"Ошибка при получении статуса инвентаря: {e}")
            raise
    
    def export_to_csv(self, df: pd.DataFrame, filename: str, subdir: str = "exports") -> str:
        """
        Экспортировать DataFrame в CSV файл.
        
        Args:
            df: DataFrame для экспорта
            filename: Имя файла
            subdir: Поддиректория для экспорта
            
        Returns:
            Путь к экспортированному файлу
        """
        # Очистить имя файла
        clean_filename = sanitize_filename(filename)
        if not clean_filename.endswith('.csv'):
            clean_filename += '.csv'
        
        # Создать полный путь к файлу
        export_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), subdir)
        os.makedirs(export_dir, exist_ok=True)
        filepath = os.path.join(export_dir, clean_filename)
        
        logger.info(f"Экспорт DataFrame в CSV: {filepath}")
        try:
            # Объединить параметры, передаваемые в to_csv, избегая дублирования
            csv_params = EXPORT_CONFIG['csv_format_options'].copy()
            csv_params['index'] = False  # Убедиться, что index всегда False
            df.to_csv(filepath, **csv_params)
            logger.info(f"Экспорт завершен: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Ошибка при экспорте в CSV: {e}")
            raise
    
    def export_to_json(self, df: pd.DataFrame, filename: str, subdir: str = "exports") -> str:
        """
        Экспортировать DataFrame в JSON файл.
        
        Args:
            df: DataFrame для экспорта
            filename: Имя файла
            subdir: Поддиректория для экспорта
            
        Returns:
            Путь к экспортированному файлу
        """
        # Очистить имя файла
        clean_filename = sanitize_filename(filename)
        if not clean_filename.endswith('.json'):
            clean_filename += '.json'
        
        # Создать полный путь к файлу
        export_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), subdir)
        os.makedirs(export_dir, exist_ok=True)
        filepath = os.path.join(export_dir, clean_filename)
        
        logger.info(f"Экспорт DataFrame в JSON: {filepath}")
        try:
            # Объединить параметры, передаваемые в to_json, избегая дублирования
            json_params = EXPORT_CONFIG['json_format_options'].copy()
            json_params['force_ascii'] = False  # Убедиться, что force_ascii всегда False
            df.to_json(filepath, **json_params)
            logger.info(f"Экспорт завершен: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Ошибка при экспорте в JSON: {e}")
            raise
    
    def run_comprehensive_report(self) -> Dict[str, pd.DataFrame]:
        """
        Выполнить комплексный аналитический отчет.
        
        Returns:
            Словарь с результатами аналитики
        """
        logger.info("Запуск комплексного аналитического отчета")
        
        report_data = {}
        
        # Топ дорогих товаров
        report_data['top_expensive'] = self.get_top_products_by_price(limit=ANALYTICS_CONFIG['top_products_limit'])
        
        # Товары с высоким рейтингом
        report_data['high_rated'] = self.get_products_by_rating(
            min_rating=ANALYTICS_CONFIG['min_rating_filter'],
            limit=ANALYTICS_CONFIG['top_products_limit']
        )
        
        # Товары со скидками
        report_data['discounted'] = self.get_discount_products(
            min_discount=ANALYTICS_CONFIG['discount_threshold'],
            limit=ANALYTICS_CONFIG['top_products_limit']
        )
        
        # Статистика по категориям
        report_data['categories'] = self.get_category_statistics()
        
        # Статистика по брендам
        report_data['brands'] = self.get_brand_performance()
        
        # Статус инвентаря
        report_data['inventory'] = self.get_inventory_status()
        
        logger.info("Комплексный отчет завершен")
        return report_data


def main():
    """Основная функция для демонстрации возможностей аналитики."""
    import sys
    from config import LOG_LEVEL
    from utils import setup_logging
    
    # Настроить логирование
    setup_logging(LOG_LEVEL)
    
    logger.info("Запуск расширенной аналитики товаров Ozon")
    
    try:
        # Использовать контекстный менеджер для безопасной работы с базой данных
        with OzonAnalytics() as analytics:
            # Выполнить комплексный отчет
            report = analytics.run_comprehensive_report()
            
            # Показать основные результаты
            print("\n📊 КОМПЛЕКСНЫЙ АНАЛИТИЧЕСКИЙ ОТЧЕТ")
            print("="*50)
            
            print(f"\n💰 Топ-{len(report['top_expensive'])} самых дорогих товаров:")
            for idx, row in report['top_expensive'].head(5).iterrows():
                print(f"  • {row['name']} ({row['brand']}) - {format_currency(row['price'])}, "
                      f"рейтинг: {row['rating']}/5")
            
            print(f"\n⭐ Товары с высоким рейтингом (>{ANALYTICS_CONFIG['min_rating_filter']}):")
            for idx, row in report['high_rated'].head(5).iterrows():
                print(f"  • {row['name']} ({row['brand']}) - рейтинг: {row['rating']}/5, "
                      f"отзывов: {format_large_number(row['review_count'])}")
            
            print(f"\n🏷️  Товары со скидкой (>{ANALYTICS_CONFIG['discount_threshold']}%):")
            for idx, row in report['discounted'].head(5).iterrows():
                discount = row['discount_percent']
                print(f"  • {row['name']} - скидка: {discount}%, "
                      f"цена: {format_currency(row['price'])}")
            
            print(f"\n📈 Статистика по категориям (топ 5):")
            for idx, row in report['categories'].head(5).iterrows():
                print(f"  • {row['category']}: {row['product_count']} товаров, "
                      f"ср. цена: {format_currency(row['avg_price'])}, "
                      f"ср. рейтинг: {row['avg_rating']:.2f}")
            
            print(f"\n🏆 Лучшие бренды (по рейтингу):")
            for idx, row in report['brands'].head(5).iterrows():
                print(f"  • {row['brand']}: {row['product_count']} товаров, "
                      f"ср. рейтинг: {row['avg_rating']:.2f}")
            
            # Экспортировать результаты
            print(f"\n📤 Экспорт результатов в файлы...")
            analytics.export_to_csv(report['top_expensive'], "top_expensive_products.csv")
            analytics.export_to_csv(report['high_rated'], "high_rated_products.csv")
            analytics.export_to_json(report['categories'], "category_statistics.json")
            
            print("\n✨ Анализ завершен успешно!")
            
    except Exception as e:
        logger.error(f"Ошибка в процессе анализа: {e}")
        print(f"❌ Ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()