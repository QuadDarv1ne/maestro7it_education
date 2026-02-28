import pandas as pd

def find_employees(employees: pd.DataFrame, salaries: pd.DataFrame) -> pd.DataFrame:
    # Делаем полное внешнее соединение (Full Outer Join)
    df = pd.merge(employees, salaries, on='employee_id', how='outer')
    
    # Фильтруем строки, где имя ИЛИ зарплата отсутствуют (NaN)
    # isna() проверяет значение на NULL/None
    missing_info = df[df['name'].isna() | df['salary'].isna()]
    
    # Выбираем только столбец employee_id и сортируем
    result = missing_info[['employee_id']].sort_values('employee_id')
    
    return result