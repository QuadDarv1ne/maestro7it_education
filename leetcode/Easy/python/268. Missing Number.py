"""
Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Полезные ссылки:
1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
2. Telegram №1 @quadd4rv1n7
3. Telegram №2 @dupley_maxim_1999
4. Rutube канал: https://rutube.ru/channel/4218729/
5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
6. YouTube канал: https://www.youtube.com/@it-coders
7. ВК группа: https://vk.com/science_geeks
"""

class Solution:
    def missingNumber(self, nums):
        """
        Находит пропущенное число в диапазоне [0, n] в массиве длины n.
        
        Args:
            nums: Массив длиной n, содержащий n различных чисел из диапазона [0, n]
            
        Returns:
            Единственное пропущенное число в диапазоне
            
        Примеры:
            >>> Solution().missingNumber([3,0,1])
            2
            >>> Solution().missingNumber([0,1])
            2
            >>> Solution().missingNumber([9,6,4,2,3,5,7,0,1])
            8
            
        Сложность:
            Время: O(n)
            Память: O(1)
        """
        n = len(nums)
        # Способ 1: Использование формулы суммы Гаусса
        expected_sum = n * (n + 1) // 2
        actual_sum = sum(nums)
        return expected_sum - actual_sum
        
        # Способ 2: Использование XOR (безопаснее для больших чисел)
        # result = len(nums)
        # for i, num in enumerate(nums):
        #     result ^= i ^ num
        # return result