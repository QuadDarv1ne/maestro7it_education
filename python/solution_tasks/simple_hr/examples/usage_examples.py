"""
Примеры использования новых функций Simple HR v2.2

Демонстрация работы с датами, валидацией и расчетом отпусков
"""

from datetime import date, timedelta
from app.utils.date_utils import (
    RussianHolidays,
    WorkingDays,
    VacationCalculator,
    DateFormatter,
    is_working_day,
    count_working_days,
    format_date_russian
)
from app.utils.validators import (
    Validator,
    EmployeeValidator,
    VacationValidator,
    ValidationError
)


def example_holidays():
    """Примеры работы с праздниками"""
    print("=" * 60)
    print("1. РАБОТА С ПРАЗДНИКАМИ")
    print("=" * 60)
    
    # Проверка новогодних праздников
    new_year = date(2024, 1, 1)
    print(f"1 января - праздник? {RussianHolidays.is_holiday(new_year)}")
    
    # Список всех праздников 2024 года
    holidays_2024 = RussianHolidays.get_holidays_in_year(2024)
    print(f"\nПраздники в 2024 году ({len(holidays_2024)} дней):")
    for holiday in holidays_2024[:5]:  # Первые 5
        print(f"  - {DateFormatter.format_russian(holiday)}")
    
    # Праздники в диапазоне
    start = date(2024, 1, 1)
    end = date(2024, 3, 31)
    holidays = RussianHolidays.get_holidays_in_range(start, end)
    print(f"\nПраздники с января по март 2024: {len(holidays)} дней")
    print()


def example_working_days():
    """Примеры работы с рабочими днями"""
    print("=" * 60)
    print("2. РАБОЧИЕ ДНИ")
    print("=" * 60)
    
    # Проверка рабочего дня
    monday = date(2024, 11, 18)  # Понедельник
    saturday = date(2024, 11, 16)  # Суббота
    
    print(f"18.11.2024 (Пн) - рабочий день? {is_working_day(monday)}")
    print(f"16.11.2024 (Сб) - рабочий день? {is_working_day(saturday)}")
    
    # Подсчет рабочих дней в месяце
    start = date(2024, 11, 1)
    end = date(2024, 11, 30)
    working = count_working_days(start, end)
    weekends = WorkingDays.count_weekends(start, end)
    
    print(f"\nНоябрь 2024:")
    print(f"  - Рабочих дней: {working}")
    print(f"  - Выходных дней: {weekends}")
    
    # Добавить 10 рабочих дней
    today = date(2024, 11, 18)
    future = WorkingDays.add_working_days(today, 10)
    print(f"\n18.11.2024 + 10 рабочих дней = {DateFormatter.format_russian(future)}")
    
    # Следующий рабочий день после пятницы
    friday = date(2024, 11, 15)
    next_working = WorkingDays.get_next_working_day(friday)
    print(f"После пятницы 15.11.2024 следующий рабочий день: {DateFormatter.format_russian(next_working)}")
    print()


def example_vacation_calculator():
    """Примеры расчета отпусков"""
    print("=" * 60)
    print("3. РАСЧЕТ ОТПУСКОВ")
    print("=" * 60)
    
    # Сотрудник работает 1 год
    hire_date = date(2023, 1, 1)
    earned = VacationCalculator.calculate_vacation_days_earned(hire_date, date(2024, 1, 1))
    print(f"Сотрудник работает с {DateFormatter.format_russian(hire_date)}")
    print(f"Заработал дней отпуска (за год): {earned}")
    
    # Сотрудник работает 6 месяцев
    hire_date_6m = date(2023, 7, 1)
    earned_6m = VacationCalculator.calculate_vacation_days_earned(hire_date_6m, date(2024, 1, 1))
    print(f"\nСотрудник работает с {DateFormatter.format_russian(hire_date_6m)}")
    print(f"Заработал дней отпуска (за 6 мес): {earned_6m}")
    
    # Детальный разбор периода отпуска
    vacation_start = date(2024, 7, 1)
    vacation_end = date(2024, 7, 14)
    breakdown = VacationCalculator.get_vacation_period_breakdown(vacation_start, vacation_end)
    
    print(f"\nПериод отпуска: {DateFormatter.format_date_range(vacation_start, vacation_end)}")
    print(f"  - Всего дней: {breakdown['total_days']}")
    print(f"  - Рабочих дней: {breakdown['working_days']}")
    print(f"  - Выходных: {breakdown['weekends']}")
    print(f"  - Праздников: {breakdown['holidays']}")
    
    # Валидация отпуска
    valid, error = VacationCalculator.is_vacation_valid(vacation_start, vacation_end)
    print(f"\nОтпуск валиден: {valid}")
    if error:
        print(f"Ошибка: {error}")
    
    # Расчет отпускных
    daily_salary = 2500  # средний дневной заработок
    allowance = VacationCalculator.calculate_vacation_allowance(
        daily_salary=daily_salary,
        vacation_days=14,
        start_date=vacation_start,
        end_date=vacation_end
    )
    print(f"\nОтпускные (14 дней × {daily_salary} руб): {allowance:,.2f} руб")
    print()


