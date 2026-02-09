import pandas as pd

def trips_and_users(trips: pd.DataFrame, users: pd.DataFrame) -> pd.DataFrame:
    # Получаем ID незабаненных пользователей
    unbanned_ids = set(users[users['banned'] == 'No']['users_id'])
    
    # Фильтруем поездки
    valid_trips = trips[
        (trips['client_id'].isin(unbanned_ids)) &
        (trips['driver_id'].isin(unbanned_ids)) &
        (trips['request_at'] >= '2013-10-01') &
        (trips['request_at'] <= '2013-10-03')
    ].copy()
    
    # Определяем отмененные поездки
    valid_trips['is_cancelled'] = valid_trips['status'].isin(['cancelled_by_driver', 'cancelled_by_client']).astype(int)
    
    # Группируем по дням
    grouped = valid_trips.groupby('request_at').agg(
        cancelled_count=('is_cancelled', 'sum'),
        total_count=('id', 'count')
    ).reset_index()
    
    # Вычисляем cancellation rate
    grouped['Cancellation Rate'] = (grouped['cancelled_count'] / grouped['total_count']).round(2)
    
    # Форматируем результат
    result = grouped[['request_at', 'Cancellation Rate']].rename(columns={'request_at': 'Day'})
    
    return result