import pandas as pd

def movie_rating(movies: pd.DataFrame, users: pd.DataFrame, movie_rating: pd.DataFrame) -> pd.DataFrame:
    """
    Возвращает DataFrame с двумя строками:
    - имя пользователя, оценившего больше всего фильмов
    - название фильма с наивысшим средним рейтингом в феврале 2020
    """
    
    # 1. Пользователь с максимальным количеством оценок
    user_counts = (
        movie_rating
        .groupby('user_id')
        .size()
        .reset_index(name='cnt')
        .merge(users, on='user_id', how='inner')
        .sort_values(['cnt', 'name'], ascending=[False, True])
    )
    # Берём первого пользователя (если данные есть)
    top_user = user_counts.iloc[0]['name'] if not user_counts.empty else None

    # 2. Фильм с наивысшим средним рейтингом в феврале 2020
    # Преобразуем дату, если ещё не datetime
    movie_rating['created_at'] = pd.to_datetime(movie_rating['created_at'])
    
    feb_ratings = movie_rating[
        (movie_rating['created_at'].dt.year == 2020) &
        (movie_rating['created_at'].dt.month == 2)
    ]
    
    if not feb_ratings.empty:
        movie_avg = (
            feb_ratings
            .groupby('movie_id')
            .agg(avg_rating=('rating', 'mean'))
            .reset_index()
            .merge(movies, on='movie_id', how='inner')
            .sort_values(['avg_rating', 'title'], ascending=[False, True])
        )
        top_movie = movie_avg.iloc[0]['title']
    else:
        top_movie = None

    # 3. Формируем итоговый DataFrame
    result = pd.DataFrame({'results': [top_user, top_movie]})
    return result