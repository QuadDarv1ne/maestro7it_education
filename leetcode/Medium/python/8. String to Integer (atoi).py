'''
https://leetcode.com/problems/string-to-integer-atoi/description/
'''
class Solution:
    def myAtoi(self, s):
        """
        Преобразует строку s в 32-битное знаковое целое число.
        Обрабатывает пробелы, знак числа, недопустимые символы и переполнение.
        """
        i, n = 0, len(s)
        while i < n and s[i] == ' ':
            i += 1
        
        if i == n:
            return 0

        sign = 1
        if s[i] == '-':
            sign = -1
            i += 1
        elif s[i] == '+':
            i += 1

        result = 0
        while i < n and s[i].isdigit():
            digit = int(s[i])
            if result > (2**31 - 1) // 10 or (result == (2**31 - 1) // 10 and digit > 7):
                return 2**31 - 1 if sign == 1 else -2**31
            result = result * 10 + digit
            i += 1

        return sign * result

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks