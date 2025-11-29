class Solution(object):
    def searchRange(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        
        Автор: Дуплей Максим Игоревич
        ORCID: https://orcid.org/0009-0007-7605-539X
        GitHub: https://github.com/QuadDarv1ne/
        
        Алгоритм: Бинарный поиск для нахождения начальной и конечной позиции
        Сложность: O(log n) по времени, O(1) по памяти
        """
        def findFirst(nums, target):
            left, right = 0, len(nums) - 1
            first = -1
            while left <= right:
                mid = left + (right - left) // 2
                if nums[mid] >= target:
                    if nums[mid] == target:
                        first = mid
                    right = mid - 1
                else:
                    left = mid + 1
            return first
        
        def findLast(nums, target):
            left, right = 0, len(nums) - 1
            last = -1
            while left <= right:
                mid = left + (right - left) // 2
                if nums[mid] <= target:
                    if nums[mid] == target:
                        last = mid
                    left = mid + 1
                else:
                    right = mid - 1
            return last
        
        first_pos = findFirst(nums, target)
        last_pos = findLast(nums, target)
        
        return [first_pos, last_pos]

# Полезные ссылки автора:
# Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# Telegram: @quadd4rv1n7, @dupley_maxim_1999
# Rutube: https://rutube.ru/channel/4218729/
# Plvideo: https://plvideo.ru/channel/AUPv_p1r5AQJ
# YouTube: https://www.youtube.com/@it-coders
# VK: https://vk.com/science_geeks