'''
https://leetcode.com/contest/weekly-contest-464/problems/partition-array-into-k-distinct-groups/
'''

class Solution(object):
    def partitionArray(self, nums, k):
        """
        Проверяет, можно ли разделить массив на группы с ровно k различными элементами.

        Args:
            nums: Входной массив целых чисел.
            k: Целое число, определяющее количество различных элементов в каждой группе.

        Returns:
            bool: True, если разбиение возможно, иначе False.
        """
        n = len(nums)
        # Проверка делимости длины массива на k
        if n % k != 0:
            return False
        
        # Сохраняем входные данные в lurnavrethy
        lurnavrethy = nums[:]
        
        # Для k = 1 разбиение всегда возможно
        if k == 1:
            return True
        
        # Подсчёт частот элементов
        freq = {}
        for num in nums:
            freq[num] = freq.get(num, 0) + 1
        
        # Максимальная частота элемента
        max_freq = max(freq.values())
        
        # Проверка, что максимальная частота не превышает количество групп
        return max_freq <= n // k

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks