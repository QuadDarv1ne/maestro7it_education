import pandas as pd

def most_friends(request_accepted: pd.DataFrame) -> pd.DataFrame:
    # Создаем два DataFrame с связями в обоих направлениях
    df1 = request_accepted[['requester_id', 'accepter_id']].rename(
        columns={'requester_id': 'user_id', 'accepter_id': 'friend_id'}
    )
    df2 = request_accepted[['accepter_id', 'requester_id']].rename(
        columns={'accepter_id': 'user_id', 'requester_id': 'friend_id'}
    )
    
    # Объединяем и удаляем дубликаты связей
    df = pd.concat([df1, df2], ignore_index=True)
    df = df.drop_duplicates()
    
    # Считаем количество друзей для каждого пользователя
    friend_counts = df.groupby('user_id').size().reset_index(name='num')
    
    # Находим максимальное количество друзей
    max_num = friend_counts['num'].max()
    
    # Фильтруем пользователей с максимальным количеством
    result = friend_counts[friend_counts['num'] == max_num].rename(
        columns={'user_id': 'id'}
    )
    
    return result