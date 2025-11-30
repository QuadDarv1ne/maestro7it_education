'''
https://leetcode.com/problems/combination-sum/description/
Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Решение задачи "Combination Sum"

Полезные ссылки:
1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
2. Telegram №1 @quadd4rv1n7
3. Telegram №2 @dupley_maxim_1999
4. Rutube канал: https://rutube.ru/channel/4218729/
5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
6. YouTube канал: https://www.youtube.com/@it-coders
7. ВК группа: https://vk.com/science_geeks
'''

class Solution(object):
    def combinationSum(self, candidates, target):
        """
        :type candidates: List[int]
        :type target: int
        :rtype: List[List[int]]
        """
        result = []
        
        def backtrack(start, current_combination, current_sum):
            # Если текущая сумма равна целевой, добавляем комбинацию в результат
            if current_sum == target:
                result.append(current_combination[:])  # Создаем копию списка
                return
            
            # Если текущая сумма превысила целевую, прекращаем рекурсию
            if current_sum > target:
                return
            
            # Перебираем кандидатов, начиная с текущего индекса
            for i in range(start, len(candidates)):
                # Добавляем кандидата в текущую комбинацию
                current_combination.append(candidates[i])
                # Рекурсивно вызываем backtrack с тем же стартовым индексом (разрешены повторы)
                backtrack(i, current_combination, current_sum + candidates[i])
                # Удаляем последний элемент (backtrack)
                current_combination.pop()
        
        # Начинаем backtrack с пустой комбинации и нулевой суммы
        backtrack(0, [], 0)
        return result