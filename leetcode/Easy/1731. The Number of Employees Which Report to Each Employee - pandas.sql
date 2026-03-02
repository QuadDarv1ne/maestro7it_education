import pandas as pd
import numpy as np

def count_employees(employees: pd.DataFrame) -> pd.DataFrame:
    """
    Возвращает список менеджеров с количеством прямых подчинённых
    и их средним возрастом, округлённым до ближайшего целого.
    Округление выполняется по правилу "half up" (арифметическое округление).

    Параметры:
    employees (pd.DataFrame): таблица с колонками employee_id, name, reports_to, age.

    Возвращает:
    pd.DataFrame: колонки employee_id, name, reports_count, average_age.
    """
    # Самосоединение таблицы: менеджер (employee_id) соединяется со своими подчинёнными (reports_to)
    merged = employees.merge(
        employees,
        how='inner',
        left_on='employee_id',
        right_on='reports_to',
        suffixes=('_manager', '_report')
    )
    
    # Группировка по данным менеджера и агрегация
    result = merged.groupby(['employee_id_manager', 'name_manager']).agg(
        reports_count=('employee_id_report', 'count'),
        average_age=('age_report', 'mean')
    ).reset_index()
    
    # Переименование колонок в соответствии с требуемым выводом
    result.columns = ['employee_id', 'name', 'reports_count', 'average_age']
    
    # Округление до ближайшего целого (half up)
    # Используем формулу floor(x + 0.5) для положительных чисел
    result['average_age'] = np.floor(result['average_age'] + 0.5).astype(int)
    
    # Сортировка по employee_id
    result = result.sort_values(by='employee_id').reset_index(drop=True)
    
    return result