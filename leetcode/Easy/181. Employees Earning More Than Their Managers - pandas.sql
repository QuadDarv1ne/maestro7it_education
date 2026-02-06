import pandas as pd

def find_employees(employee: pd.DataFrame) -> pd.DataFrame:
    # Объединяем таблицу саму с собой
    merged = employee.merge(
        employee,
        left_on='managerId',
        right_on='id',
        suffixes=('', '_manager')
    )
    
    # Фильтруем и возвращаем результат
    result = merged[merged['salary'] > merged['salary_manager']]
    return result[['name']].rename(columns={'name': 'Employee'})