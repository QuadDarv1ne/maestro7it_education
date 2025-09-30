'''
https://leetcode.com/problems/find-triangular-sum-of-an-array/description/?envType=daily-question&envId=2025-09-30
'''

class Solution:
    def triangularSum(self, nums):
        """
        Находит треугольную сумму массива:
        Пока длина nums > 1:
          создаём новый массив newNums длиной len(nums)-1,
          newNums[i] = (nums[i] + nums[i+1]) % 10.
        Возвращает последний оставшийся элемент.
        """
        n = len(nums)
        # Пошаговая симуляция от длины n до 1
        for length in range(n, 1, -1):
            for i in range(length - 1):
                nums[i] = (nums[i] + nums[i + 1]) % 10
        return nums[0]

''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks