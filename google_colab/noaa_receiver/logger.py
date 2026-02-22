"""
Модуль логирования для NOAA APT Receiver
"""

import logging
import sys
from pathlib import Path
from typing import Optional


def setup_logger(
    name: str = "noaa_receiver",
    level: str = "INFO",
    log_file: Optional[str] = None,
    log_format: Optional[str] = None,
) -> logging.Logger:
    """
    Настройка логгера с консольным и файловым выводом
    
    Args:
        name: Имя логгера
        level: Уровень логирования
        log_file: Путь к файлу логов (опционально)
        log_format: Формат сообщений
    
    Returns:
        Настроенный логгер
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # Очистка существующих обработчиков
    if logger.handlers:
        logger.handlers.clear()
    
    # Формат по умолчанию
    if log_format is None:
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    formatter = logging.Formatter(log_format, datefmt="%Y-%m-%d %H:%M:%S")
    
    # Консольный обработчик
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Файловый обработчик (опционально)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


# Глобальный логгер по умолчанию
default_logger = setup_logger()


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Получение логгера по имени"""
    if name:
        return setup_logger(name)
    return default_logger
