import pandas as pd

def actors_and_directors(actor_director: pd.DataFrame) -> pd.DataFrame:
    # Группируем по actor_id и director_id, подсчитываем количество записей
    grouped = actor_director.groupby(['actor_id', 'director_id']).size().reset_index(name='cooperation_count')
    # Фильтруем пары с 3 и более сотрудничествами
    result = grouped[grouped['cooperation_count'] >= 3][['actor_id', 'director_id']]
    return result