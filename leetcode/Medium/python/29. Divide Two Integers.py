'''
https://leetcode.com/problems/divide-two-integers/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
'''

class Solution(object):
    def divide(self, dividend, divisor):
        """
        Решение задачи "Divide Two Integers" (LeetCode 29).

        Идея:
        - Работаем с абсолютными значениями dividend и divisor.
        - Используем битовые сдвиги для ускорения вычитания (аналог умножения на 2).
        - Обрабатываем переполнение: результат должен быть в диапазоне [-2^31, 2^31 - 1].
        - Учитываем знак результата отдельно.

        Сложность:
        - Время: O(log² n)
        - Память: O(1)
        """
        INT_MAX = 2**31 - 1
        INT_MIN = -2**31

        # Особый случай: переполнение при делении INT_MIN на -1
        if dividend == INT_MIN and divisor == -1:
            return INT_MAX

        # Определяем знак результата
        negative = (dividend < 0) ^ (divisor < 0)

        # Работаем с положительными числами
        dividend, divisor = abs(dividend), abs(divisor)

        quotient = 0
        while dividend >= divisor:
            temp = divisor
            multiple = 1
            # Удваиваем divisor, пока не превысим делимое
            while dividend >= (temp << 1):
                temp <<= 1
                multiple <<= 1
            dividend -= temp
            quotient += multiple

        if negative:
            quotient = -quotient

        # Гарантируем укладывание в 32-битный диапазон
        return min(max(quotient, INT_MIN), INT_MAX)

''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07  
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/  
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ  
# 6. YouTube канал: https://www.youtube.com/@it-coders  
# 7. ВК группа: https://vk.com/science_geeks