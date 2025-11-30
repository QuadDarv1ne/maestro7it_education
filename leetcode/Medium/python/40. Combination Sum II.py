'''
https://leetcode.com/problems/combination-sum-ii/description/
Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Решение задачи "Combination Sum II"

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
    def combinationSum2(self, candidates, target):
        """
        :type candidates: List[int]
        :type target: int
        :rtype: List[List[int]]
        """
        result = []
        candidates.sort()  # Сортируем для обработки дубликатов
        
        def backtrack(start, current_combination, remaining):
            if remaining == 0:
                result.append(current_combination[:])
                return
            
            for i in range(start, len(candidates)):
                # Пропускаем дубликаты
                if i > start and candidates[i] == candidates[i-1]:
                    continue
                
                # Если текущий кандидат больше оставшейся суммы, прерываем
                if candidates[i] > remaining:
                    break
                
                current_combination.append(candidates[i])
                # Используем i+1 чтобы не использовать один элемент повторно
                backtrack(i + 1, current_combination, remaining - candidates[i])
                current_combination.pop()
        
        backtrack(0, [], target)
        return result