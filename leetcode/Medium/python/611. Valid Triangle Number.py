'''
https://leetcode.com/problems/valid-triangle-number/description/?envType=daily-question&envId=2025-09-26
'''

class Solution:
    def triangleNumber(self, nums):
        """
        Возвращает количество троек (i, j, k), i < j < k,
        таких, что nums[i], nums[j], nums[k] могут образовать треугольник.
        
        Алгоритм:
        1. Сортируем массив.
        2. Фиксируем наибольшую сторону (nums[k]).
        3. Двигаем два указателя (l и r), чтобы подсчитать количество пар.
        """
        nums.sort()
        n = len(nums)
        ans = 0
        for k in range(n - 1, 1, -1):
            l, r = 0, k - 1
            while l < r:
                if nums[l] + nums[r] > nums[k]:
                    ans += (r - l)
                    r -= 1
                else:
                    l += 1
        return ans

''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks