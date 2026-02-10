import pandas as pd

def immediate_food_delivery(delivery: pd.DataFrame) -> pd.DataFrame:
    """
    Вычисляет процент немедленных доставок для первых заказов клиентов.
    Имя функции должно быть 'immediate_food_delivery' для прохождения тестов LeetCode.
    """
    # 1. Сортируем по клиенту и дате заказа
    delivery_sorted = delivery.sort_values(['customer_id', 'order_date'])

    # 2. Группируем по клиенту и берём первый заказ
    first_orders = delivery_sorted.groupby('customer_id', as_index=False).first()

    # 3. Определяем, была ли доставка немедленной (даты совпадают)
    first_orders['is_immediate'] = (
        first_orders['order_date'] == first_orders['customer_pref_delivery_date']
    ).astype(int)

    # 4. Вычисляем процент (среднее значение * 100) и округляем до 2 знаков
    immediate_percentage = round(first_orders['is_immediate'].mean() * 100, 2)

    # 5. Возвращаем результат в формате DataFrame, как требует LeetCode
    result_df = pd.DataFrame({'immediate_percentage': [immediate_percentage]})
    return result_df