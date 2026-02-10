import pandas as pd

def restaurant_growth(customer: pd.DataFrame) -> pd.DataFrame:
    """
    Вычисляет скользящее среднее выручки ресторана за 7-дневное окно.
    
    Алгоритм:
    1. Агрегируем данные по дням, суммируя выручку.
    2. Убеждаемся, что данные охватывают все дни без пропусков (резервируем индекс дат).
    3. Рассчитываем скользящую сумму и среднее за 7 дней.
    4. Отбираем строки с полным 7-дневным окном (начиная с 7-го дня).
    
    Возвращает:
        DataFrame с колонками ['visited_on', 'amount', 'average_amount']
    """
    # Преобразуем даты в формат datetime, если это ещё не сделано
    customer['visited_on'] = pd.to_datetime(customer['visited_on'])
    
    # 1. Агрегируем выручку по дням (может быть несколько посетителей в один день)
    daily_revenue = customer.groupby('visited_on', as_index=False)['amount'].sum()
    
    # 2. Убеждаемся, что даты идут подряд (без пропусков).
    # Создаём полный временной ряд от минимальной до максимальной даты в данных.
    # Заполняем пропущенные дни значением 0 (т.к. по условию "не менее одного клиента в день",
    # но данные примера не содержат явных пропусков).
    date_range = pd.date_range(
        start=daily_revenue['visited_on'].min(),
        end=daily_revenue['visited_on'].max(),
        freq='D'
    )
    
    # Преобразуем в DataFrame и присоединяем фактические данные.
    # Это гарантирует, что все даты будут в индексе для корректного расчета скользящего окна.
    full_dates = pd.DataFrame({'visited_on': date_range})
    daily_revenue_full = pd.merge(full_dates, daily_revenue, on='visited_on', how='left')
    daily_revenue_full['amount'] = daily_revenue_full['amount'].fillna(0)  # если день без данных - выручка 0
    
    # Сортируем по дате (хотя уже отсортировано, но для надёжности)
    daily_revenue_full = daily_revenue_full.sort_values('visited_on')
    
    # 3. Вычисляем скользящую сумму за 7 дней (текущий день + 6 предыдущих)
    # Используем min_periods=7, чтобы результат появлялся только когда есть полное окно.
    daily_revenue_full['rolling_sum'] = daily_revenue_full['amount'].rolling(
        window=7,           # размер окна - 7 дней
        min_periods=7       # минимальное количество дней для расчета
    ).sum()
    
    # 4. Вычисляем скользящее среднее и округляем до 2 знаков
    daily_revenue_full['average_amount'] = (daily_revenue_full['rolling_sum'] / 7).round(2)
    
    # 5. Переименовываем колонку rolling_sum в amount для итогового результата
    # и выбираем только строки, где скользящая сумма не NaN (т.е. начиная с 7-го дня)
    result = daily_revenue_full.dropna(subset=['rolling_sum']).copy()
    result['amount'] = result['rolling_sum'].astype(int)  # по примеру, сумма - целое число
    
    # 6. Форматируем дату обратно в строку (как в примере) и выбираем нужные колонки
    result['visited_on'] = result['visited_on'].dt.strftime('%Y-%m-%d')
    final_result = result[['visited_on', 'amount', 'average_amount']]
    
    return final_result