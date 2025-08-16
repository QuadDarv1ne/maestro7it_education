'''
https://leetcode.com/problems/happy-number/description/
'''

from collections import defaultdict

class Solution:
    def isHappy(self, n):
        """
        Проверяет, является ли число счастливым.
        """
        seen = set()
        while n != 1 and n not in seen:
            seen.add(n)
            n = sum(int(c) ** 2 for c in str(n))
        return n == 1

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks