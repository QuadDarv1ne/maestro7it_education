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
    def thirdMax(self, nums: list[int]) -> int:
        """
        Возвращает третий уникальный максимум или максимальное число,
        если уникальных значений меньше трёх.

        Аргументы:
            nums (list[int]): массив целых чисел.

        Возвращает:
            int: третий уникальный максимум или максимальное число.
        """
        # Используем None для обозначения "не установлено"
        first = second = third = None

        for num in nums:
            # Пропускаем, если число уже является одним из текущих максимумов
            if num == first or num == second or num == third:
                continue

            # Обновляем максимумы со сдвигом
            if first is None or num > first:
                third = second
                second = first
                first = num
            elif second is None or num > second:
                third = second
                second = num
            elif third is None or num > third:
                third = num

        # Если третий максимум был найден (не None), возвращаем его
        return third if third is not None else first