import pandas as pd

def rearrange_products_table(products: pd.DataFrame) -> pd.DataFrame:
    return pd.melt(
        products,
        id_vars=['product_id'],        # столбец, который остаётся неизменным
        var_name='store',             # новое имя для столбца с названиями магазинов
        value_name='price'           # новое имя для столбца с ценами
    ).dropna(subset=['price'])       # удаляем строки, где цена = NULL