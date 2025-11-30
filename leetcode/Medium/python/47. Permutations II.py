'''
https://leetcode.com/problems/permutations-ii/description/
Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Решение задачи "Permutations II"

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
    def permuteUnique(self, nums):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """
        result = []
        nums.sort()  # Сортируем для обработки дубликатов
        
        def backtrack(current, used):
            # Если текущая перестановка завершена
            if len(current) == len(nums):
                result.append(current[:])
                return
            
            for i in range(len(nums)):
                # Пропускаем использованные элементы
                if used[i]:
                    continue
                
                # Пропускаем дубликаты: если текущий элемент равен предыдущему и предыдущий не использован
                if i > 0 and nums[i] == nums[i-1] and not used[i-1]:
                    continue
                
                used[i] = True
                current.append(nums[i])
                backtrack(current, used)
                # Backtrack
                current.pop()
                used[i] = False
        
        backtrack([], [False] * len(nums))
        return result