'''
https://leetcode.com/problems/number-of-people-aware-of-a-secret/description/?envType=daily-question&envId=2025-09-09
'''

class Solution:
    def peopleAwareOfSecret(self, n, delay, forget):
        """
        Вычисляет количество людей, знающих секрет к n-му дню.

        Каждый человек:
        - начинает делиться секретом через delay дней после того, как узнал его,
        - забывает секрет через forget дней.

        Алгоритм основан на динамическом программировании:
        dp[i] — количество людей, которые узнали секрет в день i.
        Считаем через префиксные суммы (difference array), чтобы учитывать только тех,
        кто может делиться и не забыл секрет.

        :param n: количество дней
        :param delay: через сколько дней начинают делиться
        :param forget: через сколько дней забывают
        :return: количество людей, знающих секрет на n-й день (mod 1e9+7)
        """
        MOD = 10**9 + 7
        dp = [0] * (n + 1)
        dp[1] = 1
        sum_sharing = 0

        for day in range(2, n + 1):
            if day - delay >= 1:
                sum_sharing = (sum_sharing + dp[day - delay]) % MOD
            if day - forget >= 1:
                sum_sharing = (sum_sharing - dp[day - forget] + MOD) % MOD
            dp[day] = sum_sharing

        return sum(dp[max(1, n - forget + 1):n + 1]) % MOD

''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks