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

'''
https://leetcode.com/problems/minimum-operations-to-make-a-uni-value-grid/description/?envType=daily-question&envId=2026-04-28
'''

from typing import List

class Solution:
    def minOperations(self, grid, x):
        """
        Возвращает минимальное количество операций для приведения
        двумерной сетки grid к uni-value (все элементы равны).

        За одну операцию можно прибавить x или вычесть x из любого элемента.

        Если это невозможно, возвращает -1.

        :param grid: двумерный список целых чисел (m x n)
        :param x: целое число, шаг изменения элементов
        :return: минимальное число операций или -1
        """
        # Разворачиваем сетку в одномерный список
        flat = [num for row in grid for num in row]

        # Проверяем остатки – все должны быть равны
        remainder = flat[0] % x
        for val in flat:
            if val % x != remainder:
                return -1

        # Сортируем и находим медиану
        flat.sort()
        median = flat[len(flat) // 2]

        # Считаем суммарные операции
        ops = 0
        for val in flat:
            ops += abs(val - median) // x

        return ops