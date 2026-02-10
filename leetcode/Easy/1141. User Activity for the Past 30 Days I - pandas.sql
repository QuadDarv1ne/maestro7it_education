import pandas as pd

def user_activity(activity: pd.DataFrame) -> pd.DataFrame:
    # Преобразуем activity_date в datetime, если ещё не
    activity['activity_date'] = pd.to_datetime(activity['activity_date'])
    
    # Определяем границы периода
    end_date = pd.to_datetime('2019-07-27')
    start_date = end_date - pd.Timedelta(days=29)
    
    # Фильтруем записи за последние 30 дней
    filtered = activity[(activity['activity_date'] >= start_date) & 
                        (activity['activity_date'] <= end_date)]
    
    # Группируем по дате, считаем уникальных пользователей
    result = filtered.groupby('activity_date')['user_id'].nunique().reset_index()
    result.columns = ['day', 'active_users']
    
    # Сортируем по дате (по возрастанию)
    result = result.sort_values('day')
    
    return result