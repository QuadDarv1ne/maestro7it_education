import pandas as pd

def last_passenger(queue: pd.DataFrame) -> pd.DataFrame:
    """
    Возвращает имя последнего пассажира, который может поместиться в автобус без превышения лимита в 1000 кг.
    
    Параметры:
    ----------
    queue : pd.DataFrame
        DataFrame с пассажирами, содержащий столбцы:
        - person_id: идентификатор пассажира
        - person_name: имя пассажира
        - weight: вес пассажира в кг
        - turn: порядковый номер в очереди на посадку
    
    Возвращает:
    ----------
    pd.DataFrame
        DataFrame с одним столбцом 'person_name', содержащий имя последнего пассажира,
        который может сесть в автобус. Если никто не может сесть, возвращает пустой DataFrame.
    
    Алгоритм:
    ---------
    1. Сортировка пассажиров по порядку посадки (turn)
    2. Вычисление накопительной суммы весов (кумулятивный вес)
    3. Фильтрация пассажиров с кумулятивным весом ≤ 1000 кг
    4. Выбор последнего пассажира из отфильтрованного списка
    
    Пример:
    -------
    Входные данные:
        person_id  person_name  weight  turn
        1          Alice        250     1
        2          Alex         350     2
        3          John Cena    400     3
        4          Marie        200     4
    
    Результат:
        person_name
        0   John Cena
    
    Объяснение:
    - Alice (250 кг): сумма = 250
    - Alex (350 кг): сумма = 600
    - John Cena (400 кг): сумма = 1000
    - Marie (200 кг): сумма = 1200 (превышает лимит)
    """
    # Сортируем по порядку посадки
    df_sorted = queue.sort_values('turn')
    
    # Вычисляем кумулятивную сумму весов
    df_sorted['cumulative_weight'] = df_sorted['weight'].cumsum()
    
    # Фильтруем пассажиров, которые могут сесть (не превышают 1000 кг)
    valid_passengers = df_sorted[df_sorted['cumulative_weight'] <= 1000]
    
    # Если нет подходящих пассажиров, возвращаем пустой DataFrame
    if valid_passengers.empty:
        return pd.DataFrame(columns=['person_name'])
    
    # Берем последнего пассажира (с максимальным номером очереди)
    last_passenger_row = valid_passengers.iloc[-1]
    
    # Возвращаем DataFrame с именем пассажира
    return pd.DataFrame({'person_name': [last_passenger_row['person_name']]})