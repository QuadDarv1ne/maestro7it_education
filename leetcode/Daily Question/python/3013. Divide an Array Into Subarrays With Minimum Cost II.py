"""
Решение задачи LeetCode № 3013. Divide an Array Into Subarrays With Minimum Cost II"
https://leetcode.com/problems/divide-an-array-into-subarrays-with-minimum-cost-ii/description/
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

import bisect

class Solution(object):
    def minimumCost(self, nums, k, dist):
        """
        :type nums: List[int]
        :type k: int
        :type dist: int
        :rtype: int
        """
        n = len(nums)
        if k == 1:
            return nums[0]
        
        # Поддерживаем два отсортированных списка
        selected = []  # k-1 наименьших элементов
        candidates = []  # остальные элементы
        selected_sum = 0
        
        # Инициализация первого окна [1, dist+1]
        window = sorted([nums[i] for i in range(1, min(n, dist + 2))])
        
        selected = window[:k-1]
        selected_sum = sum(selected)
        candidates = window[k-1:]
        
        min_cost = nums[0] + selected_sum
        
        # Скользим окном
        for right in range(dist + 2, n):
            left = right - dist - 1
            out_val = nums[left]
            in_val = nums[right]
            
            # Удаляем выходящий элемент
            idx = bisect.bisect_left(selected, out_val)
            if idx < len(selected) and selected[idx] == out_val:
                selected.pop(idx)
                selected_sum -= out_val
                
                # Если удалили из selected, нужно добавить наименьший из candidates
                if candidates:
                    val = candidates.pop(0)
                    bisect.insort(selected, val)
                    selected_sum += val
            else:
                idx = bisect.bisect_left(candidates, out_val)
                if idx < len(candidates):
                    candidates.pop(idx)
            
            # Добавляем входящий элемент
            if len(selected) < k - 1:
                bisect.insort(selected, in_val)
                selected_sum += in_val
            elif not selected or in_val < selected[-1]:
                # Новый элемент должен быть в selected
                if len(selected) == k - 1:
                    # Перемещаем максимальный из selected в candidates
                    val = selected.pop()
                    selected_sum -= val
                    bisect.insort(candidates, val)
                
                bisect.insort(selected, in_val)
                selected_sum += in_val
            else:
                # Новый элемент идет в candidates
                bisect.insort(candidates, in_val)
            
            min_cost = min(min_cost, nums[0] + selected_sum)
        
        return min_cost