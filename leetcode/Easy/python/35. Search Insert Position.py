'''
https://leetcode.com/problems/search-insert-position/description/
Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Решение задачи "Search Insert Position"

Полезные ссылки:
1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
2. Telegram №1 @quadd4rv1n7
3. Telegram №2 @dupley_maxim_1999
4. Rutube канал: https://rutube.ru/channel/4218729/
5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
6. YouTube канал: https://www.youtube.com/@it-coders
7. ВК группа: https://vk.com/science_geeks
'''

class Solution:
    def searchInsert(self, nums, target):
        """
        Находит позицию для вставки target в отсортированный массив.
        
        Args:
            nums (list[int]): Отсортированный массив уникальных целых чисел
            target (int): Целевое значение для поиска/вставки
            
        Returns:
            int: Индекс target, если найден, иначе индекс для вставки
        """
        left, right = 0, len(nums) - 1
        
        while left <= right:
            mid = (left + right) // 2
            
            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        
        # Если элемент не найден, left указывает на позицию для вставки
        return left