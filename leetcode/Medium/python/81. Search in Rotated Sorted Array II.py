'''
https://leetcode.com/problems/search-in-rotated-sorted-array-ii/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
'''

class Solution(object):
    def search(self, nums, target):
        """
        Решение задачи "Search in Rotated Sorted Array II" (LeetCode 81).

        Задача:
        - Дан повернутый отсортированный массив nums, содержащий дубликаты.
        - Необходимо определить, существует ли элемент target в массиве.

        Идея:
        - Используем модифицированный бинарный поиск.
        - На каждом шаге определяем, какая часть массива упорядочена.
        - Если nums[left] == nums[mid], невозможно понять структуру —
          просто сдвигаем левую границу.
        - Если левая или правая часть упорядочена, проверяем,
          может ли target находиться в этой части.

        Сложность:
        - Время: O(log n) в среднем, O(n) в худшем случае (из-за дубликатов)
        - Память: O(1)
        """
        left, right = 0, len(nums) - 1

        while left <= right:
            mid = (left + right) // 2

            # Если элемент найден
            if nums[mid] == target:
                return True

            # Невозможно определить упорядоченную часть из-за дубликатов
            if nums[left] == nums[mid]:
                left += 1
                continue

            # Левая часть отсортирована
            if nums[left] < nums[mid]:
                if nums[left] <= target < nums[mid]:
                    right = mid - 1
                else:
                    left = mid + 1
            # Правая часть отсортирована
            else:
                if nums[mid] < target <= nums[right]:
                    left = mid + 1
                else:
                    right = mid - 1

        return False


''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07  
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/  
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ  
# 6. YouTube канал: https://www.youtube.com/@it-coders  
# 7. ВК группа: https://vk.com/science_geeks
