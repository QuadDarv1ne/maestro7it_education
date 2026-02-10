import pandas as pd

def gameplay_analysis(activity: pd.DataFrame) -> pd.DataFrame:
    # Найти первую дату входа для каждого игрока
    first_login = activity.groupby('player_id')['event_date'].min().reset_index()
    first_login.columns = ['player_id', 'first_login_date']
    
    # Добавить следующий день
    first_login['next_day'] = first_login['first_login_date'] + pd.Timedelta(days=1)
    
    # Присоединить к основной таблице
    merged = activity.merge(first_login, on='player_id')
    
    # Найти игроков, которые вернулись на следующий день
    consecutive_players = merged[merged['event_date'] == merged['next_day']]['player_id'].nunique()
    
    # Общее количество игроков
    total_players = activity['player_id'].nunique()
    
    # Вычислить долю
    fraction = round(consecutive_players / total_players, 2)
    
    return pd.DataFrame({'fraction': [fraction]})