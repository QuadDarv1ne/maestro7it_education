import pandas as pd

def price_at_given_date(products: pd.DataFrame) -> pd.DataFrame:
    target_date = pd.to_datetime('2019-08-16')
    
    # 1. Фильтруем записи до целевой даты включительно
    df_before = products[pd.to_datetime(products['change_date']) <= target_date]
    
    # 2. Для каждого товара находим последнее изменение (макс. дату)
    if not df_before.empty:
        # Находим последнюю дату для каждого товара
        last_dates = df_before.groupby('product_id')['change_date'].max().reset_index()
        # Присоединяем цену по последней дате
        latest_prices = pd.merge(last_dates, products, on=['product_id', 'change_date'])
        latest_prices = latest_prices[['product_id', 'new_price']].rename(columns={'new_price': 'price'})
    else:
        latest_prices = pd.DataFrame(columns=['product_id', 'price'])
    
    # 3. Все уникальные ID товаров
    all_products = pd.DataFrame({'product_id': products['product_id'].unique()})
    
    # 4. LEFT JOIN всех товаров с последними ценами
    result = pd.merge(all_products, latest_prices, on='product_id', how='left')
    
    # 5. Заменяем NaN на 10 (товары без изменений до даты)
    result['price'] = result['price'].fillna(10).astype(int)
    
    return result