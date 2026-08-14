"""
Общие вспомогательные функции
"""
from datetime import datetime


def format_date(date_obj, format='%Y-%m-%d'):
    """Форматирование даты в строку"""
    if date_obj is None:
        return ''
    return date_obj.strftime(format)


def is_upcoming(date_obj) -> bool:
    """Проверка, является ли дата будущей"""
    if date_obj is None:
        return False
    return date_obj > datetime.now()
