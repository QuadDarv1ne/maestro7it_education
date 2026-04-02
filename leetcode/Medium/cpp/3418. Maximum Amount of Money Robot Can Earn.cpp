/**
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Полезные ссылки:
 * 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
 * 2. Telegram №1 @quadd4rv1n7
 * 3. Telegram №2 @dupley_maxim_1999
 * 4. Rutube канал: https://rutube.ru/channel/4218729/
 * 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
 * 6. YouTube канал: https://www.youtube.com/@it-coders
 * 7. ВК группа: https://vk.com/science_geeks
 */

class Solution {
public:
    int maximumAmount(vector<vector<int>>& coins) {
        int m = coins.size(), n = coins[0].size();
        const int NEG_INF = -1e9;
        vector<vector<vector<int>>> dp(m, vector<vector<int>>(n, vector<int>(3, NEG_INF)));
        
        // Initialize starting cell
        for (int k = 0; k <= 2; k++) {
            if (coins[0][0] >= 0) {
                dp[0][0][k] = coins[0][0];
            } else {
                if (k == 0) dp[0][0][0] = coins[0][0];
                else dp[0][0][k] = 0;
            }
        }
        
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (i == 0 && j == 0) continue;
                
                for (int k = 0; k <= 2; k++) {
                    // From top
                    if (i > 0 && dp[i-1][j][k] > NEG_INF) {
                        int val = coins[i][j];
                        if (val >= 0) {
                            dp[i][j][k] = max(dp[i][j][k], dp[i-1][j][k] + val);
                        } else {
                            // Don't neutralize
                            dp[i][j][k] = max(dp[i][j][k], dp[i-1][j][k] + val);
                            // Neutralize
                            if (k > 0) {
                                dp[i][j][k] = max(dp[i][j][k], dp[i-1][j][k-1]);
                            }
                        }
                    }
                    
                    // From left
                    if (j > 0 && dp[i][j-1][k] > NEG_INF) {
                        int val = coins[i][j];
                        if (val >= 0) {
                            dp[i][j][k] = max(dp[i][j][k], dp[i][j-1][k] + val);
                        } else {
                            // Don't neutralize
                            dp[i][j][k] = max(dp[i][j][k], dp[i][j-1][k] + val);
                            // Neutralize
                            if (k > 0) {
                                dp[i][j][k] = max(dp[i][j][k], dp[i][j-1][k-1]);
                            }
                        }
                    }
                }
            }
        }
        
        return max({dp[m-1][n-1][0], dp[m-1][n-1][1], dp[m-1][n-1][2]});
    }
};