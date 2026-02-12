import pandas as pd

def top_travellers(users: pd.DataFrame, rides: pd.DataFrame) -> pd.DataFrame:
    """
    Возвращает DataFrame с именами пользователей и общей дистанцией.
    
    Алгоритм:
        - Группируем поездки по user_id, суммируем distance.
        - Делаем LEFT JOIN c users (все пользователи).
        - Заполняем NaN расстояния нулями.
        - Сортируем по travelled_distance DESC, name ASC.
    """
    # Суммируем расстояния по пользователям
    ride_distances = rides.groupby('user_id', as_index=False)['distance'].sum()
    
    # LEFT JOIN (все пользователи) + заполнение NaN нулями
    result = users.merge(ride_distances, left_on='id', right_on='user_id', how='left')
    result['distance'] = result['distance'].fillna(0)
    
    # Формируем итоговые колонки и сортируем
    result = result[['name', 'distance']].rename(columns={'distance': 'travelled_distance'})
    result = result.sort_values(
        by=['travelled_distance', 'name'], 
        ascending=[False, True]
    ).reset_index(drop=True)
    
    return result