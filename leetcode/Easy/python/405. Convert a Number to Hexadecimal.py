"""
Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Полезные ссылки:
1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
2. Telegram №1 @quadd4rv1n7
3. Telegram №2 @dupley_maxim_1999
4. Rutube канал: https://rutube.ru/channel/4218729/
5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
6. YouTube канал: https://www.youtube.com/@it-coders
7. ВК группа: https://vk.com/science_geeks
"""

class Solution:
    def toHex(self, num: int) -> str:
        """
        Преобразует 32-битное целое число в шестнадцатеричную строку.

        Алгоритм:
        1. Если num == 0, вернуть "0".
        2. Для отрицательных чисел используем дополнительный код:
           прибавляем 2**32, чтобы получить беззнаковое представление.
        3. Извлекаем по 4 бита (младшие), преобразуем в hex-цифру и собираем
           результат с конца.

        Аргументы:
            num (int): 32-битное целое число.

        Возвращает:
            str: шестнадцатеричное представление в нижнем регистре.
        """
        if num == 0:
            return "0"

        # Для отрицательных чисел получаем беззнаковое 32-битное значение
        if num < 0:
            num += 2 ** 32

        hex_chars = "0123456789abcdef"
        result = []

        while num > 0:
            # Берём младшие 4 бита
            digit = num & 0xF
            result.append(hex_chars[digit])
            # Сдвигаем вправо на 4 бита
            num >>= 4

        # Так как мы собирали цифры от младших к старшим, нужно развернуть
        return ''.join(reversed(result))