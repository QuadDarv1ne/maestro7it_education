import pandas as pd

def biggest_single_number(mynumbers: pd.DataFrame) -> pd.DataFrame:
    # Группируем по числам и подсчитываем частоту
    count_series = mynumbers.groupby('num').size()
    # Оставляем числа, встречающиеся ровно один раз
    unique_nums = count_series[count_series == 1].index
    # Если есть уникальные числа, берем максимум, иначе NaN (который станет null)
    max_num = unique_nums.max() if len(unique_nums) > 0 else float('nan')
    # Возвращаем DataFrame с одной строкой и одной колонкой 'num'
    return pd.DataFrame({'num': [max_num]})