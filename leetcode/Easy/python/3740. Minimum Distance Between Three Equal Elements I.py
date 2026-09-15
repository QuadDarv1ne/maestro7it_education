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
    def minimumDistance(self, nums):
        """
        Находит минимальное расстояние между тремя одинаковыми элементами в массиве.

        Для каждой тройки индексов (i, j, k) с одинаковыми значениями nums[i] == nums[j] == nums[k]
        расстояние вычисляется как 2 * (k - i) при условии i < j < k.
        Чтобы минимизировать расстояние, достаточно для каждого числа рассмотреть все возможные
        комбинации по 3 индекса из списка его позиций и найти минимальную разницу между
        максимальным и минимальным индексом в этой тройке, умноженную на 2.

        Алгоритм:
        1. Сгруппировать индексы для каждого значения с помощью словаря.
        2. Для каждого значения, если индексов меньше 3 — пропустить.
        3. Перебрать все тройки индексов (i < j < k) в отсортированном списке позиций.
        4. Вычислить 2 * (k - i) и обновить глобальный минимум.

        Args:
            nums (List[int]): Входной массив целых чисел.

        Returns:
            int: Минимальное возможное расстояние. Если хороших троек нет, возвращает -1.
        """
        # Шаг 1: Группировка индексов по значениям
        positions = defaultdict(list)
        for idx, val in enumerate(nums):
            positions[val].append(idx)

        min_dist = float('inf')

        # Шаг 2: Обработка каждого значения
        for val, idx_list in positions.items():
            n = len(idx_list)
            if n < 3:
                continue

            # Шаг 3: Перебор всех троек индексов
            for i in range(n - 2):
                for j in range(i + 1, n - 1):
                    for k in range(j + 1, n):
                        # Шаг 4: Вычисление расстояния
                        dist = 2 * (idx_list[k] - idx_list[i])
                        if dist < min_dist:
                            min_dist = dist

        return -1 if min_dist == float('inf') else min_dist