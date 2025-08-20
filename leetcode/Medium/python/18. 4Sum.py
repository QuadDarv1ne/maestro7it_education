'''
https://leetcode.com/problems/4sum/description/
'''

# from typing import List

class Solution:
    # def fourSum(self, nums: List[int], target: int) -> List[List[int]]:
    def fourSum(self, nums, target):
        """
        Описание:
            Находит все уникальные квартеты (a, b, c, d) из массива nums,
            такие что a + b + c + d == target. Результат не содержит дубликатов,
            порядок квартетов не важен.

        Параметры:
            nums (List[int]): входной массив целых чисел.
            target (int): целевая сумма.

        Возвращает:
            List[List[int]]: список уникальных квартетов.

        Идея алгоритма:
            1) Отсортировать массив.
            2) Перебрать первые две позиции i, j (O(n^2)).
            3) Для оставшихся двух элементов использовать два указателя (left/right).
            4) Пропускать дубликаты на всех уровнях.

        Сложность:
            Время: O(n^3), Память: O(1) дополнительная (не считая результата).

        Пример:
            >>> Solution().fourSum([1,0,-1,0,-2,2], 0)
            [[-2,-1,1,2],[-2,0,0,2],[-1,0,0,1]]
        """
        nums.sort()
        n = len(nums)
        res = []

        for i in range(n - 3):
            if i > 0 and nums[i] == nums[i - 1]:
                continue
            # малые/большие отсеки (необязательно, но может ускорить)
            # if nums[i] + nums[i+1] + nums[i+2] + nums[i+3] > target: break
            # if nums[i] + nums[n-3] + nums[n-2] + nums[n-1] < target: continue

            for j in range(i + 1, n - 2):
                if j > i + 1 and nums[j] == nums[j - 1]:
                    continue

                left, right = j + 1, n - 1
                while left < right:
                    s = nums[i] + nums[j] + nums[left] + nums[right]
                    if s == target:
                        res.append([nums[i], nums[j], nums[left], nums[right]])
                        left += 1
                        right -= 1
                        while left < right and nums[left] == nums[left - 1]:
                            left += 1
                        while left < right and nums[right] == nums[right + 1]:
                            right -= 1
                    elif s < target:
                        left += 1
                    else:
                        right -= 1
        return res

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks