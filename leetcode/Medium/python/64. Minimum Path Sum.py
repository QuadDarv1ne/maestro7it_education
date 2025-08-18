'''
https://leetcode.com/problems/minimum-path-sum/description/
'''

class Solution:
    def minPathSum(self, grid):
        """
        Находит минимальную сумму пути из верхнего левого
        в нижний правый угол сетки, двигаясь только вправо или вниз.

        :param grid: m × n сетка неотрицательных чисел
        :return: минимальная сумма пути

        Алгоритм:
        dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1])

        Время: O(m * n)
        Память: O(m * n)
        """
        m, n = len(grid), len(grid[0])
        dp = [[0] * n for _ in range(m)]
        dp[0][0] = grid[0][0]

        for j in range(1, n):
            dp[0][j] = dp[0][j - 1] + grid[0][j]
        for i in range(1, m):
            dp[i][0] = dp[i - 1][0] + grid[i][0]
        for i in range(1, m):
            for j in range(1, n):
                dp[i][j] = grid[i][j] + min(dp[i - 1][j], dp[i][j - 1])

        return dp[m - 1][n - 1]

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks