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

# Python
class Solution:
    """
    Находит минимальный элемент в повернутом отсортированном массиве с дубликатами.
    
    Подход:
    1. Используем модифицированный бинарный поиск
    2. Сравниваем mid с right для определения направления поиска
    3. При nums[mid] == nums[right] уменьшаем right на 1
    
    Сложность по времени: O(log n) в среднем, O(n) в худшем случае (все элементы одинаковы)
    Сложность по памяти: O(1)
    """
    
    def findMin(self, nums):
        left, right = 0, len(nums) - 1
        
        while left < right:
            mid = left + (right - left) // 2
            
            if nums[mid] < nums[right]:
                # Минимум находится в левой половине (включая mid)
                right = mid
            elif nums[mid] > nums[right]:
                # Минимум находится в правой половине (исключая mid)
                left = mid + 1
            else:
                # nums[mid] == nums[right], не можем определить направление
                # Уменьшаем область поиска
                right -= 1
        
        return nums[left]