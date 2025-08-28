'''
https://leetcode.com/problems/sort-matrix-by-diagonals/description/?envType=daily-question&envId=2025-08-28
'''

class Solution(object):
    def sortMatrix(self, grid):
        """
        Сортировка диагоналей квадратной матрицы (LeetCode 3446).

        Правила:
        - Диагонали в нижне-левой треугольной части (включая главную) сортировать в
          не-увеличивающем порядке (по убыванию).
        - Диагонали в верхне-правой треугольной части сортировать в
          не-убывающем порядке (по возрастанию).

        :param grid: List[List[int]] — n x n матрица
        :return: List[List[int]] — модифицированная матрица
        """
        n = len(grid)
        if n == 0: 
            return grid

        # 1) Нижне-левая часть + главная диагональ:
        # стартуем с (n-1,0), (n-2,0), ..., (0,0)
        for start_row in range(n - 1, -1, -1):
            i, j = start_row, 0
            vals = []
            while i < n and j < n:
                vals.append(grid[i][j])
                i += 1; j += 1
            vals.sort(reverse=True)  # non-increasing
            i, j = start_row, 0
            k = 0
            while i < n and j < n:
                grid[i][j] = vals[k]
                k += 1; i += 1; j += 1

        # 2) Верхне-правая часть (кроме главной): стартуем с (0,1), (0,2), ..., (0,n-1)
        for start_col in range(1, n):
            i, j = 0, start_col
            vals = []
            while i < n and j < n:
                vals.append(grid[i][j])
                i += 1; j += 1
            vals.sort()  # non-decreasing
            i, j = 0, start_col
            k = 0
            while i < n and j < n:
                grid[i][j] = vals[k]
                k += 1; i += 1; j += 1

        return grid

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks