import pandas as pd

def consecutive_numbers(logs: pd.DataFrame) -> pd.DataFrame:
    # Сортируем по id для последовательности
    logs = logs.sort_values('id')
    
    # Используем shift для получения предыдущих значений
    logs['prev_num'] = logs['num'].shift(1)
    logs['prev_num2'] = logs['num'].shift(2)
    logs['prev_id'] = logs['id'].shift(1)
    logs['prev_id2'] = logs['id'].shift(2)
    
    # Фильтруем строки где:
    # 1. Текущее число равно предыдущему и пред-предыдущему
    # 2. ID идут последовательно (id-1 = prev_id, id-2 = prev_id2)
    consecutive_mask = (
        (logs['num'] == logs['prev_num']) &
        (logs['num'] == logs['prev_num2']) &
        (logs['id'] == logs['prev_id'] + 1) &
        (logs['prev_id'] == logs['prev_id2'] + 1)
    )
    
    # Получаем уникальные числа
    result_df = logs.loc[consecutive_mask, ['num']].drop_duplicates()
    result_df.columns = ['ConsecutiveNums']
    
    return result_df