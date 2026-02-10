import pandas as pd

def exchange_seats(seat: pd.DataFrame) -> pd.DataFrame:
    df = seat.sort_values('id').reset_index(drop=True)
    
    # Создаем столбцы со сдвинутыми id
    df['prev_id'] = df['id'].shift(1)  # Сдвиг назад
    df['next_id'] = df['id'].shift(-1) # Сдвиг вперед
    
    # Применяем логику замены
    df['new_id'] = df['id']  # По умолчанию оставляем тот же id
    # Для нечетных id (кроме последнего) берем следующий id
    df.loc[(df['id'] % 2 == 1) & (df['next_id'].notna()), 'new_id'] = df['next_id']
    # Для четных id берем предыдущий id
    df.loc[df['id'] % 2 == 0, 'new_id'] = df['prev_id']
    
    # Заменяем id на новые значения и сортируем
    df['id'] = df['new_id']
    return df[['id', 'student']].sort_values('id')