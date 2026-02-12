import pandas as pd

def account_summary(users: pd.DataFrame, transactions: pd.DataFrame) -> pd.DataFrame:
    """
    Возвращает имена и баланс пользователей с балансом > 10000.
    """
    # 1. Группируем транзакции по счету, суммируем amount
    balance_df = transactions.groupby('account', as_index=False)['amount'].sum()
    
    # 2. Соединяем с пользователями (LEFT JOIN, чтобы учесть всех)
    merged = users.merge(balance_df, on='account', how='left')
    
    # 3. Заполняем NaN (счета без транзакций) нулями
    merged['amount'] = merged['amount'].fillna(0)
    
    # 4. Переименовываем столбец и фильтруем по балансу
    merged = merged.rename(columns={'amount': 'balance'})
    result = merged[merged['balance'] > 10000]
    
    # 5. Возвращаем только нужные колонки
    return result[['name', 'balance']]