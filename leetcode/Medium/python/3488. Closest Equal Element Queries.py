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
import bisect

class Solution:
    def solveQueries(self, nums, queries):
        """
        Находит минимальное кольцевое расстояние до ДРУГОГО равного элемента.
        """
        n = len(nums)
        index_map = defaultdict(list)
        for i, val in enumerate(nums):
            index_map[val].append(i)
            
        answer = []
        
        for q in queries:
            val = nums[q]
            pos = index_map[val]
            m = len(pos)
            
            if m == 1:
                answer.append(-1)
                continue
                
            # Находим индекс элемента q в списке pos
            idx = bisect.bisect_left(pos, q)
            
            # Определяем соседей (ЛЕВОГО и ПРАВОГО) в списке pos
            left_idx = (idx - 1) % m
            right_idx = (idx + 1) % m
            
            left_pos = pos[left_idx]
            right_pos = pos[right_idx]
            
            # Вычисление кольцевого расстояния
            d_left = abs(q - left_pos)
            dist_left = min(d_left, n - d_left)
            
            d_right = abs(q - right_pos)
            dist_right = min(d_right, n - d_right)
            
            answer.append(min(dist_left, dist_right))
            
        return answer