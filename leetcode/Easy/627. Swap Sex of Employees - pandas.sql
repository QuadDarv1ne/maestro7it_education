import pandas as pd

def swap_salary(salary: pd.DataFrame) -> pd.DataFrame:
    # Создаем сопоставление для замены значений
    salary['sex'] = salary['sex'].replace({'f': 'm', 'm': 'f'})
    return salary