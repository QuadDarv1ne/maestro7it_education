import pandas as pd

def reformat_table(department: pd.DataFrame) -> pd.DataFrame:
    """
    Преобразует таблицу Department из длинного формата в широкий.
    Имя функции ДОЛЖНО быть 'reformat_table' для прохождения тестов LeetCode.
    """
    # 1. Создаем сводную таблицу (PIVOT)
    pivoted = department.pivot_table(
        index='id',
        columns='month',
        values='revenue',
        aggfunc='max'  # Можно использовать 'first', 'sum' - результат одинаков при уникальных данных
    )

    # 2. Переименовываем колонки, добавляя '_Revenue'
    pivoted.columns = [col + '_Revenue' for col in pivoted.columns]

    # 3. Определяем полный список месяцев
    all_months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    # 4. Добавляем отсутствующие месяцы как колонки с NaN
    for month in all_months:
        col_name = month + '_Revenue'
        if col_name not in pivoted.columns:
            pivoted[col_name] = pd.NA

    # 5. Сбрасываем индекс и задаем порядок колонок
    result = pivoted.reset_index()
    ordered_columns = ['id'] + [m + '_Revenue' for m in all_months]
    result = result[ordered_columns]

    return result