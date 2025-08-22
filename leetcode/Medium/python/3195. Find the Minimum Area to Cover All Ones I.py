'''
https://leetcode.com/problems/find-the-minimum-area-to-cover-all-ones-i/description/?envType=daily-question&envId=2025-08-22
'''

# from math import inf
# from typing import List

class Solution:
    # def minimumArea(self, grid: List[List[int]]) -> int:
    def minimumArea(self, grid):
        """
        Функция вычисляет минимальную площадь прямоугольника, покрывающего все единицы в матрице.
        
        Алгоритм:
        1. Находим минимальные и максимальные индексы строк и столбцов, где встречается '1'.
        2. Вычисляем площадь прямоугольника как:
           (maxRow - minRow + 1) * (maxCol - minCol + 1).
        3. Если в матрице нет '1', возвращаем 0.

        Сложность:
        - Время: O(m * n), где m и n — размеры матрицы.
        - Память: O(1).
        """
        m, n = len(grid), len(grid[0])
        min_r, min_c = float('inf'), float('inf')
        max_r, max_c = -1, -1

        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:
                    min_r = min(min_r, i)
                    min_c = min(min_c, j)
                    max_r = max(max_r, i)
                    max_c = max(max_c, j)

        return 0 if max_r == -1 else (max_r - min_r + 1) * (max_c - min_c + 1)

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks