'''
https://leetcode.com/problems/count-elements-with-maximum-frequency/description/?envType=daily-question&envId=2025-09-22

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
'''

from collections import Counter

class Solution:
    def maxFrequencyElements(self, nums):
        """
        Подсчёт общего количества элементов (суммарной частоты) для всех значений,
        частота которых равна максимальной частоте в массиве.

        :param nums: Входной список целых чисел
        :return: Суммарное количество элементов с максимальной частотой
        """
        freq = Counter(nums)
        if not freq:
            return 0
        maxFreq = max(freq.values())
        return sum(f for f in freq.values() if f == maxFreq)

''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks