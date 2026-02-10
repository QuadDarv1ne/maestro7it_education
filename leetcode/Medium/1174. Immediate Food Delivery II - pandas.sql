import pandas as pd

def immediate_delivery(delivery: pd.DataFrame) -> pd.DataFrame:
    # 1. Сортируем по customer_id и order_date, чтобы первый заказ был первым в группе
    delivery_sorted = delivery.sort_values(['customer_id', 'order_date'])

    # 2. Группируем по customer_id и берём первую запись (первый заказ)
    first_orders = delivery_sorted.groupby('customer_id', as_index=False).first()

    # 3. Проверяем, была ли доставка немедленной
    first_orders['is_immediate'] = (first_orders['order_date'] == first_orders['customer_pref_delivery_date']).astype(int)

    # 4. Вычисляем процент: среднее значение is_immediate * 100
    immediate_percentage = round(first_orders['is_immediate'].mean() * 100, 2)

    # 5. Возвращаем DataFrame с результатом, как требует формат LeetCode
    result_df = pd.DataFrame({'immediate_percentage': [immediate_percentage]})
    return result_df