'''
https://leetcode.com/problems/convert-integer-to-the-sum-of-two-no-zero-integers/description/?envType=daily-question&envId=2025-09-08
'''

class Solution:
    def getNoZeroIntegers(self, n):
        """
        Задача: Разбить число n на два положительных числа a и b,
        такие что:
        1) a + b = n
        2) a и b не содержат цифру '0'

        Метод:
        - Перебираем числа a от 1 до n-1
        - Вычисляем b = n - a
        - Проверяем, что в строковом представлении a и b нет '0'
        - Возвращаем первую подходящую пару
        """
        for a in range(1, n):
            b = n - a
            if '0' not in str(a) and '0' not in str(b):
                return [a, b]
        return []

''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks