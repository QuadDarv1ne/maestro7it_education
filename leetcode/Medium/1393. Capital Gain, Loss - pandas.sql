import pandas as pd

def capital_gain_loss(stocks: pd.DataFrame) -> pd.DataFrame:
    """
    Возвращает DataFrame с капитальной прибылью/убытком для каждой акции.
    
    Алгоритм:
        - Добавляем столбец signed_price:
            * для 'Sell' → +price
            * для 'Buy'  → -price
        - Группируем по stock_name и суммируем signed_price.
    
    Аргументы:
        stocks (pd.DataFrame): таблица с колонками 
            stock_name, operation, operation_day, price
        
    Возвращает:
        pd.DataFrame: колонки stock_name, capital_gain_loss
    """
    # Создаём копию, чтобы не менять исходный DataFrame
    df = stocks.copy()
    
    # Присваиваем знак в зависимости от операции
    df['signed_price'] = df.apply(
        lambda row: row['price'] if row['operation'] == 'Sell' else -row['price'], 
        axis=1
    )
    
    # Группировка и суммирование
    result = (
        df.groupby('stock_name', as_index=False)['signed_price']
          .sum()
          .rename(columns={'signed_price': 'capital_gain_loss'})
    )
    
    return result