/*
https://leetcode.com/problems/scramble-string/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

class Solution {
public:
    bool isScramble(string s1, string s2) {
        int n = s1.size();
        if (n != s2.size()) return false;

        // Частотная проверка
        vector<int> cnt(26,0);
        for (int i = 0; i < n; i++) {
            cnt[s1[i]-'a']++;
            cnt[s2[i]-'a']--;
        }
        for (int c : cnt) {
            if (c != 0) return false;
        }

        // 3D DP: dp[i][j][len]
        vector<vector<vector<bool>>> dp(
            n, vector<vector<bool>>(n, vector<bool>(n+1,false))
        );

        // Инициализация для длины 1
        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++)
                dp[i][j][1] = (s1[i] == s2[j]);

        // Заполняем по увеличению длины
        for (int len = 2; len <= n; len++) {
            for (int i = 0; i+len <= n; i++) {
                for (int j = 0; j+len <= n; j++) {
                    for (int k = 1; k < len; k++) {
                        if ((dp[i][j][k] && dp[i+k][j+k][len-k]) ||
                            (dp[i][j+len-k][k] && dp[i+k][j][len-k])) {
                            dp[i][j][len] = true;
                            break;
                        }
                    }
                }
            }
        }
        return dp[0][0][n];
    }
};
