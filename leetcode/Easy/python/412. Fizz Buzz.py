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
    def fizzBuzz(self, n: int) -> list[str]:
        """
        Возвращает массив строк для чисел от 1 до n по правилам FizzBuzz.

        Аргументы:
            n (int): верхняя граница диапазона (включительно).

        Возвращает:
            list[str]: массив, где для каждого числа от 1 до n:
                - "FizzBuzz", если число делится на 3 и на 5,
                - "Fizz", если только на 3,
                - "Buzz", если только на 5,
                - иначе само число в виде строки.
        """
        answer = []
        for i in range(1, n + 1):
            if i % 15 == 0:  # делится на 3 и 5
                answer.append("FizzBuzz")
            elif i % 3 == 0:
                answer.append("Fizz")
            elif i % 5 == 0:
                answer.append("Buzz")
            else:
                answer.append(str(i))
        return answer