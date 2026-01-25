"""
LeetCode 1984. Minimum Difference Between Highest and Lowest of K Scores
https://leetcode.com/problems/minimum-difference-between-highest-and-lowest-of-k-scores

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

class Solution(object):
    def minimumDifference(self, nums, k):
        """
        Решение задачи LeetCode 1984 "Минимальная разница между наибольшим 
        и наименьшим значением среди K оценок".
        
        Алгоритм находит минимальную возможную разницу между наибольшим и 
        наименьшим значением в любой группе из k элементов массива.
        
        Параметры:
            nums: List[int] - массив целых чисел (оценки учащихся)
            k: int - количество элементов для выбора в группе
            
        Возвращает:
            int: Минимальная возможная разница между максимальным и 
                 минимальным значением в группе из k элементов
                 
        Алгоритм:
            1. Если k <= 1, возвращаем 0 (разница в группе из одного элемента равна 0)
            2. Сортируем массив по возрастанию
            3. Используем скользящее окно размера k для нахождения минимальной разницы
               между первым и последним элементом в каждом окне
            4. Возвращаем найденную минимальную разницу
               
        Сложность:
            Время: O(n log n) - доминирует операция сортировки
            Память: O(1) - сортировка на месте, O(n) в худшем случае для некоторых алгоритмов сортировки
            
        Примеры:
            >>> solution = Solution()
            >>> solution.minimumDifference([9, 4, 1, 7], 2)
            2
            
            >>> solution.minimumDifference([90], 1)
            0
            
            >>> solution.minimumDifference([1, 3, 5, 7, 9, 11], 4)
            6
            
        Обоснование корректности:
            После сортировки массива, минимальная разница в группе из k элементов 
            достигается на некотором непрерывном подмассиве длины k. Поэтому достаточно 
            рассмотреть все такие подмассивы и выбрать минимальную разницу между 
            их крайними элементами.
        """
        # Обработка тривиального случая
        if k <= 1:
            return 0
        
        # Сортируем массив для применения скользящего окна
        nums.sort()
        min_diff = float('inf')
        n = len(nums)
        
        # Проходим по всем возможным позициям окна длины k
        for i in range(n - k + 1):
            # Разница между максимальным и минимальным в текущем окне
            current_diff = nums[i + k - 1] - nums[i]
            if current_diff < min_diff:
                min_diff = current_diff
                
        return min_diff