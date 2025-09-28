'''
https://leetcode.com/problems/largest-perimeter-triangle/description/?envType=daily-question&envId=2025-09-28
'''

class Solution:
    def largestPerimeter(self, nums):
        """
        Находит максимальный периметр треугольника, который можно построить
        из трёх длин массива nums.

        Алгоритм:
        1. Сортируем массив по возрастанию.
        2. Перебираем элементы с конца (nums[i] — наибольшая сторона).
        3. Для каждой тройки (nums[i-2], nums[i-1], nums[i]) проверяем условие треугольника:
           nums[i-2] + nums[i-1] > nums[i].
        4. Как только находим подходящую тройку — возвращаем её периметр.
        5. Если ни одна тройка не подходит — возвращаем 0.
        """
        nums.sort()
        n = len(nums)
        for i in range(n - 1, 1, -1):
            a, b, c = nums[i-2], nums[i-1], nums[i]
            if a + b > c:
                return a + b + c
        return 0

''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks