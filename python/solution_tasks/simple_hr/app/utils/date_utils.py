"""
Утилиты для работы с датами, праздниками и рабочими днями
"""
from datetime import datetime, date, timedelta
from typing import List, Tuple, Optional


class RussianHolidays:
    """Класс для работы с российскими праздниками"""
    
    # Фиксированные праздники (месяц, день)
    FIXED_HOLIDAYS = [
        (1, 1),   # Новый год
        (1, 2),   # Новогодние каникулы
        (1, 3),   # Новогодние каникулы
        (1, 4),   # Новогодние каникулы
        (1, 5),   # Новогодние каникулы
        (1, 6),   # Новогодние каникулы
        (1, 7),   # Рождество Христово
        (1, 8),   # Новогодние каникулы
        (2, 23),  # День защитника Отечества
        (3, 8),   # Международный женский день
        (5, 1),   # Праздник Весны и Труда
        (5, 9),   # День Победы
        (6, 12),  # День России
        (11, 4),  # День народного единства
    ]
    
    @classmethod
    def is_holiday(cls, check_date: date) -> bool:
        """Проверить, является ли дата праздником"""
        return (check_date.month, check_date.day) in cls.FIXED_HOLIDAYS
    
    @classmethod
    def get_holidays_in_year(cls, year: int) -> List[date]:
        """Получить список праздников в году"""
        return [date(year, month, day) for month, day in cls.FIXED_HOLIDAYS]
    
    @classmethod
    def get_holidays_in_range(cls, start_date: date, end_date: date) -> List[date]:
        """Получить список праздников в диапазоне дат"""
        holidays = []
        current_year = start_date.year
        
        while current_year <= end_date.year:
            year_holidays = cls.get_holidays_in_year(current_year)
            for holiday in year_holidays:
                if start_date <= holiday <= end_date:
                    holidays.append(holiday)
            current_year += 1
        
        return holidays


class WorkingDays:
    """Класс для работы с рабочими днями"""
    
    @staticmethod
    def is_weekend(check_date: date) -> bool:
        """Проверить, является ли дата выходным (суббота или воскресенье)"""
        return check_date.weekday() in [5, 6]
    
    @staticmethod
    def is_working_day(check_date: date) -> bool:
        """Проверить, является ли дата рабочим днем"""
        return not (WorkingDays.is_weekend(check_date) or RussianHolidays.is_holiday(check_date))
    
    @staticmethod
    def count_working_days(start_date: date, end_date: date) -> int:
        """Подсчитать количество рабочих дней в диапазоне"""
        if start_date > end_date:
            return 0
        
        working_days = 0
        current = start_date
        
        while current <= end_date:
            if WorkingDays.is_working_day(current):
                working_days += 1
            current += timedelta(days=1)
        
        return working_days
    
    @staticmethod
    def count_weekends(start_date: date, end_date: date) -> int:
        """Подсчитать количество выходных дней в диапазоне"""
        if start_date > end_date:
            return 0
        
        total_days = (end_date - start_date).days + 1
        working_days = WorkingDays.count_working_days(start_date, end_date)
        
        return total_days - working_days
    
    @staticmethod
    def add_working_days(start_date: date, days: int) -> date:
        """Добавить N рабочих дней к дате"""
        current = start_date
        added = 0
        
        while added < days:
            current += timedelta(days=1)
            if WorkingDays.is_working_day(current):
                added += 1
        
        return current
    
    @staticmethod
    def get_next_working_day(check_date: date) -> date:
        """Получить следующий рабочий день"""
        next_day = check_date + timedelta(days=1)
        
        while not WorkingDays.is_working_day(next_day):
            next_day += timedelta(days=1)
        
        return next_day
    
    @staticmethod
    def get_previous_working_day(check_date: date) -> date:
        """Получить предыдущий рабочий день"""
        prev_day = check_date - timedelta(days=1)
        
        while not WorkingDays.is_working_day(prev_day):
            prev_day -= timedelta(days=1)
        
        return prev_day


