import pandas as pd

def average_selling_price(prices: pd.DataFrame, units_sold: pd.DataFrame) -> pd.DataFrame:
    """
    Вычисляет среднюю цену продажи для каждого товара.
    
    Алгоритм:
    1. Объединяем таблицы цен и продаж по product_id
    2. Фильтруем строки, где дата покупки попадает в период действия цены
    3. Вычисляем выручку для каждой продажи
    4. Агрегируем данные по товарам
    5. Рассчитываем среднюю цену с обработкой нулевых значений
    
    Возвращает:
        DataFrame с колонками ['product_id', 'average_price']
    """
    
    # 1. Проверяем и конвертируем даты при необходимости
    # Если даты не в формате datetime, преобразуем их
    date_columns = ['start_date', 'end_date', 'purchase_date']
    
    for col in ['start_date', 'end_date']:
        if col in prices.columns and not pd.api.types.is_datetime64_any_dtype(prices[col]):
            prices[col] = pd.to_datetime(prices[col])
    
    if 'purchase_date' in units_sold.columns and not pd.api.types.is_datetime64_any_dtype(units_sold['purchase_date']):
        units_sold['purchase_date'] = pd.to_datetime(units_sold['purchase_date'])
    
    # 2. Объединяем таблицы
    # LEFT JOIN: оставляем все товары из prices, даже если у них нет продаж
    merged_df = pd.merge(
        prices,
        units_sold,
        on='product_id',
        how='left',
        suffixes=('_price', '_sold')
    )
    
    # 3. Создаем маску для фильтрации
    # Условие 1: purchase_date между start_date и end_date (включительно)
    # Условие 2: purchase_date является NaN (товары без продаж)
    condition = (
        # Проверяем, что purchase_date не NaN и находится в диапазоне
        merged_df['purchase_date'].notna() &
        (merged_df['purchase_date'] >= merged_df['start_date']) &
        (merged_df['purchase_date'] <= merged_df['end_date'])
    ) | (
        # ИЛИ purchase_date является NaN (товары без продаж)
        merged_df['purchase_date'].isna()
    )
    
    # 4. Применяем фильтр
    filtered_df = merged_df[condition].copy()
    
    # 5. Вычисляем выручку от каждой продажи
    # units * price, но только для строк с продажами
    filtered_df['revenue'] = filtered_df['units'] * filtered_df['price']
    
    # 6. Группируем по product_id и вычисляем агрегированные значения
    result_df = filtered_df.groupby('product_id', as_index=False).agg(
        total_revenue=('revenue', 'sum'),   # Сумма выручки
        total_units=('units', 'sum')        # Сумма проданных единиц
    )
    
    # 7. Вычисляем среднюю цену
    # Избегаем деления на 0: если total_units = 0 или NaN, устанавливаем 0
    result_df['average_price'] = result_df.apply(
        lambda row: (
            round(row['total_revenue'] / row['total_units'], 2)
            if pd.notna(row['total_units']) and row['total_units'] != 0
            else 0.0
        ),
        axis=1
    )
    
    # 8. Возвращаем результат в требуемом формате
    return result_df[['product_id', 'average_price']]