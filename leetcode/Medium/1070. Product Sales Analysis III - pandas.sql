import pandas as pd

def sales_analysis(sales: pd.DataFrame) -> pd.DataFrame:
    # Находим первый год продаж для каждого продукта
    first_years = sales.groupby('product_id')['year'].min().reset_index()
    
    # Объединяем с исходной таблицей, чтобы получить quantity и price
    result = pd.merge(
        first_years, 
        sales, 
        on=['product_id', 'year'], 
        how='left'
    )
    
    # Переименовываем столбец и выбираем нужные поля
    result = result.rename(columns={'year': 'first_year'})
    result = result[['product_id', 'first_year', 'quantity', 'price']]
    
    return result