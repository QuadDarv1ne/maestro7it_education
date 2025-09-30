'''
https://leetcode.com/problems/fraction-to-recurring-decimal/description/?envType=daily-question&envId=2025-09-24
'''

class Solution:
    def fractionToDecimal(self, numerator, denominator):
        """
        Преобразует дробь numerator/denominator в строку с десятичным представлением.
        Если десятичная часть повторяется, заключает повторяющуюся часть в скобки.

        Алгоритм:
        1. Обработать знак и целую часть.
        2. Симулировать деление "в столбик" для дробной части.
        3. Использовать словарь для отслеживания остатков:
           - если остаток повторяется → найден цикл.
        4. Заключить повторяющуюся часть в скобки.

        Сложность:
        - Время O(L), где L — длина периода/дробной части.
        - Память O(L), так как сохраняем остатки.

        :param numerator: целое число (может быть отрицательным)
        :param denominator: целое число, не равное нулю
        :return: строка, например "0.5", "2", "0.(6)", "-0.1(6)"
        """
        if numerator == 0:
            return "0"

        result = []

        if (numerator < 0) ^ (denominator < 0):
            result.append("-")

        # работаем с абсолютными значениями
        n, d = abs(numerator), abs(denominator)
        result.append(str(n // d))
        remainder = n % d
        if remainder == 0:
            return "".join(result)

        # определяем знак и целую часть
        result.append(".")
        seen = {}

        while remainder != 0:
            if remainder in seen:
                idx = seen[remainder]
                result.insert(idx, "(")
                result.append(")")
                break
            seen[remainder] = len(result)
            remainder *= 10
            result.append(str(remainder // d))
            remainder %= d

        return "".join(result)

''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks