import pandas as pd

def find_investments(insurance: pd.DataFrame) -> pd.DataFrame:
    # Найти количество одинаковых tiv_2015
    tiv_2015_counts = insurance.groupby('tiv_2015')['pid'].transform('count')
    
    # Найти количество одинаковых локаций
    location_counts = insurance.groupby(['lat', 'lon'])['pid'].transform('count')
    
    # Фильтровать
    filtered = insurance[
        (tiv_2015_counts > 1) & (location_counts == 1)
    ]
    
    # Вычислить сумму
    total = filtered['tiv_2016'].sum()
    
    return pd.DataFrame({'tiv_2016': [round(total, 2)]})