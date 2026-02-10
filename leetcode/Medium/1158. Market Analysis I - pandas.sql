import pandas as pd

def market_analysis(users: pd.DataFrame, orders: pd.DataFrame) -> pd.DataFrame:
    # 1. Фильтруем заказы только за 2019 год
    orders_2019 = orders[pd.to_datetime(orders['order_date']).dt.year == 2019]

    # 2. Делаем левое соединение (LEFT JOIN) Users с отфильтрованными заказами
    merged_df = pd.merge(
        users,
        orders_2019,
        how='left',
        left_on='user_id',
        right_on='buyer_id'
    )

    # 3. Группируем по пользователю и считаем заказы
    result = merged_df.groupby(['user_id', 'join_date'], as_index=False).agg(
        orders_in_2019=('order_id', 'count')  # count автоматически проигнорирует NaN для пользователей без заказов
    )

    # 4. Переименовываем колонки как в условии задачи
    result = result.rename(columns={'user_id': 'buyer_id'})

    return result