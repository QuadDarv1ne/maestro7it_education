'''
https://leetcode.com/problems/water-bottles-ii/description/?envType=daily-question&envId=2025-10-02
'''

class Solution:
    def maxBottlesDrunk(self, numBottles, numExchange):
        """
        Задача: Water Bottles II
        Возвращает максимальное число бутылок, которые можно выпить.

        Алгоритм:
        1. Пьём все начальные бутылки.
        2. Пока пустых бутылок хватает для обмена:
            - Делаем обмен.
            - Пьём новую бутылку.
            - Курс обмена увеличивается на 1.
        """
        ans = numBottles
        empty = numBottles
        while empty >= numExchange:
            empty = empty - numExchange + 1
            ans += 1
            numExchange += 1
        return ans

''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks