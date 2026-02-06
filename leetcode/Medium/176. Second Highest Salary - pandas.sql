import pandas as pd
import numpy as np
from typing import Optional

def second_highest_salary(employee: pd.DataFrame) -> pd.DataFrame:
    """
    Возвращает вторую максимальную зарплату из DataFrame.
    
    Args:
        employee: DataFrame с колонками ['id', 'salary']
        
    Returns:
        DataFrame с одной колонкой ['SecondHighestSalary']
    """
    # Проверяем, есть ли данные
    if employee.empty or employee['salary'].empty:
        return pd.DataFrame({'SecondHighestSalary': [np.nan]})
    
    # Удаляем дубликаты зарплат
    unique_salaries = employee['salary'].drop_duplicates()
    
    # Если меньше 2 уникальных зарплат, возвращаем NaN
    if len(unique_salaries) < 2:
        return pd.DataFrame({'SecondHighestSalary': [np.nan]})
    
    # Сортируем по убыванию и берем вторую зарплату
    second_highest = unique_salaries.nlargest(2).iloc[1]
    
    return pd.DataFrame({'SecondHighestSalary': [second_highest]})


def second_highest_salary_optimized(employee: pd.DataFrame) -> pd.DataFrame:
    """
    Оптимизированная версия с использованием nlargest.
    """
    # Получаем две наибольшие уникальные зарплаты
    top_2 = employee['salary'].drop_duplicates().nlargest(2)
    
    # Если есть вторая зарплата, возвращаем ее, иначе NaN
    second_highest = top_2.iloc[1] if len(top_2) > 1 else np.nan
    
    return pd.DataFrame({'SecondHighestSalary': [second_highest]})


# Пример использования
if __name__ == "__main__":
    # Тестовые данные
    test_cases = [
        pd.DataFrame({'id': [1, 2, 3], 'salary': [100, 200, 300]}),  # Обычный случай
        pd.DataFrame({'id': [1, 2, 3], 'salary': [100, 100, 200]}),  # Есть дубликаты
        pd.DataFrame({'id': [1], 'salary': [100]}),  # Только одна зарплата
        pd.DataFrame({'id': [], 'salary': []}),  # Пустой DataFrame
        pd.DataFrame({'id': [1, 2, 3], 'salary': [100, 100, 100]}),  # Все зарплаты одинаковые
    ]
    
    for i, df in enumerate(test_cases, 1):
        print(f"Тест {i}:")
        print(f"Данные:\n{df}")
        result = second_highest_salary(df)
        print(f"Результат: {result.iloc[0, 0]}")
        print("-" * 40)


# Функция для LeetCode
class Solution:
    def second_highest_salary(self, employee: pd.DataFrame) -> pd.DataFrame:
        return second_highest_salary_optimized(employee)