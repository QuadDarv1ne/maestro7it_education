'''
https://leetcode.com/problems/3sum/description/
'''

# from typing import List

class Solution:
    # def threeSum(self, nums: List[int]) -> List[List[int]]:
    def threeSum(self, nums):
        """
        Задача: Найти все уникальные тройки чисел в массиве nums,
        сумма которых равна нулю.
        
        Метод:
        1. Сортируем массив.
        2. Для каждого числа используем два указателя (left, right),
           чтобы найти дополнение до нуля.
        3. Пропускаем дубликаты, чтобы не было одинаковых троек.

        Сложность:
        - Время: O(n^2)
        - Память: O(1), не считая памяти под результат.

        Пример:
        nums = [-1, 0, 1, 2, -1, -4]
        Результат = [[-1, -1, 2], [-1, 0, 1]]
        """
        nums.sort()
        res = []
        n = len(nums)

        for i in range(n - 2):
            if i > 0 and nums[i] == nums[i - 1]:
                continue
            if nums[i] > 0:
                break
            l, r = i + 1, n - 1
            while l < r:
                s = nums[i] + nums[l] + nums[r]
                if s < 0:
                    l += 1
                elif s > 0:
                    r -= 1
                else:
                    res.append([nums[i], nums[l], nums[r]])
                    while l < r and nums[l] == nums[l + 1]:
                        l += 1
                    while l < r and nums[r] == nums[r - 1]:
                        r -= 1
                    l += 1
                    r -= 1
        return res

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks