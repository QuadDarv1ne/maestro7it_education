import pandas as pd

def sales_analysis(product: pd.DataFrame, sales: pd.DataFrame) -> pd.DataFrame:
    # Объединяем таблицы
    merged_df = pd.merge(product, sales, on='product_id')
    
    # Группируем по продукту, вычисляем min и max дату продаж
    grouped = merged_df.groupby(['product_id', 'product_name']).agg(
        min_date=('sale_date', 'min'),
        max_date=('sale_date', 'max')
    ).reset_index()
    
    # Фильтруем: обе даты должны быть в пределах весны 2019
    result = grouped[
        (grouped['min_date'] >= '2019-01-01') & 
        (grouped['max_date'] <= '2019-03-31')
    ]
    
    return result[['product_id', 'product_name']]