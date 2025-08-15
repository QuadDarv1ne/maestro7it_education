'''
https://leetcode.com/problems/power-of-four/description/?envType=daily-question&envId=2025-08-15
'''

class Solution:
    def isPowerOfFour(self, n):
        """
        Проверяет, является ли число степенью четырёх.

        Условия:
        1. n > 0
        2. (n & (n - 1)) == 0  — строго одна единичная битовая единица (степень двух).
        3. (n & 0x55555555) == n — единица находится на чётной позиции.

        :param n: int — проверяемое число
        :return: bool — True, если n == 4^k для некоторого целого k ≥ 0, иначе False
        """
        return n > 0 and (n & (n - 1)) == 0 and (n & 0x55555555) == n

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks