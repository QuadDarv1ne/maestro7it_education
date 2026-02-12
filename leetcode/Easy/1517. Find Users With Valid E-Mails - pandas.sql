import pandas as pd

def valid_emails(users: pd.DataFrame) -> pd.DataFrame:
    """
    Возвращает пользователей с валидными email-адресами.
    Валидный email: <префикс>@leetcode.com, где префикс:
        - начинается с буквы
        - содержит только буквы, цифры, '_', '.', '-'
    """
    # Регулярное выражение (аналогично MySQL)
    valid_pattern = r'^[A-Za-z][A-Za-z0-9_.-]*@leetcode\.com$'
    
    # Применяем фильтр через str.match
    valid_mask = users['mail'].str.match(valid_pattern, na=False)
    
    return users[valid_mask]