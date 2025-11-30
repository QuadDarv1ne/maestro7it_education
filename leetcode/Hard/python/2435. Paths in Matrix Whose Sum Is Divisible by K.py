'''
Решение задачи "Number of Paths"
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
'''

class Solution:
    def numberOfPaths(self, grid, k):
        """
        Вычисляет количество путей от левого верхнего угла до правого нижнего угла сетки,
        где сумма чисел по пути делится на k.
        
        Args:
            grid (List[List[int]]): Двумерная сетка с числами
            k (int): Делитель
            
        Returns:
            int: Количество путей, удовлетворяющих условию
            
        Time Complexity: O(m * n * k)
        Space Complexity: O(m * n * k)
        """
        MOD = 10**9 + 7
        m, n = len(grid), len(grid[0])
        
        # DP таблица: dp[i][j][r] - количество путей до (i,j) с остатком r
        dp = [[[0] * k for _ in range(n)] for _ in range(m)]
        
        # Инициализация начальной точки
        dp[0][0][grid[0][0] % k] = 1
        
        for i in range(m):
            for j in range(n):
                for r in range(k):
                    if dp[i][j][r] > 0:
                        # Движение вправо
                        if j + 1 < n:
                            new_r = (r + grid[i][j+1]) % k
                            dp[i][j+1][new_r] = (dp[i][j+1][new_r] + dp[i][j][r]) % MOD
                        # Движение вниз
                        if i + 1 < m:
                            new_r = (r + grid[i+1][j]) % k
                            dp[i+1][j][new_r] = (dp[i+1][j][new_r] + dp[i][j][r]) % MOD
        
        return dp[m-1][n-1][0] % MOD