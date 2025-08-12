/**
 * https://leetcode.com/problems/ways-to-express-an-integer-as-sum-of-powers/description/?envType=daily-question&envId=2025-08-12
 */

public class Solution {
    private static final int MOD = 1000000007;

    /**
     * Находит количество способов представить число n как сумму уникальных целых чисел,
     * возведённых в степень x.
     *
     * @param n Целое число, которое нужно представить.
     * @param x Степень, в которую возводятся числа.
     * @return Количество способов представить n как сумму степеней чисел.
     */
    public int numberOfWays(int n, int x) {
        int[][] dp = new int[n + 1][n + 1];
        for (int[] row : dp) {
            Arrays.fill(row, -1);
        }
        return dfs(n, n, x, dp);
    }

    private int dfs(int i, int remaining, int x, int[][] dp) {
        if (remaining == 0) return 1;
        if (i == 0 || remaining < 0) return 0;
        if (dp[i][remaining] != -1) return dp[i][remaining];

        int include = dfs(i - 1, remaining - (int) Math.pow(i, x), x, dp);
        int exclude = dfs(i - 1, remaining, x, dp);

        dp[i][remaining] = (include + exclude) % MOD;
        return dp[i][remaining];
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