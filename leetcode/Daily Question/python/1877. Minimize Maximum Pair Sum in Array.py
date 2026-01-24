'''
https://leetcode.com/problems/maximum-matrix-sum/
Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Решение задачи "Maximum Matrix Sum"

Полезные ссылки:
1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
2. Telegram №1 @quadd4rv1n7
3. Telegram №2 @dupley_maxim_1999
4. Rutube канал: https://rutube.ru/channel/4218729/
5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
6. YouTube канал: https://www.youtube.com/@it-coders
7. ВК группа: https://vk.com/science_geeks
'''

class Solution:
    def minPairSum(self, nums):
        """
        Минимизирует максимальную сумму пары в массиве.
        
        Параметры:
            nums: Список целых чисел (длина четная)
            
        Возвращает:
            int: Минимально возможное значение максимальной суммы пары
                после оптимального разбиения массива на пары
            
        Алгоритм:
            1. Сортируем массив по возрастанию
            2. Формируем пары: первый с последним, второй с предпоследним и т.д.
            3. Находим максимальную сумму среди всех пар
            
        Пример:
            >>> s = Solution()
            >>> s.minPairSum([3, 5, 2, 3])
            7
            >>> s.minPairSum([3, 5, 4, 2, 4, 6])
            8
            
        Сложность:
            Время: O(n log n) - сортировка
            Память: O(1) (или O(n) для Timsort в худшем случае)
        """
        nums.sort()
        n = len(nums)
        max_sum = 0
        
        for i in range(n // 2):
            current_sum = nums[i] + nums[n - 1 - i]
            if current_sum > max_sum:
                max_sum = current_sum
        
        return max_sum