def example_date_formatter():
    """Примеры форматирования дат"""
    print("=" * 60)
    print("4. ФОРМАТИРОВАНИЕ ДАТ")
    print("=" * 60)
    
    test_date = date(2024, 3, 15)
    
    # Различные форматы
    print(f"Дата: {test_date}")
    print(f"По-русски: {DateFormatter.format_russian(test_date)}")
    print(f"С днем недели: {DateFormatter.format_with_weekday(test_date)}")
    print(f"Без года: {DateFormatter.format_russian(test_date, include_year=False)}")
    
    # Диапазон дат
    start = date(2024, 3, 1)
    end = date(2024, 3, 15)
    print(f"\nДиапазон: {DateFormatter.format_date_range(start, end)}")
    
    # Месяцы
    print(f"\nНазвания месяцев:")
    print(f"  - Именительный падеж: {DateFormatter.get_month_name(3, nominative=True)}")
    print(f"  - Родительный падеж: {DateFormatter.get_month_name(3, nominative=False)}")
    print()


def example_validators():
    """Примеры работы с валидаторами"""
    print("=" * 60)
    print("5. ВАЛИДАЦИЯ ДАННЫХ")
    print("=" * 60)
    
    # Валидация email
    print("Валидация email:")
    emails = [
        ("user@example.com", True),
        ("invalid.email", False),
        ("test@test.ru", True),
    ]
    
    for email, should_be_valid in emails:
        try:
            Validator.validate_email(email)
            print(f"  ✓ {email} - валиден")
        except ValidationError as e:
            print(f"  ✗ {email} - {e}")
    
    # Валидация пароля
    print("\nВалидация пароля:")
    passwords = [
        ("Pass123!", True),
        ("weak", False),
        ("NoNumber!", False),
        ("StrongP@ss123", True),
    ]
    
    for password, should_be_valid in passwords:
        try:
            Validator.validate_password(password)
            print(f"  ✓ '{password}' - валиден")
        except ValidationError as e:
            print(f"  ✗ '{password}' - {e}")
    
    # Валидация зарплаты
    print("\nВалидация зарплаты:")
    salaries = [
        (50000, True),
        (-1000, False),
        (15000000, False),
        (100000, True),
    ]
    
    for salary, should_be_valid in salaries:
        try:
            Validator.validate_salary(salary)
            print(f"  ✓ {salary} - валиден")
        except ValidationError as e:
            print(f"  ✗ {salary} - {e}")
    
    # Валидация даты рождения
    print("\nВалидация даты рождения:")
    birth_dates = [
        (date(1990, 5, 15), True),  # Взрослый
        (date(2010, 1, 1), False),  # Слишком молодой
        (date(2025, 1, 1), False),  # В будущем
        (date(1985, 12, 20), True),
    ]
    
    for birth_date, should_be_valid in birth_dates:
        try:
            Validator.validate_birth_date(birth_date)
            print(f"  ✓ {birth_date} - валиден")
        except ValidationError as e:
            print(f"  ✗ {birth_date} - {e}")
    print()


def example_employee_validation():
    """Пример валидации данных сотрудника"""
    print("=" * 60)
    print("6. ВАЛИДАЦИЯ СОТРУДНИКА")
    print("=" * 60)
    
    # Корректные данные
    valid_data = {
        'full_name': 'Иванов Иван Иванович',
        'email': 'ivanov@company.com',
        'employee_id': 'EMP-001',
        'hire_date': date(2024, 1, 15),
        'birth_date': date(1990, 5, 10),
        'salary': 80000,
        'phone': '+7 (999) 123-45-67'
    }
    
    print("Валидация корректных данных:")
    try:
        EmployeeValidator.validate_create(valid_data)
        print("  ✓ Все данные валидны!")
    except ValidationError as e:
        print(f"  ✗ Ошибка: {e}")
    
    # Некорректные данные
    invalid_data = {
        'full_name': 'AB',  # Слишком короткое имя
        'email': 'invalid-email',  # Неверный email
        'employee_id': 'E1',  # Слишком короткий ID
        'hire_date': date(2025, 12, 1),  # Дата в будущем
        'birth_date': date(2015, 1, 1),  # Слишком молодой
        'salary': -5000,  # Отрицательная зарплата
    }
    
    print("\nВалидация некорректных данных:")
    try:
        EmployeeValidator.validate_create(invalid_data)
        print("  ✓ Данные валидны")
    except ValidationError as e:
        print(f"  ✗ Ошибки валидации:\n    {e}")
    print()


