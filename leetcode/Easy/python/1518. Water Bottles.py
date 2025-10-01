'''
https://leetcode.com/problems/water-bottles/description/?envType=daily-question&envId=2025-10-01
'''

class Solution:
    def numWaterBottles(self, numBottles, numExchange):
        """
        Возвращает максимальное количество бутылок, которые можно выпить,
        если можно обменивать numExchange пустых бутылок на одну полную.

        Алгоритм:
        1. Начально выпиваем все numBottles → ans = numBottles, empty = numBottles.
        2. Пока empty >= numExchange:
           - newBottles = empty // numExchange
           - ans += newBottles
           - empty = (empty % numExchange) + newBottles
        3. Возвращаем ans.
        """
        ans = numBottles
        empty = numBottles
        while empty >= numExchange:
            new = empty // numExchange
            ans += new
            empty = (empty % numExchange) + new
        return ans

''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks