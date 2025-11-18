"""
Дополнительные утилиты для Simple HR
Вспомогательные функции для работы с данными
"""

from datetime import datetime, date, timedelta
from typing import List, Dict, Any, Optional
import calendar


def calculate_work_days(start_date: date, end_date: date, exclude_weekends: bool = True) -> int:
    """
    Вычисляет количество рабочих дней между двумя датами
    
    Args:
        start_date: Дата начала
        end_date: Дата окончания
        exclude_weekends: Исключить выходные (сб, вс)
    
    Returns:
        int: Количество рабочих дней
    """
    if start_date > end_date:
        return 0
    
    days = 0
    current = start_date
    
    while current <= end_date:
        # Проверяем является ли день выходным
        if exclude_weekends and current.weekday() >= 5:  # 5=сб, 6=вс
            current += timedelta(days=1)
            continue
        
        days += 1
        current += timedelta(days=1)
    
    return days


def get_russian_month_name(month: int, genitive: bool = False) -> str:
    """
    Возвращает название месяца на русском
    
    Args:
        month: Номер месяца (1-12)
        genitive: Использовать родительный падеж
    
    Returns:
        str: Название месяца
    """
    if genitive:
        months = [
            'января', 'февраля', 'марта', 'апреля',
            'мая', 'июня', 'июля', 'августа',
            'сентября', 'октября', 'ноября', 'декабря'
        ]
    else:
        months = [
            'Январь', 'Февраль', 'Март', 'Апрель',
            'Май', 'Июнь', 'Июль', 'Август',
            'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
        ]
    
    return months[month - 1] if 1 <= month <= 12 else ''


def format_date_russian(dt: date, include_weekday: bool = False) -> str:
    """
    Форматирует дату в русском формате
    
    Args:
        dt: Дата для форматирования
        include_weekday: Включить день недели
    
    Returns:
        str: Отформатированная дата
    """
    if isinstance(dt, datetime):
        dt = dt.date()
    
    result = f"{dt.day} {get_russian_month_name(dt.month, genitive=True)} {dt.year}"
    
    if include_weekday:
        weekdays = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']
        result = f"{weekdays[dt.weekday()]}, {result}"
    
    return result


def calculate_age(birth_date: date) -> int:
    """
    Вычисляет возраст по дате рождения
    
    Args:
        birth_date: Дата рождения
    
    Returns:
        int: Возраст в годах
    """
    today = date.today()
    age = today.year - birth_date.year
    
    # Корректируем если день рождения еще не наступил в этом году
    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1
    
    return age


def calculate_work_experience(hire_date: date, end_date: Optional[date] = None) -> Dict[str, int]:
    """
    Вычисляет стаж работы
    
    Args:
        hire_date: Дата приема на работу
        end_date: Дата окончания работы (по умолчанию сегодня)
    
    Returns:
        dict: Словарь с годами, месяцами и днями стажа
    """
    if end_date is None:
        end_date = date.today()
    
    # Вычисляем разницу
    years = end_date.year - hire_date.year
    months = end_date.month - hire_date.month
    days = end_date.day - hire_date.day
    
    # Корректируем отрицательные значения
    if days < 0:
        months -= 1
        days += calendar.monthrange(end_date.year, end_date.month - 1 if end_date.month > 1 else 12)[1]
    
    if months < 0:
        years -= 1
        months += 12
    
    return {
        'years': years,
        'months': months,
        'days': days,
        'total_days': (end_date - hire_date).days
    }


def format_work_experience(experience: Dict[str, int]) -> str:
    """
    Форматирует стаж работы в читаемый вид
    
    Args:
        experience: Словарь со стажем (результат calculate_work_experience)
    
    Returns:
        str: Отформатированный стаж
    """
    parts = []
    
    years = experience['years']
    months = experience['months']
    days = experience['days']
    
    if years > 0:
        if years == 1:
            parts.append(f"{years} год")
        elif years in [2, 3, 4]:
            parts.append(f"{years} года")
        else:
            parts.append(f"{years} лет")
    
    if months > 0:
        if months == 1:
            parts.append(f"{months} месяц")
        elif months in [2, 3, 4]:
            parts.append(f"{months} месяца")
        else:
            parts.append(f"{months} месяцев")
    
    if days > 0 and not parts:  # Показываем дни только если нет лет и месяцев
        if days == 1:
            parts.append(f"{days} день")
        elif days in [2, 3, 4]:
            parts.append(f"{days} дня")
        else:
            parts.append(f"{days} дней")
    
    return " ".join(parts) if parts else "0 дней"


def generate_employee_report_filename(report_type: str, extension: str = 'csv') -> str:
    """
    Генерирует имя файла для отчета
    
    Args:
        report_type: Тип отчета
        extension: Расширение файла
    
    Returns:
        str: Имя файла
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f"hr_report_{report_type}_{timestamp}.{extension}"


def parse_russian_date(date_str: str) -> Optional[date]:
    """
    Парсит дату из различных русских форматов
    
    Args:
        date_str: Строка с датой
    
    Returns:
        date или None если не удалось распарсить
    """
    formats = [
        '%d.%m.%Y',
        '%d/%m/%Y',
        '%d-%m-%Y',
        '%Y-%m-%d',
        '%d %B %Y',
        '%d %b %Y'
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    
    return None


def chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
    """
    Разбивает список на chunks указанного размера
    
    Args:
        lst: Исходный список
        chunk_size: Размер chunk
    
    Returns:
        List[List]: Список chunks
    """
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """
    Безопасное деление с обработкой деления на ноль
    
    Args:
        numerator: Числитель
        denominator: Знаменатель
        default: Значение по умолчанию при делении на ноль
    
    Returns:
        float: Результат деления или default
    """
    try:
        return numerator / denominator if denominator != 0 else default
    except (TypeError, ZeroDivisionError):
        return default


def format_number_russian(number: int) -> str:
    """
    Форматирует число с правильным склонением
    
    Args:
        number: Число
    
    Returns:
        str: Отформатированное число с правильным склонением
    """
    # Определяем последнюю цифру
    last_digit = number % 10
    last_two_digits = number % 100
    
    # Для чисел от 11 до 14 особое правило
    if 11 <= last_two_digits <= 14:
        return f"{number} сотрудников"
    
    if last_digit == 1:
        return f"{number} сотрудник"
    elif last_digit in [2, 3, 4]:
        return f"{number} сотрудника"
    else:
        return f"{number} сотрудников"


def get_quarter(month: int) -> int:
    """
    Возвращает квартал по номеру месяца
    
    Args:
        month: Номер месяца (1-12)
    
    Returns:
        int: Номер квартала (1-4)
    """
    return (month - 1) // 3 + 1


def get_quarter_dates(year: int, quarter: int) -> tuple[date, date]:
    """
    Возвращает даты начала и окончания квартала
    
    Args:
        year: Год
        quarter: Номер квартала (1-4)
    
    Returns:
        tuple: (start_date, end_date)
    """
    if quarter < 1 or quarter > 4:
        raise ValueError("Quarter must be between 1 and 4")
    
    start_month = (quarter - 1) * 3 + 1
    end_month = start_month + 2
    
    start_date = date(year, start_month, 1)
    _, last_day = calendar.monthrange(year, end_month)
    end_date = date(year, end_month, last_day)
    
    return start_date, end_date
