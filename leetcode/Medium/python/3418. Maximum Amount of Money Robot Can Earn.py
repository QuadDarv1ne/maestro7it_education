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
    def maximumAmount(self, coins):
        m, n = len(coins), len(coins[0])
        NEG_INF = -10**9
        
        # dp[i][j][k] = max coins at (i,j) with k neutralizations used
        dp = [[[NEG_INF] * 3 for _ in range(n)] for _ in range(m)]
        
        # Initialize starting cell
        for k in range(3):
            if coins[0][0] >= 0:
                dp[0][0][k] = coins[0][0]
            else:
                if k == 0:
                    dp[0][0][0] = coins[0][0]  # can't neutralize, take loss
                else:
                    dp[0][0][k] = 0  # neutralize, get 0
        
        for i in range(m):
            for j in range(n):
                if i == 0 and j == 0:
                    continue
                    
                for k in range(3):
                    # Try coming from top
                    if i > 0 and dp[i-1][j][k] > NEG_INF:
                        val = coins[i][j]
                        if val >= 0:
                            dp[i][j][k] = max(dp[i][j][k], dp[i-1][j][k] + val)
                        else:
                            # Don't neutralize
                            dp[i][j][k] = max(dp[i][j][k], dp[i-1][j][k] + val)
                            # Neutralize (if we have neutralizations left)
                            if k > 0:
                                dp[i][j][k] = max(dp[i][j][k], dp[i-1][j][k-1])
                    
                    # Try coming from left
                    if j > 0 and dp[i][j-1][k] > NEG_INF:
                        val = coins[i][j]
                        if val >= 0:
                            dp[i][j][k] = max(dp[i][j][k], dp[i][j-1][k] + val)
                        else:
                            # Don't neutralize
                            dp[i][j][k] = max(dp[i][j][k], dp[i][j-1][k] + val)
                            # Neutralize (if we have neutralizations left)
                            if k > 0:
                                dp[i][j][k] = max(dp[i][j][k], dp[i][j-1][k-1])
        
        return max(dp[m-1][n-1])