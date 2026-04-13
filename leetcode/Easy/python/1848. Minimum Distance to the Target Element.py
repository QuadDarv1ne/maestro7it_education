'''
https://leetcode.com/problems/add-binary/description/
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
'''

"""
Задача: Найти минимальное расстояние от индекса start до любого элемента массива nums,
значение которого равно target.

Дано:
    nums (List[int]) : массив целых чисел (индексация с 0)
    target (int)    : целевое значение, которое гарантированно присутствует в nums
    start (int)     : начальный индекс, 0 <= start < len(nums)

Найти:
    int : минимальное значение abs(i - start) среди всех i, где nums[i] == target

Примеры:
    Input: nums = [1,2,3,4,5], target = 5, start = 3
    Output: 1 (т.к. target находится по индексу 4, |4-3| = 1)

    Input: nums = [1], target = 1, start = 0
    Output: 0

    Input: nums = [1,1,1,1,1], target = 1, start = 2
    Output: 0 (индекс 2 совпадает с start)

Ограничения:
    1 <= len(nums) <= 1000
    1 <= nums[i] <= 10^4
    0 <= start < len(nums)
    target присутствует в nums

Идея решения:
    - Перебрать все индексы i от 0 до n-1
    - Если nums[i] == target, вычислить abs(i - start)
    - Вернуть минимальное из найденных расстояний
    - Сложность: O(n) по времени, O(1) по памяти
"""

# from typing import List

class Solution:
    def getMinDistance(self, nums, target, start):
        min_dist = float('inf')
        for i, val in enumerate(nums):
            if val == target:
                min_dist = min(min_dist, abs(i - start))
        return min_dist