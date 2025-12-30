'''
https://leetcode.com/problems/magic-squares-in-grid/description/
Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Решение задачи "Magic Squares In Grid"

Полезные ссылки:
1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
2. Telegram №1 @quadd4rv1n7
3. Telegram №2 @dupley_maxim_1999
4. Rutube канал: https://rutube.ru/channel/4218729/
5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
6. YouTube канал: https://www.youtube.com/@it-coders
7. ВК группа: https://vk.com/science_geeks
'''

from typing import List

class Solution:
    def numMagicSquaresInside(self, grid):
        """
        Подсчитывает количество магических квадратов 3x3 в заданной сетке.
        
        Args:
            grid: двумерный массив целых чисел
            
        Returns:
            Количество магических квадратов 3x3 в сетке
            
        Магический квадрат 3x3 должен удовлетворять:
        1. Содержать все числа от 1 до 9 (без повторений)
        2. Суммы строк, столбцов и диагоналей равны 15
        """
        def is_magic(r, c):
            """
            Проверяет, является ли подматрица 3x3 магическим квадратом.
            
            Args:
                r: начальная строка
                c: начальный столбец
                
            Returns:
                True если подматрица является магическим квадратом
            """
            # Проверяем, что все числа от 1 до 9 без повторений
            nums = set()
            for i in range(3):
                for j in range(3):
                    num = grid[r + i][c + j]
                    if num < 1 or num > 9:
                        return False
                    nums.add(num)
            
            if len(nums) != 9:
                return False
            
            # Проверяем суммы строк (должны быть равны 15)
            for i in range(3):
                if sum(grid[r + i][c + j] for j in range(3)) != 15:
                    return False
            
            # Проверяем суммы столбцов
            for j in range(3):
                if sum(grid[r + i][c + j] for i in range(3)) != 15:
                    return False
            
            # Проверяем диагонали
            diag1 = grid[r][c] + grid[r + 1][c + 1] + grid[r + 2][c + 2]
            diag2 = grid[r][c + 2] + grid[r + 1][c + 1] + grid[r + 2][c]
            
            return diag1 == 15 and diag2 == 15
        
        rows = len(grid)
        cols = len(grid[0])
        
        # Если сетка меньше чем 3x3, не может быть магических квадратов
        if rows < 3 or cols < 3:
            return 0
        
        count = 0
        
        # Перебираем все возможные левые верхние углы квадратов 3x3
        for r in range(rows - 2):
            for c in range(cols - 2):
                # Оптимизация: центр магического квадрата 3x3 всегда должен быть 5
                if grid[r + 1][c + 1] != 5:
                    continue
                if is_magic(r, c):
                    count += 1
        
        return count