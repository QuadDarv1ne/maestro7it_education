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
    def addStrings(self, num1: str, num2: str) -> str:
        """
        Складывает два неотрицательных числа, представленных в виде строк.

        Аргументы:
            num1 (str): первое число в виде строки.
            num2 (str): второе число в виде строки.

        Возвращает:
            str: результат сложения в виде строки.

        Алгоритм:
            - Проходим по цифрам справа налево, имитируя сложение столбиком.
            - На каждом шаге вычисляем сумму двух цифр и переноса.
            - Формируем результат с конца.
        """
        i, j = len(num1) - 1, len(num2) - 1
        carry = 0
        result = []

        while i >= 0 or j >= 0 or carry:
            digit1 = int(num1[i]) if i >= 0 else 0
            digit2 = int(num2[j]) if j >= 0 else 0

            total = digit1 + digit2 + carry
            carry = total // 10
            result.append(str(total % 10))

            i -= 1
            j -= 1

        # Так как мы добавляли цифры от младших к старшим, нужно развернуть
        return ''.join(reversed(result))