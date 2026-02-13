import pandas as pd

def fix_names(users: pd.DataFrame) -> pd.DataFrame:
    # Первый символ заглавный, остальные строчные (строго по условию)
    users['name'] = users['name'].str.capitalize()
    # Если нужно сделать заглавной первую букву каждого слова (Mary Ann -> Mary Ann):
    # users['name'] = users['name'].str.title()
    return users.sort_values(by='user_id')