/**
 * https://leetcode.com/problems/regular-expression-matching/description/
 */

#include <string>
#include <vector>
using namespace std;

/**
 * @brief Проверяет, соответствует ли строка s шаблону p,
 * поддерживающему '.' и '*'.
 */
class Solution {
public:
    bool isMatch(string s, string p) {
        int m = s.size(), n = p.size();
        vector<vector<bool>> dp(m + 1, vector<bool>(n + 1, false));
        dp[0][0] = true;

        // Инициализация для шаблонов вида a*, a*b*, и т.д.
        for (int j = 1; j <= n; ++j) {
            if (p[j - 1] == '*') dp[0][j] = dp[0][j - 2];
        }

        for (int i = 1; i <= m; ++i) {
            for (int j = 1; j <= n; ++j) {
                if (p[j - 1] == s[i - 1] || p[j - 1] == '.') {
                    dp[i][j] = dp[i - 1][j - 1];
                } else if (p[j - 1] == '*') {
                    dp[i][j] = dp[i][j - 2] || 
                               ((p[j - 2] == s[i - 1] || p[j - 2] == '.') && dp[i - 1][j]);
                }
            }
        }
        return dp[m][n];
    }
};

/*
''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
*/