"""
https://leetcode.com/problems/next-permutation/description/
Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
"""

class Solution:
    def nextPermutation(self, nums):
        """
        Находит следующую лексикографическую перестановку массива.
        Модифицирует исходный массив на месте.
        
        Алгоритм:
        1. Найти убывающий суффикс (идем справа налево)
        2. Найти элемент для обмена
        3. Обменять элементы
        4. Развернуть суффикс
        
        Args:
            nums: список целых чисел для модификации
            
        Returns:
            None (модифицирует список на месте)
        """
        n = len(nums)
        if n <= 1:
            return
        
        # Шаг 1: Найти первый убывающий элемент справа
        i = n - 2
        while i >= 0 and nums[i] >= nums[i + 1]:
            i -= 1
        
        # Шаг 2: Если нашли убывающий элемент
        if i >= 0:
            # Найти наименьший элемент справа от i, который больше nums[i]
            j = n - 1
            while j >= 0 and nums[j] <= nums[i]:
                j -= 1
            # Обменять элементы
            nums[i], nums[j] = nums[j], nums[i]
        
        # Шаг 3: Развернуть суффикс (от i+1 до конца)
        left, right = i + 1, n - 1
        while left < right:
            nums[left], nums[right] = nums[right], nums[left]
            left += 1
            right -= 1

''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
