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
    int numberOfStableArrays(int zero, int one, int limit) {
        const int MOD = 1e9 + 7;
        // dp[z][o][last][k]
        vector<vector<vector<vector<int>>>> dp(
            zero + 1, vector<vector<vector<int>>>(
                one + 1, vector<vector<int>>(
                    2, vector<int>(limit + 1, 0))));

        if (zero > 0) dp[1][0][0][1] = 1;
        if (one > 0) dp[0][1][1][1] = 1;

        for (int z = 0; z <= zero; ++z) {
            for (int o = 0; o <= one; ++o) {
                for (int last = 0; last < 2; ++last) {
                    for (int k = 1; k <= limit; ++k) {
                        int cur = dp[z][o][last][k];
                        if (cur == 0) continue;
                        // добавляем противоположный символ
                        if (last == 0) {
                            if (o + 1 <= one)
                                dp[z][o + 1][1][1] = (dp[z][o + 1][1][1] + cur) % MOD;
                        } else {
                            if (z + 1 <= zero)
                                dp[z + 1][o][0][1] = (dp[z + 1][o][0][1] + cur) % MOD;
                        }
                        // добавляем такой же символ
                        if (k < limit) {
                            if (last == 0 && z + 1 <= zero)
                                dp[z + 1][o][0][k + 1] = (dp[z + 1][o][0][k + 1] + cur) % MOD;
                            else if (last == 1 && o + 1 <= one)
                                dp[z][o + 1][1][k + 1] = (dp[z][o + 1][1][k + 1] + cur) % MOD;
                        }
                    }
                }
            }
        }

        int ans = 0;
        for (int last = 0; last < 2; ++last)
            for (int k = 1; k <= limit; ++k)
                ans = (ans + dp[zero][one][last][k]) % MOD;
        return ans;
    }
};
