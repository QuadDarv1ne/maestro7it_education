import pandas as pd

def list_products(products: pd.DataFrame, orders: pd.DataFrame) -> pd.DataFrame:
    """
    Находит продукты, заказанные в феврале 2020 года в количестве не менее 100 единиц.
    
    Параметры:
    ----------
    products : pd.DataFrame
        DataFrame с колонками ['product_id', 'product_name']
    
    orders : pd.DataFrame
        DataFrame с колонками ['order_id', 'product_id', 'order_date', 'unit']
    
    Возвращает:
    ----------
    pd.DataFrame
        DataFrame с колонками ['product_name', 'unit'], отсортированный по 
        количеству (unit) по убыванию, затем по названию продукта
    """
    
    # 1. Преобразуем order_date в тип datetime, если это ещё не сделано
    orders['order_date'] = pd.to_datetime(orders['order_date'])
    
    # 2. Фильтруем заказы за февраль 2020 года
    # Создаём маску для фильтрации: год = 2020 и месяц = 2 (февраль)
    feb_2020_mask = (orders['order_date'].dt.year == 2020) & \
                    (orders['order_date'].dt.month == 2)
    
    # Применяем фильтр
    feb_orders = orders[feb_2020_mask].copy()
    
    # 3. Объединяем отфильтрованные заказы с таблицей продуктов
    merged_df = pd.merge(
        feb_orders,
        products,
        on='product_id',
        how='inner'
    )
    
    # 4. Группируем по product_id и product_name, суммируем количество
    grouped_df = merged_df.groupby(['product_id', 'product_name'], as_index=False)['unit'].sum()
    
    # 5. Фильтруем продукты с суммой unit >= 100
    filtered_df = grouped_df[grouped_df['unit'] >= 100].copy()
    
    # 6. Сортируем результат: сначала по unit (по убыванию), затем по product_name
    result_df = filtered_df.sort_values(
        by=['unit', 'product_name'], 
        ascending=[False, True]
    ).reset_index(drop=True)
    
    # 7. Выбираем только нужные колонки в правильном порядке
    return result_df[['product_name', 'unit']]