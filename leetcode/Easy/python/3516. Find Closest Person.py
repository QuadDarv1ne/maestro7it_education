'''
https://leetcode.com/problems/find-closest-person/description/?envType=daily-question&envId=2025-09-04
'''

class Solution:
    def findClosest(self, x, y, z):
        """
        Определяет, кто из двух людей ближе к цели.

        :param x: позиция первого человека
        :param y: позиция второго человека
        :param z: позиция цели
        :return: 1, если первый ближе;
                 2, если второй ближе;
                 0, если оба на одинаковом расстоянии
        """
        a = abs(x - z)
        b = abs(y - z)
        if a == b:
            return 0
        return 1 if a < b else 2

''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks