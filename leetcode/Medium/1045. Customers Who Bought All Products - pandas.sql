import pandas as pd

def find_customers(customer: pd.DataFrame, product: pd.DataFrame) -> pd.DataFrame:
    # 1. Находим общее количество уникальных продуктов в каталоге
    total_products = product['product_key'].nunique()
    
    # 2. Для каждого покупателя считаем, сколько уникальных продуктов он купил
    # Группируем по 'customer_id', применяем nunique() к 'product_key'
    customer_stats = customer.groupby('customer_id')['product_key'].nunique().reset_index()
    
    # 3. Оставляем только тех покупателей, у которых это число равно общему количеству продуктов
    result = customer_stats[customer_stats['product_key'] == total_products][['customer_id']]
    
    return result