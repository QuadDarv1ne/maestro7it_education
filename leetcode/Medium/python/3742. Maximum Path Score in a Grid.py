"""
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

class Solution:
    def maxPathScore(self, grid, k):
        """
        Находит максимальный счёт на пути из левого верхнего в правый нижний угол,
        двигаясь только вправо или вниз, при условии, что суммарная стоимость не превышает k.

        Значения ячеек:
        - 0: добавляет 0 очков, стоимость 0
        - 1: добавляет 1 очко, стоимость 1
        - 2: добавляет 2 очка, стоимость 1

        Если ни один путь не укладывается в бюджет k, возвращает -1.

        Аргументы:
            grid (List[List[int]]): матрица m x n, значения 0, 1 или 2.
            k (int): максимальная допустимая стоимость.

        Возвращает:
            int: максимальное количество очков, или -1, если путь невозможен.
        """
        m, n = len(grid), len(grid[0])
        # dp[i][j][c] = максимальный счёт в клетке (i,j) при точной стоимости c
        dp = [[[-1] * (k + 1) for _ in range(n)] for _ in range(m)]

        # начальная клетка
        start_cost = 0 if grid[0][0] == 0 else 1
        start_score = 0 if grid[0][0] == 0 else (1 if grid[0][0] == 1 else 2)
        if start_cost <= k:
            dp[0][0][start_cost] = start_score

        for i in range(m):
            for j in range(n):
                if i == 0 and j == 0:
                    continue
                add_cost = 0 if grid[i][j] == 0 else 1
                add_score = 0 if grid[i][j] == 0 else (1 if grid[i][j] == 1 else 2)

                # сверху
                if i > 0:
                    for prev_cost in range(k + 1 - add_cost):
                        if dp[i-1][j][prev_cost] != -1:
                            new_cost = prev_cost + add_cost
                            new_score = dp[i-1][j][prev_cost] + add_score
                            if new_score > dp[i][j][new_cost]:
                                dp[i][j][new_cost] = new_score
                # слева
                if j > 0:
                    for prev_cost in range(k + 1 - add_cost):
                        if dp[i][j-1][prev_cost] != -1:
                            new_cost = prev_cost + add_cost
                            new_score = dp[i][j-1][prev_cost] + add_score
                            if new_score > dp[i][j][new_cost]:
                                dp[i][j][new_cost] = new_score

        ans = -1
        for cost in range(k + 1):
            if dp[m-1][n-1][cost] > ans:
                ans = dp[m-1][n-1][cost]
        return ans