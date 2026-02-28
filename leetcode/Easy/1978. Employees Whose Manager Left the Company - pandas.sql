import pandas as pd

def find_employees(employees: pd.DataFrame) -> pd.DataFrame:
    # Создаём множество всех employee_id для быстрой проверки
    all_employee_ids = set(employees['employee_id'])
    
    # Функция для проверки условий
    def condition(row):
        # Зарплата меньше 30000
        if row['salary'] >= 30000:
            return False
        # Есть менеджер
        if pd.isna(row['manager_id']):
            return False
        # Менеджер уволился (его нет в таблице)
        if row['manager_id'] not in all_employee_ids:
            return True
        return False
    
    # Применяем фильтрацию
    result = employees[employees.apply(condition, axis=1)]
    
    # Сортируем по employee_id и возвращаем только этот столбец
    return result[['employee_id']].sort_values('employee_id')