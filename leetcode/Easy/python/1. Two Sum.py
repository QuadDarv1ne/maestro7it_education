'''
https://leetcode.com/problems/two-sum/description/
'''

class Solution:
    def twoSum(self, nums, target):
        """
        Находит индексы двух чисел в массиве, сумма которых равна заданному числу target.

        :param nums: Список целых чисел.
        :param target: Целевое значение суммы.
        :return: Список из двух индексов чисел, сумма которых равна target.
        """
        seen = {}  # Словарь для хранения чисел и их индексов
        for i, num in enumerate(nums):
            complement = target - num
            if complement in seen:
                return [seen[complement], i]
            seen[num] = i
        return []


''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks