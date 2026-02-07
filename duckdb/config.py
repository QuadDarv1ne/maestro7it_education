# -*- coding: utf-8 -*-
"""
Конфигурация проекта для анализа товаров Ozon с помощью DuckDB

Этот модуль содержит настройки конфигурации для проекта.
"""

import os

# Основные настройки
DATABASE_NAME = os.getenv('DUCKDB_DATABASE_NAME', 'ozon_products.duckdb')
DEBUG_MODE = os.getenv('DEBUG_MODE', 'False').lower() == 'true'
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# Настройки путей
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXPORT_DIR = os.path.join(BASE_DIR, 'exports')
DATA_DIR = os.path.join(BASE_DIR, 'data')

# Создание директорий если они не существуют
os.makedirs(EXPORT_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

# Настройки аналитики
ANALYTICS_CONFIG = {
    'top_products_limit': int(os.getenv('TOP_PRODUCTS_LIMIT', '10')),
    'min_rating_filter': float(os.getenv('MIN_RATING_FILTER', '4.0')),
    'min_review_count': int(os.getenv('MIN_REVIEW_COUNT', '100')),
    'discount_threshold': float(os.getenv('DISCOUNT_THRESHOLD', '10.0'))
}

# Настройки экспорта
EXPORT_CONFIG = {
    'csv_format_options': {
        'index': False
    },
    'json_format_options': {
        'orient': 'records',
        'force_ascii': False
    }
}