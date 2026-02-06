import pandas as pd

def order_scores(scores: pd.DataFrame) -> pd.DataFrame:
    # Сортируем оценки по убыванию
    scores_sorted = scores.sort_values('score', ascending=False)
    
    # Вычисляем dense rank
    scores_sorted['rank'] = scores_sorted['score'].rank(method='dense', ascending=False).astype(int)
    
    return scores_sorted[['score', 'rank']]