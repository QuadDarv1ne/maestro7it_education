#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Продвинутая аналитика для базы данных товаров Ozon

Этот скрипт демонстрирует дополнительные аналитические возможности использования DuckDB
на наборе данных товаров Ozon.
"""

import duckdb
import pandas as pd
import os

# Configuration
DATABASE_NAME = os.getenv('DUCKDB_DATABASE_NAME', 'ozon_products.duckdb')

def connect_to_database():
    """Установить соединение с базой данных."""
    try:
        con = duckdb.connect(DATABASE_NAME)
        print(f"✅ Подключено к базе данных: {DATABASE_NAME}")
        return con
    except Exception as e:
        print(f"❌ Ошибка подключения к базе данных: {e}")
        return None

def run_advanced_analytics(con):
    """Выполнить продвинутые аналитические запросы к данным."""
    print("\n" + "="*60)
    print("ОТЧЕТ ПРОДВИНУТОЙ АНАЛИТИКИ")
    print("="*60)
    
    # 1. Анализ цен по категории
    print("\n💰 Средняя цена по категории:")
    try:
        avg_price_by_category = con.execute("""
            SELECT 
                category,
                COUNT(*) as product_count,
                AVG(price) as avg_price,
                MIN(price) as min_price,
                MAX(price) as max_price
            FROM ozon_products
            GROUP BY category
            ORDER BY avg_price DESC;
        """).fetchdf()
        print(avg_price_by_category)
    except Exception as e:
        print(f"❌ Error in average price by category query: {e}")
    
    # 2. Анализ скидок
    print("\n🏷️  Анализ скидок:")
    try:
        discount_analysis = con.execute("""
            SELECT 
                name,
                brand,
                price,
                old_price,
                ROUND(((old_price - price) / old_price) * 100, 2) as discount_percent
            FROM ozon_products
            WHERE old_price > price
            ORDER BY discount_percent DESC
            LIMIT 10;
        """).fetchdf()
        print(discount_analysis)
    except Exception as e:
        print(f"❌ Error in discount analysis query: {e}")
    
    # 3. Анализ доступности товаров
    print("\n📦 Доступность товаров по брендам:")
    try:
        stock_analysis = con.execute("""
            SELECT 
                brand,
                COUNT(*) as total_products,
                SUM(CASE WHEN is_in_stock THEN 1 ELSE 0 END) as in_stock_count,
                ROUND((SUM(CASE WHEN is_in_stock THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 2) as in_stock_percentage
            FROM ozon_products
            GROUP BY brand
            ORDER BY in_stock_percentage DESC;
        """).fetchdf()
        print(stock_analysis)
    except Exception as e:
        print(f"❌ Error in stock analysis query: {e}")
    
    # 4. Корреляция цены и рейтинга
    print("\n📈 Корреляция цены и рейтинга:")
    try:
        price_rating_correlation = con.execute("""
            SELECT 
                category,
                AVG(price) as avg_price,
                AVG(rating) as avg_rating,
                COUNT(*) as product_count
            FROM ozon_products
            WHERE rating IS NOT NULL
            GROUP BY category
            HAVING COUNT(*) >= 2
            ORDER BY avg_rating DESC;
        """).fetchdf()
        print(price_rating_correlation)
    except Exception as e:
        print(f"❌ Error in price vs rating query: {e}")
    
    # 5. Анализ количества отзывов
    print("\n👥 Товары с высоким количеством отзывов:")
    try:
        high_review_products = con.execute("""
            SELECT 
                name,
                brand,
                rating,
                review_count
            FROM ozon_products
            WHERE review_count > 1000
            ORDER BY review_count DESC;
        """).fetchdf()
        print(high_review_products)
    except Exception as e:
        print(f"❌ Error in high review products query: {e}")

def export_data(con):
    """Экспорт данных в различные форматы."""
    print("\n" + "="*60)
    print("ЭКСПОРТ ДАННЫХ")
    print("="*60)
    
    try:
        # Export to CSV
        con.execute("""
            COPY (SELECT * FROM ozon_products ORDER BY price DESC) 
            TO 'ozon_products_export.csv' (FORMAT CSV, HEADER);
        """)
        print("✅ Exported data to 'ozon_products_export.csv'")
        
        # Export top products to JSON
        con.execute("""
            COPY (SELECT * FROM ozon_products WHERE rating > 4.5 ORDER BY price DESC LIMIT 10) 
            TO 'top_rated_products.json' (FORMAT JSON);
        """)
        print("✅ Exported top rated products to 'top_rated_products.json'")
        
    except Exception as e:
        print(f"❌ Error during export: {e}")

def main():
    """Основная функция для запуска всех анализов."""
    print("🚀 Запуск продвинутой аналитики для базы данных товаров Ozon...")
    
    # Подключиться к базе данных
    con = connect_to_database()
    if not con:
        return
    
    # Запустить продвинутую аналитику
    run_advanced_analytics(con)
    
    # Экспортировать данные
    export_data(con)
    
    # Закрыть соединение
    con.close()
    print("\n✨ Продвинутая аналитика успешно завершена!")
    print("📁 Проверьте экспортированные файлы: 'ozon_products_export.csv' и 'top_rated_products.json'")

if __name__ == "__main__":
    main()