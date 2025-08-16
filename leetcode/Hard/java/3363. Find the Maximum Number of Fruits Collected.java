/**
 * https://leetcode.com/problems/find-the-maximum-number-of-fruits-collected/description/?envType=daily-question&envId=2025-08-16
 */

class Solution {
    public int maxCollectedFruits(int[][] fruits) {
        int n = fruits.length;
        final int INF = Integer.MIN_VALUE / 2;
        int[][] f2 = new int[n][n], f3 = new int[n][n];
        for (int[] row : f2) Arrays.fill(row, INF);
        for (int[] row : f3) Arrays.fill(row, INF);

        f2[0][n-1] = fruits[0][n-1];
        for (int i = 1; i < n; i++)
            for (int j = i+1; j < n; j++) {
                int best = Math.max(f2[i-1][j], f2[i-1][j-1]);
                if (j+1<n) best = Math.max(best, f2[i-1][j+1]);
                f2[i][j] = best + fruits[i][j];
            }

        f3[n-1][0] = fruits[n-1][0];
        for (int j = 1; j < n; j++)
            for (int i = j+1; i < n; i++) {
                int best = Math.max(f3[i][j-1], f3[i-1][j-1]);
                if (i+1<n) best = Math.max(best, f3[i+1][j-1]);
                f3[i][j] = best + fruits[i][j];
            }

        int diag = 0;
        for (int i = 0; i < n; i++) diag += fruits[i][i];
        return diag + f2[n-2][n-1] + f3[n-1][n-2];
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