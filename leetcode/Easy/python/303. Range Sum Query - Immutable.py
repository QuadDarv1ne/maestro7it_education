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

class NumArray:
    """
    Класс для быстрого вычисления суммы элементов подмассива.
    Использует предварительно вычисленные префиксные суммы.
    """
    def __init__(self, nums):
        """
        Инициализирует объект массивом nums и вычисляет префиксные суммы.

        Аргументы:
            nums (list[int]): исходный массив целых чисел.
        """
        self.prefix = [0] * (len(nums) + 1)
        for i in range(len(nums)):
            self.prefix[i + 1] = self.prefix[i] + nums[i]

    def sumRange(self, left, right):
        """
        Возвращает сумму элементов nums с индекса left по right включительно.

        Аргументы:
            left (int): начальный индекс (включительно).
            right (int): конечный индекс (включительно).

        Возвращает:
            int: сумма элементов на отрезке [left, right].
        """
        return self.prefix[right + 1] - self.prefix[left]