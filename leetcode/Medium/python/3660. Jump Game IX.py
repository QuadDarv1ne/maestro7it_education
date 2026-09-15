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

class Solution:
    def maxValue(self, nums):
        """
        Для каждого индекса i вычисляет максимальное значение в nums, 
        которое может быть достигнуто, начиная с i, следуя правилам прыжков.
        
        Правила прыжков:
        - Прыжок вперёд (j > i) разрешён, только если nums[j] < nums[i].
        - Прыжок назад (j < i) разрешён, только если nums[j] > nums[i].
        
        Стратегия основана на поиске компонент связности в неявном графе,
        где рёбра задаются правилами. Компоненты образуют непрерывные отрезки,
        разделённые «разрезами»: все элементы слева от разреза <= все элементы справа.
        В каждой компоненте максимальное достижимое значение — это максимум по отрезку.
        """
        n = len(nums)
        ans = [0] * n
        
        # prefix_max[i] = максимум на отрезке [0..i]
        prefix_max = [0] * n
        cur_max = nums[0]
        for i in range(n):
            cur_max = max(cur_max, nums[i])
            prefix_max[i] = cur_max
        
        # suffix_min[i] = минимум на отрезке [i..n-1]
        suffix_min = [0] * n
        cur_min = nums[-1]
        for i in range(n - 1, -1, -1):
            cur_min = min(cur_min, nums[i])
            suffix_min[i] = cur_min
        
        # Находим индексы разрезов между соседними элементами.
        # Разрез между i и i+1 существует, если максимум слева <= минимум справа.
        cut_indices = []
        for i in range(n - 1):
            if prefix_max[i] <= suffix_min[i + 1]:
                cut_indices.append(i)
        
        # Обрабатываем каждый отрезок между разрезами (или от границы массива).
        start = 0
        for cut in cut_indices:
            end = cut
            # Вычисляем максимум на отрезке [start..end]
            seg_max = max(nums[start:end + 1])
            for i in range(start, end + 1):
                ans[i] = seg_max
            start = end + 1
        
        # Последний отрезок от последнего разреза (или 0) до конца массива.
        if start < n:
            seg_max = max(nums[start:])
            for i in range(start, n):
                ans[i] = seg_max
        
        return ans