def example_vacation_validation():
    """Пример валидации отпуска"""
    print("=" * 60)
    print("7. ВАЛИДАЦИЯ ОТПУСКА")
    print("=" * 60)
    
    # Корректный отпуск
    valid_vacation = {
        'start_date': date(2024, 7, 1),
        'end_date': date(2024, 7, 14),
        'type': 'paid'
    }
    
    print("Валидация корректного отпуска:")
    try:
        VacationValidator.validate_create(valid_vacation)
        print("  ✓ Отпуск валиден!")
    except ValidationError as e:
        print(f"  ✗ Ошибка: {e}")
    
    # Некорректный отпуск (конец раньше начала)
    invalid_vacation = {
        'start_date': date(2024, 7, 15),
        'end_date': date(2024, 7, 1),
        'type': 'paid'
    }
    
    print("\nВалидация некорректного отпуска:")
    try:
        VacationValidator.validate_create(invalid_vacation)
        print("  ✓ Отпуск валиден")
    except ValidationError as e:
        print(f"  ✗ Ошибка: {e}")
    print()


def example_real_world_scenario():
    """Реальный сценарий использования"""
    print("=" * 60)
    print("8. РЕАЛЬНЫЙ СЦЕНАРИЙ")
    print("=" * 60)
    print("Сотрудник подает заявление на отпуск")
    print()
    
    # Данные сотрудника
    employee_name = "Петров Петр Петрович"
    hire_date = date(2023, 1, 15)
    
    # Запрашиваемый отпуск
    vacation_start = date(2024, 8, 1)
    vacation_end = date(2024, 8, 14)
    
    print(f"Сотрудник: {employee_name}")
    print(f"Дата найма: {DateFormatter.format_russian(hire_date)}")
    print(f"Запрошен отпуск: {DateFormatter.format_date_range(vacation_start, vacation_end)}")
    print()
    
    # 1. Проверяем заработанные дни
    earned_days = VacationCalculator.calculate_vacation_days_earned(hire_date)
    print(f"1. Заработано дней отпуска: {earned_days}")
    
    # 2. Проверяем валидность периода
    is_valid, error = VacationCalculator.is_vacation_valid(vacation_start, vacation_end)
    print(f"2. Период отпуска валиден: {is_valid}")
    if error:
        print(f"   Ошибка: {error}")
        return
    
    # 3. Детальная информация о периоде
    breakdown = VacationCalculator.get_vacation_period_breakdown(vacation_start, vacation_end)
    print(f"3. Детали периода:")
    print(f"   - Всего дней: {breakdown['total_days']}")
    print(f"   - Рабочих дней: {breakdown['working_days']}")
    print(f"   - Выходных: {breakdown['weekends']}")
    print(f"   - Праздников: {breakdown['holidays']}")
    
    # 4. Проверяем, хватает ли дней
    if breakdown['total_days'] <= earned_days:
        print(f"4. ✓ Отпуск можно предоставить (хватает дней)")
        
        # 5. Рассчитываем отпускные
        daily_salary = 2800
        allowance = VacationCalculator.calculate_vacation_allowance(
            daily_salary=daily_salary,
            vacation_days=breakdown['total_days'],
            start_date=vacation_start,
            end_date=vacation_end
        )
        print(f"5. Сумма отпускных: {allowance:,.2f} руб")
    else:
        print(f"4. ✗ Недостаточно заработанных дней отпуска")
        print(f"   Запрошено: {breakdown['total_days']} дней")
        print(f"   Доступно: {earned_days} дней")
    print()


def main():
    """Запуск всех примеров"""
    print("\n" + "=" * 60)
    print("ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ SIMPLE HR v2.2")
    print("=" * 60)
    print()
    
    example_holidays()
    example_working_days()
    example_vacation_calculator()
    example_date_formatter()
    example_validators()
    example_employee_validation()
    example_vacation_validation()
    example_real_world_scenario()
    
    print("=" * 60)
    print("ВСЕ ПРИМЕРЫ ВЫПОЛНЕНЫ УСПЕШНО!")
    print("=" * 60)


if __name__ == "__main__":
    main()
