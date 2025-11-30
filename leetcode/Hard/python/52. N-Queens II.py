'''
https://leetcode.com/problems/n-queens-ii/description/
Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Решение задачи "N-Queens II"

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
    def totalNQueens(self, n):
        """
        :type n: int
        :rtype: int
        """
        def backtrack(row, cols, diagonals, anti_diagonals):
            # Базовый случай: все ферзи размещены
            if row == n:
                return 1
            
            count = 0
            for col in range(n):
                curr_diagonal = row - col
                curr_anti_diagonal = row + col
                
                # Если позиция под атакой, пропускаем
                if (col in cols or 
                    curr_diagonal in diagonals or 
                    curr_anti_diagonal in anti_diagonals):
                    continue
                
                # Размещаем ферзя
                cols.add(col)
                diagonals.add(curr_diagonal)
                anti_diagonals.add(curr_anti_diagonal)
                
                # Рекурсивно считаем решения для следующей строки
                count += backtrack(row + 1, cols, diagonals, anti_diagonals)
                
                # Убираем ферзя (backtrack)
                cols.remove(col)
                diagonals.remove(curr_diagonal)
                anti_diagonals.remove(curr_anti_diagonal)
            
            return count
        
        return backtrack(0, set(), set(), set())