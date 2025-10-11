'''
https://leetcode.com/problems/maximum-total-damage-with-spell-casting/?envType=daily-question&envId=2025-10-11
'''

import bisect
from collections import Counter
from functools import cache

class Solution:
    def maximumTotalDamage(self, power: list[int]) -> int:
        """
        Эффективное решение (O(n log n)) задачи "Maximum Total Damage With Spell Casting".
        Использует бинарный поиск для переходов между допустимыми значениями.
        """
        cnt = Counter(power)
        uniq = sorted(cnt.keys())
        n = len(uniq)

        nxt = [0] * n
        for i, d in enumerate(uniq):
            nxt[i] = bisect.bisect_right(uniq, d + 2)

        @cache
        def dfs(i: int) -> int:
            if i >= n:
                return 0
            skip = dfs(i + 1)
            take = uniq[i] * cnt[uniq[i]] + dfs(nxt[i])
            return max(skip, take)

        return dfs(0)

''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks