/**
 * https://leetcode.com/problems/unique-paths/description/
 */
class Solution {
    /**
     * Вычисляет количество уникальных путей в сетке m x n,
     * двигаясь только вниз и вправо.
     *
     * @param m количество строк
     * @param n количество столбцов
     * @return количество уникальных путей
     *
     * Алгоритм:
     * Используется динамическое программирование.
     * dp[i][j] = dp[i-1][j] + dp[i][j-1]
     *
     * Время: O(m*n)
     * Память: O(m*n)
     */
    public int uniquePaths(int m, int n) {
        int[][] dp = new int[m][n];
        dp[0][0] = 1;

        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (i > 0) dp[i][j] += dp[i - 1][j];
                if (j > 0) dp[i][j] += dp[i][j - 1];
            }
        }

        return dp[m - 1][n - 1];
    }
}

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