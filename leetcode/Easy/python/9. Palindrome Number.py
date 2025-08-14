'''
https://leetcode.com/problems/palindrome-number/description/
'''

class Solution:
    def isPalindrome(self, x):
        """
        Проверяет, является ли целое число x палиндромом без преобразования в строку.

        Действия:
        - Отрицательные числа и числа, оканчивающиеся на 0 (кроме 0) → False.
        - Переворачиваем цифры с конца по одной, пока перевёрнутая часть меньше остальной.
        - В конце сравниваем: x == rev (чётная) или x == rev // 10 (нечётная).

        Время: O(log₁₀(x)), память: O(1).
        """
        if x < 0 or (x % 10 == 0 and x != 0):
            return False
        rev = 0
        while x > rev:
            rev = rev * 10 + x % 10
            x //= 10
        return x == rev or x == rev // 10

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks