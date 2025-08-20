'''
https://leetcode.com/problems/3sum-closest/description/
'''

# from typing import List

class Solution:
    # def threeSumClosest(self, nums: List[int], target: int) -> int:
    def threeSumClosest(self, nums, target):
        """
        Возвращает сумму трёх чисел из nums, наиболее близкую к target.

        Метод:
        1. Сортировка списка.
        2. Для каждого i используем два указателя, l и r, для поиска наилучшей суммы.
        3. Обновляем closest_sum при нахождении более близкой комбинации.
        4. При точном совпадении — возвращаем сразу.

        Время: O(n^2), Доп. память: O(1).
        """
        nums.sort()
        n = len(nums)
        closest_sum = nums[0] + nums[1] + nums[2]

        for i in range(n - 2):
            l, r = i + 1, n - 1
            while l < r:
                s = nums[i] + nums[l] + nums[r]
                if s == target:
                    return s
                if abs(s - target) < abs(closest_sum - target):
                    closest_sum = s
                if s < target:
                    l += 1
                else:
                    r -= 1

        return closest_sum

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks