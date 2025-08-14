'''
https://leetcode.com/problems/soup-servings/description/?envType=daily-question&envId=2025-08-08
'''

class Solution:
    def soupServings(self, n: int) -> float:
        """
        Вычисляет вероятность того, что суп A закончится раньше супа B,
        плюс половина вероятности, что они закончатся одновременно.

        Идея:
        - Порции кратны 25 мл → масштабируем: m = ceil(n/25) = (n + 24) // 25.
        - Рекурсивный DFS с мемоизацией по состояниям (a, b) — сколько «четвертушек» (по 25 мл) осталось.
        - Базы:
            * a <= 0 и b <= 0 → 0.5
            * a <= 0 → 1.0
            * b <= 0 → 0.0
        - Переход:
            dfs(a,b) = 0.25 * [ dfs(a-4,b) + dfs(a-3,b-1) + dfs(a-2,b-2) + dfs(a-1,b-3) ]
        - Для больших n (≈ > 4800) ответ стремится к 1.0 → можно сразу вернуть 1.0.

        :param n: миллилитры каждого вида супа (0 ≤ n ≤ 1e9)
        :return: искомая вероятность (погрешность ≤ 1e-5)
        """
        if n > 4800:
            return 1.0

        m = (n + 24) // 25  # ceil(n/25) без импортов
        memo = {}

        def dfs(a: int, b: int) -> float:
            if a <= 0 and b <= 0:
                return 0.5
            if a <= 0:
                return 1.0
            if b <= 0:
                return 0.0
            key = (a, b)
            if key in memo:
                return memo[key]
            res = 0.25 * (
                dfs(a - 4, b) +
                dfs(a - 3, b - 1) +
                dfs(a - 2, b - 2) +
                dfs(a - 1, b - 3)
            )
            memo[key] = res
            return res

        return dfs(m, m)

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks