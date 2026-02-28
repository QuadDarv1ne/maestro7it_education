import pandas as pd

def calculate_special_bonus(employees: pd.DataFrame) -> pd.DataFrame:
    # Создаём столбец bonus с помощью условного присваивания
    employees['bonus'] = employees.apply(
        lambda row: row['salary'] 
        if row['employee_id'] % 2 != 0 and not row['name'].startswith('M') 
        else 0,
        axis=1
    )
    
    # Сортируем по employee_id и возвращаем нужные столбцы
    return employees[['employee_id', 'bonus']].sort_values('employee_id')