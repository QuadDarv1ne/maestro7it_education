'''
https://leetcode.com/problems/new-21-game/description/?envType=daily-question&envId=2025-08-17
'''

class Solution:
    def new21Game(self, n, k, maxPt):
        """
        Игра "Новый Блэкджек".
        Мы начинаем с 0 очков и тянем карты до тех пор, пока сумма < k.
        Каждая карта даёт от 1 до maxPts очков равновероятно.
        Нужно вычислить вероятность того, что итоговая сумма ≤ n.

        :param n: int - максимальное количество очков, которое нас устраивает
        :param k: int - порог остановки (перестаём тянуть карты, если сумма >= k)
        :param maxPts: int - максимальное количество очков за карту
        :return: float - вероятность, что итоговое количество очков ≤ n
        """
        if k == 0 or n >= k - 1 + maxPts:
            return 1.0

        dp = [0.0] * (n + 1)
        dp[0] = 1.0
        window_sum = 1.0
        result = 0.0

        for i in range(1, n + 1):
            dp[i] = window_sum / maxPts
            if i < k:
                window_sum += dp[i]
            else:
                result += dp[i]
            if i - maxPts >= 0:
                window_sum -= dp[i - maxPts]

        return result

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks