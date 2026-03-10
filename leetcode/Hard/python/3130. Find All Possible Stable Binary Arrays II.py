"""
Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Полезные ссылки:
1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
2. Telegram №1 @quadd4rv1n7
3. Telegram №2 @dupley_maxim_1999
4. Rutube канал: https://rutube.ru/channel/4218729/
5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
6. YouTube канал: https://www.youtube.com/@it-coders
7. ВК группа: https://vk.com/science_geeks
"""

class Solution:
    """
    Решение задачи «Найти все возможные стабильные бинарные массивы II».
    
    Алгоритм: Динамическое программирование с трёхмерным состоянием.
    
    Состояние:
        dp[i][j][k] — количество стабильных массивов, содержащих:
            - i нулей
            - j единиц
            - последний элемент равен k (0 или 1)
    
    Переходы:
        - Если добавляем 0: берём все массивы с (i-1, j) и добавляем 0 в конец,
          но вычитаем случаи, где это создаст последовательность из (limit+1) нулей.
        - Аналогично для добавления 1.
    
    Базовые случаи:
        - Массивы только из 0: допустимы, если длина ≤ limit
        - Массивы только из 1: допустимы, если длина ≤ limit
    
    Возвращаем: (dp[zero][one][0] + dp[zero][one][1]) % MOD
    
    Сложность:
        Время: O(zero × one)
        Память: O(zero × one)
    """
    
    def numberOfStableArrays(self, zero, one, limit):
        MOD = 1000000007
        
        # dp[i][j][k]: i нулей, j единиц, последний бит = k
        dp = [[[0] * 2 for _ in range(one + 1)] for _ in range(zero + 1)]
        
        # Базовые случаи: массивы только из одного типа элементов
        for i in range(min(zero, limit) + 1):
            dp[i][0][0] = 1  # только нули, длина ≤ limit
        for j in range(min(one, limit) + 1):
            dp[0][j][1] = 1  # только единицы, длина ≤ limit
        
        # Заполнение таблицы ДП
        for i in range(1, zero + 1):
            for j in range(1, one + 1):
                # Добавляем 0 в конец
                dp[i][j][0] = (
                    dp[i - 1][j][0] +  # предыдущий был 0
                    dp[i - 1][j][1] -  # предыдущий был 1
                    (dp[i - limit - 1][j][1] if i - limit >= 1 else 0) +  # исключаем недопустимые
                    MOD
                ) % MOD
                
                # Добавляем 1 в конец
                dp[i][j][1] = (
                    dp[i][j - 1][0] +  # предыдущий был 0
                    dp[i][j - 1][1] -  # предыдущий был 1
                    (dp[i][j - limit - 1][0] if j - limit >= 1 else 0) +  # исключаем недопустимые
                    MOD
                ) % MOD
        
        # Суммируем массивы, заканчивающиеся на 0 и на 1
        return (dp[zero][one][0] + dp[zero][one][1]) % MOD