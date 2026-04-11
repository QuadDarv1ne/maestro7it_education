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

# from typing import List
from collections import defaultdict

class Solution:
    """
    Класс для решения задачи поиска минимального расстояния между тремя равными элементами.
    """
    def minimumDistance(self, nums):
        """
        Находит минимальное расстояние между тремя равными элементами в массиве.

        Алгоритм:
        1. Группирует индексы каждого числа с помощью defaultdict.
        2. Для каждой группы, содержащей минимум 3 элемента, вычисляет расстояние
           между первым и третьим индексом в каждой тройке последовательных индексов.
        3. Возвращает минимальное из найденных расстояний или -1, если таких троек нет.

        Args:
            nums (List[int]): Входной массив целых чисел.

        Returns:
            int: Минимальное расстояние или -1.

        Examples:
            >>> s = Solution()
            >>> s.minimumDistance([1,2,1,1,3])
            6
            >>> s.minimumDistance([1,1,2,3,2,1,2])
            8
            >>> s.minimumDistance([1])
            -1
        """
        # Группируем индексы по значениям
        val_to_indices = defaultdict(list)
        for i, num in enumerate(nums):
            val_to_indices[num].append(i)

        min_dist = float('inf')
        for indices in val_to_indices.values():
            n = len(indices)
            if n >= 3:
                # Проверяем все последовательные тройки
                for i in range(n - 2):
                    dist = 2 * (indices[i + 2] - indices[i])
                    if dist < min_dist:
                        min_dist = dist

        return min_dist if min_dist != float('inf') else -1