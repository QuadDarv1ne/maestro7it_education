import pandas as pd

def latest_login(logins: pd.DataFrame) -> pd.DataFrame:
    # 1. Оставляем только 2020 год
    df_2020 = logins[logins['time_stamp'].dt.year == 2020]
    
    # 2. Группируем по user_id → берём максимальный timestamp
    result = df_2020.groupby('user_id')['time_stamp'].max().reset_index()
    
    # 3. Переименовываем столбец как требуется
    result = result.rename(columns={'time_stamp': 'last_stamp'})
    
    return result