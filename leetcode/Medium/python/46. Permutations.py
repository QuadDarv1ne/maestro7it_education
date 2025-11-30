'''
https://leetcode.com/problems/permutations/description/
Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Решение задачи "Permutations"

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
    def permute(self, nums):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """
        result = []
        
        def backtrack(start):
            # Если дошли до конца массива, добавляем текущую перестановку
            if start == len(nums):
                result.append(nums[:])
                return
            
            # Перебираем все элементы от start до конца
            for i in range(start, len(nums)):
                # Меняем местами текущий элемент и элемент на позиции start
                nums[start], nums[i] = nums[i], nums[start]
                # Рекурсивно генерируем перестановки для оставшейся части
                backtrack(start + 1)
                # Возвращаем обратно (backtrack)
                nums[start], nums[i] = nums[i], nums[start]
        
        backtrack(0)
        return result