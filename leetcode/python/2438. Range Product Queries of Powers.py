'''
https://leetcode.com/problems/range-product-queries-of-powers/description/?envType=daily-question&envId=2025-08-11
'''

"""
Функция productQueries:
:param n: положительное целое число, разбиваемое на минимальные степени двойки.
:param queries: список запросов [[l, r], ...]; нужно вернуть список продуктов этих степеней по модулю 10^9+7.
:return: список ответов на каждый запрос.
Алгоритм:
1. Извлекаем степени двойки (set-биты) из n.
2. Строим префикс произведений для быстрого вычисления диапазонов.
3. Для каждого запроса используем модульную инверсию (pow с mod-2), так как модуль прост.
"""
from typing import List

class Solution:
    def productQueries(self, n: int, queries: List[List[int]]) -> List[int]:
        MOD = 10**9 + 7
        powers = []
        bit = 0
        while n > 0:
            if n & 1:
                powers.append(1 << bit)
            bit += 1
            n >>= 1

        pre = [1]
        for x in powers:
            pre.append(pre[-1] * x % MOD)

        result = []
        for l, r in queries:
            inv = pow(pre[l], MOD - 2, MOD)
            result.append(pre[r + 1] * inv % MOD)
        return result

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
