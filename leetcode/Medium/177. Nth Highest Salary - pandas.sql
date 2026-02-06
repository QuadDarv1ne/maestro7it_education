import pandas as pd

def nth_highest_salary(employee: pd.DataFrame, N: int) -> pd.DataFrame:
    # Обработка некорректного N
    if N <= 0:
        return pd.DataFrame({f'getNthHighestSalary({N})': [None]})
    
    # Получаем уникальные зарплаты в порядке убывания
    distinct_salaries = employee['salary'].drop_duplicates().sort_values(ascending=False)
    
    # Проверяем, существует ли N-ая зарплата
    if N > len(distinct_salaries):
        nth_salary = None
    else:
        nth_salary = distinct_salaries.iloc[N-1]
    
    # Возвращаем DataFrame с правильным форматом
    return pd.DataFrame({f'getNthHighestSalary({N})': [nth_salary]})