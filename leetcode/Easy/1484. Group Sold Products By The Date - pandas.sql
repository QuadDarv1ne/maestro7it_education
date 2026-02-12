import pandas as pd

def categorize_products(activities: pd.DataFrame) -> pd.DataFrame:
    """
    Возвращает DataFrame с количеством уникальных товаров и их списком для каждой даты.
    
    Алгоритм:
        - Удаляем дубликаты (sell_date, product).
        - Группируем по дате:
            * count() -> num_sold
            * apply(sorted).str.join(',') -> products
        - Сортируем по sell_date.
    """
    # Убираем дубликаты строк (дата + товар)
    unique_products = activities.drop_duplicates(subset=['sell_date', 'product'])
    
    # Группировка и аггрегация
    result = unique_products.groupby('sell_date').agg(
        num_sold=('product', 'count'),
        products=('product', lambda x: ','.join(sorted(x)))
    ).reset_index()
    
    # Сортировка по дате
    result = result.sort_values('sell_date').reset_index(drop=True)
    
    return result[['sell_date', 'num_sold', 'products']]