'''
https://leetcode.com/problems/ways-to-express-an-integer-as-sum-of-powers/description/?envType=daily-question&envId=2025-08-12
'''

MOD = 10**9 + 7

class Solution:
    def numberOfWays(self, n: int, x: int) -> int:
        """
        Находит количество способов представить число n как сумму уникальных целых чисел,
        возведённых в степень x.

        :param n: Целое число, которое нужно представить.
        :param x: Степень, в которую возводятся числа.
        :return: Количество способов представить n как сумму степеней чисел.
        """
        def dfs(i, remaining):
            if remaining == 0:
                return 1
            if i == 0 or remaining < 0:
                return 0
            if (i, remaining) in memo:
                return memo[(i, remaining)]

            include = dfs(i - 1, remaining - i**x)
            exclude = dfs(i - 1, remaining)

            memo[(i, remaining)] = (include + exclude) % MOD
            return memo[(i, remaining)]

        memo = {}
        return dfs(n, n)

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks