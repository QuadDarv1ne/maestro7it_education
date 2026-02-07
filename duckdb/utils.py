# -*- coding: utf-8 -*-
"""
Утилиты для проекта анализа товаров Ozon с помощью DuckDB

Этот модуль содержит вспомогательные функции и классы для проекта.
"""

import logging
import os
from datetime import datetime
from typing import Optional

def setup_logging(log_level: str = "INFO", log_file: Optional[str] = None):
    """
    Настроить систему логирования для проекта.
    
    Args:
        log_level: Уровень логирования (DEBUG, INFO, WARNING, ERROR)
        log_file: Путь к файлу лога (опционально)
    """
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Настройка корневого логгера
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))
    
    # Удалить существующие обработчики
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Создать форматтер
    formatter = logging.Formatter(log_format)
    
    # Настроить консольный обработчик
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, log_level.upper()))
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # Настроить файловый обработчик при необходимости
    if log_file:
        # Создать директорию для логов если она не существует
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(getattr(logging, log_level.upper()))
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    
    return root_logger


def get_logger(name: str) -> logging.Logger:
    """
    Получить логгер с указанным именем.
    
    Args:
        name: Имя логгера
        
    Returns:
        Объект логгера
    """
    return logging.getLogger(name)


def format_currency(value: float, currency: str = "RUB") -> str:
    """
    Форматировать значение валюты.
    
    Args:
        value: Значение для форматирования
        currency: Код валюты
        
    Returns:
        Отформатированная строка валюты
    """
    if currency == "RUB":
        return f"{value:,.2f} ₽".replace(",", " ")
    elif currency == "USD":
        return f"${value:,.2f}"
    else:
        return f"{value:,.2f} {currency}"


def calculate_discount_percent(old_price: float, new_price: float) -> float:
    """
    Рассчитать процент скидки.
    
    Args:
        old_price: Старая цена
        new_price: Новая цена
        
    Returns:
        Процент скидки
    """
    if old_price <= 0:
        return 0.0
    return round(((old_price - new_price) / old_price) * 100, 2)


def sanitize_filename(filename: str) -> str:
    """
    Очистить имя файла от недопустимых символов.
    
    Args:
        filename: Исходное имя файла
        
    Returns:
        Очищенное имя файла
    """
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename.strip()


def get_current_datetime_str() -> str:
    """
    Получить текущую дату и время в строковом формате.
    
    Returns:
        Строка с датой и временем
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def format_large_number(num: int) -> str:
    """
    Форматировать большое число для лучшего восприятия.
    
    Args:
        num: Число для форматирования
        
    Returns:
        Отформатированная строка числа
    """
    if num >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num / 1_000:.1f}K"
    else:
        return str(num)