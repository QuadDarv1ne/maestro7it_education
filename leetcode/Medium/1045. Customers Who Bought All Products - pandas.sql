import pandas as pd

def customers_who_bought_all_products(customer: pd.DataFrame, product: pd.DataFrame) -> pd.DataFrame:
    # Подсчитываем общее количество уникальных продуктов
    total_products = product['product_key'].nunique()
    # Группируем по покупателю и считаем уникальные купленные продукты
    customer_stats = customer.groupby('customer_id')['product_key'].nunique().reset_index()
    # Фильтруем покупателей, купивших все продукты
    result = customer_stats[customer_stats['product_key'] == total_products][['customer_id']]
    return result