class VacationCalculator:
    """Класс для расчета отпусков"""
    
    # Стандартное количество дней отпуска в год (28 календарных дней)
    STANDARD_VACATION_DAYS = 28
    
    @staticmethod
    def calculate_vacation_days_earned(hire_date: date, current_date: Optional[date] = None) -> float:
        """
        Рассчитать количество заработанных дней отпуска
        
        Args:
            hire_date: Дата найма
            current_date: Текущая дата (по умолчанию - сегодня)
        
        Returns:
            Количество дней отпуска с учетом дробной части
        """
        if current_date is None:
            current_date = date.today()
        
        if hire_date > current_date:
            return 0.0
        
        # Рассчитываем количество отработанных месяцев
        months_worked = (current_date.year - hire_date.year) * 12
        months_worked += current_date.month - hire_date.month
        
        # Учитываем дни месяца
        if current_date.day < hire_date.day:
            months_worked -= 1
        
        # 2.33 дня отпуска в месяц (28 / 12)
        vacation_days_per_month = VacationCalculator.STANDARD_VACATION_DAYS / 12
        
        return round(months_worked * vacation_days_per_month, 2)
    
    @staticmethod
    def calculate_vacation_allowance(
        daily_salary: float,
        vacation_days: int,
        start_date: date,
        end_date: date
    ) -> float:
        """
        Рассчитать сумму отпускных
        
        Args:
            daily_salary: Средний дневной заработок
            vacation_days: Количество дней отпуска
            start_date: Дата начала отпуска
            end_date: Дата окончания отпуска
        
        Returns:
            Сумма отпускных
        """
        # Базовая сумма
        total = daily_salary * vacation_days
        
        # Проверяем, есть ли праздники в период отпуска
        holidays = RussianHolidays.get_holidays_in_range(start_date, end_date)
        
        # Праздники не оплачиваются дополнительно
        # но и не вычитаются из отпуска
        
        return round(total, 2)
    
    @staticmethod
    def get_vacation_period_breakdown(start_date: date, end_date: date) -> dict:
        """
        Получить детальную информацию о периоде отпуска
        
        Returns:
            Словарь с информацией о периоде
        """
        total_days = (end_date - start_date).days + 1
        working_days = WorkingDays.count_working_days(start_date, end_date)
        weekends = WorkingDays.count_weekends(start_date, end_date)
        holidays = len(RussianHolidays.get_holidays_in_range(start_date, end_date))
        
        return {
            'total_days': total_days,
            'working_days': working_days,
            'weekends': weekends,
            'holidays': holidays,
            'start_date': start_date,
            'end_date': end_date
        }
    
    @staticmethod
    def is_vacation_valid(
        start_date: date,
        end_date: date,
        min_days: int = 1,
        max_days: int = 28
    ) -> Tuple[bool, Optional[str]]:
        """
        Проверить валидность периода отпуска
        
        Returns:
            Кортеж (валиден, сообщение об ошибке)
        """
        if start_date > end_date:
            return False, "Дата начала не может быть позже даты окончания"
        
        total_days = (end_date - start_date).days + 1
        
        if total_days < min_days:
            return False, f"Минимальная продолжительность отпуска: {min_days} дней"
        
        if total_days > max_days:
            return False, f"Максимальная продолжительность отпуска: {max_days} дней"
        
        # Проверка, что отпуск не в прошлом
        if end_date < date.today():
            return False, "Нельзя создать отпуск в прошлом"
        
        return True, None


class DateFormatter:
    """Класс для форматирования дат на русском языке"""
    
    MONTHS_GENITIVE = [
        'января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
        'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря'
    ]
    
    MONTHS_NOMINATIVE = [
        'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
        'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
    ]
    
    WEEKDAYS = [
        'Понедельник', 'Вторник', 'Среда', 'Четверг',
        'Пятница', 'Суббота', 'Воскресенье'
    ]
    
    @classmethod
    def format_russian(cls, date_obj: date, include_year: bool = True) -> str:
        """Форматировать дату на русском: '15 марта 2024 г.'"""
        if include_year:
            return f"{date_obj.day} {cls.MONTHS_GENITIVE[date_obj.month - 1]} {date_obj.year} г."
        return f"{date_obj.day} {cls.MONTHS_GENITIVE[date_obj.month - 1]}"
    
    @classmethod
    def format_with_weekday(cls, date_obj: date) -> str:
        """Форматировать дату с днем недели: 'Понедельник, 15 марта 2024 г.'"""
        weekday = cls.WEEKDAYS[date_obj.weekday()]
        date_str = cls.format_russian(date_obj)
        return f"{weekday}, {date_str}"
    
    @classmethod
    def get_month_name(cls, month: int, nominative: bool = True) -> str:
        """Получить название месяца"""
        if nominative:
            return cls.MONTHS_NOMINATIVE[month - 1]
        return cls.MONTHS_GENITIVE[month - 1]
    
    @classmethod
    def format_date_range(cls, start: date, end: date) -> str:
        """Форматировать диапазон дат: '1-15 марта 2024 г.'"""
        if start.month == end.month and start.year == end.year:
            return f"{start.day}-{end.day} {cls.MONTHS_GENITIVE[start.month - 1]} {start.year} г."
        elif start.year == end.year:
            return (f"{start.day} {cls.MONTHS_GENITIVE[start.month - 1]} - "
                   f"{end.day} {cls.MONTHS_GENITIVE[end.month - 1]} {start.year} г.")
        else:
            return f"{cls.format_russian(start)} - {cls.format_russian(end)}"


# Удобные функции для быстрого доступа

def is_working_day(check_date: date) -> bool:
    """Проверить, является ли дата рабочим днем"""
    return WorkingDays.is_working_day(check_date)


def count_working_days(start: date, end: date) -> int:
    """Подсчитать рабочие дни в диапазоне"""
    return WorkingDays.count_working_days(start, end)


def format_date_russian(date_obj: date) -> str:
    """Форматировать дату на русском"""
    return DateFormatter.format_russian(date_obj)


def calculate_vacation_days(hire_date: date) -> float:
    """Рассчитать заработанные дни отпуска"""
    return VacationCalculator.calculate_vacation_days_earned(hire_date)
