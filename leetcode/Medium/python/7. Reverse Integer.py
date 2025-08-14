'''
https://leetcode.com/problems/reverse-integer/description/
'''

class Solution:
    def reverse(self, x):
        """
        Переворачивает цифры целого числа x и возвращает результат.
        Если результат выходит за пределы 32-битного диапазона, возвращает 0.
        """
        sign = -1 if x < 0 else 1
        x *= sign
        reversed_x = 0
        
        while x != 0:
            digit = x % 10
            reversed_x = reversed_x * 10 + digit
            if reversed_x > 2**31 - 1:
                return 0
            x //= 10
        
        return sign * reversed_x

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks