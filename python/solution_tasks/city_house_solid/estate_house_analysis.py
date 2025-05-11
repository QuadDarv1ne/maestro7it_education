import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta

# Инициализация генератора данных
fake = Faker()
np.random.seed(42)

# Создание датафрейма с 50 строками
data = {
    'date': [datetime(2023, 1, 1) + timedelta(days=np.random.randint(0, 365)) for _ in range(50)],
    'area': [fake.city() for _ in range(50)],
    'average_price': np.random.randint(30000, 120000, 50),
    'code': ['E' + str(np.random.randint(10000000, 99999999)) for _ in range(50)],
    'houses_add': np.random.randint(0, 20, 50),
    'no_of_citness': np.random.choice([np.nan, np.random.randint(1000, 50000)], 50),
    'borough_flag': np.random.choice(['↑', '↓', np.nan], 50, p=[0.4, 0.4, 0.2]),
    'house_solid': np.random.randint(0, 100, 50)
}

df = pd.DataFrame(data)

# Добавление пропущенных значений в несколько столбцов
for col in ['houses_add', 'no_of_citness', 'house_solid']:
    df.loc[np.random.choice(df.index, 10), col] = np.nan

# Пример данных
print("Первые 5 строк данных:")
display(df.head())

print("\nСтатистика по числовым столбцам:")
display(df.describe())

print("\nПроверка фильтрации (average_price > 50000):")
print(f"Подходящих строк: {len(df[df['average_price'] > 50000])}")
