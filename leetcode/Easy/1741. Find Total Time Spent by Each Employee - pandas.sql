import pandas as pd

def total_time(employees: pd.DataFrame) -> pd.DataFrame:
    # 1. Считаем общее время за день для каждого сотрудника
    result = employees.groupby(['event_day', 'emp_id']).apply(
        lambda x: (x['out_time'] - x['in_time']).sum()
    ).reset_index(name='total_time')
    
    # 2. Переименовываем колонку event_day -> day
    result.rename(columns={'event_day': 'day'}, inplace=True)
    
    # 3. Возвращаем в правильном порядке столбцов
    return result[['day', 'emp_id', 'total_time']]