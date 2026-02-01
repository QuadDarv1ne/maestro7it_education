"""
Решение задачи LeetCode № 3010: "Divide an Array Into Subarrays With Minimum Cost I"
https://leetcode.com/problems/divide-an-array-into-subarrays-with-minimum-cost-i/description/
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

class Solution(object):
    def minimumCost(self, nums):
        """
        Находит минимальную стоимость разделения массива на 3 подмассива.
        
        Массив делится на 3 непустых подмассива nums[0..i], nums[i+1..j], nums[j+1..n-1].
        Стоимость разделения = nums[0] + nums[i+1] + nums[j+1] (первые элементы каждого подмассива).
        
        Так как nums[0] всегда включается в стоимость, нужно найти два минимальных элемента
        среди nums[1:] и добавить их к nums[0].
        
        :type nums: List[int]
        :rtype: int
        """
        # nums[0] всегда является первым элементом первого подмассива
        cost = nums[0]
        
        # Находим два минимальных элемента среди оставшихся элементов
        min1 = float('inf')
        min2 = float('inf')
        
        for i in range(1, len(nums)):
            if nums[i] < min1:
                min2 = min1
                min1 = nums[i]
            elif nums[i] < min2:
                min2 = nums[i]
        
        # Возвращаем сумму: первый элемент + два минимальных из оставшихся
        return cost + min1 + min2