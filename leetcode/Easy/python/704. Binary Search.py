'''
https://leetcode.com/problems/binary-search/description/
'''

class Solution:
    def search(self, nums, target):
        """
        Выполняет бинарный поиск элемента target в отсортированном массиве nums.

        :param nums: Список целых чисел, отсортированный по возрастанию.
        :param target: Целое число, которое необходимо найти в массиве.
        :return: Индекс элемента target в массиве nums, или -1, если элемент не найден.
        """
        left, right = 0, len(nums) - 1

        while left <= right:
            mid = left + (right - left) // 2
            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1

        return -1

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks