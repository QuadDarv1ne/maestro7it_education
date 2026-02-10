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
    def longestBalanced(self, nums):
        """
        Возвращает длину самого длинного сбалансированного подмассива.

        Параметры:
            nums (List[int]): Входной массив целых чисел.

        Возвращает:
            int: Длина самого длинного подмассива, в котором количество
                уникальных четных чисел равно количеству уникальных нечетных.

        Примеры:
            >>> Solution().longestBalanced([2,5,4,3])
            4
            >>> Solution().longestBalanced([3,2,2,5,4])
            5
            >>> Solution().longestBalanced([1,2,3,2])
            3
        """
        n = len(nums)
        max_len = 0
        
        for i in range(n):
            even_set = set()
            odd_set = set()
            
            for j in range(i, n):
                if nums[j] % 2 == 0:
                    even_set.add(nums[j])
                else:
                    odd_set.add(nums[j])
                
                if len(even_set) == len(odd_set):
                    max_len = max(max_len, j - i + 1)
        
        return max_len