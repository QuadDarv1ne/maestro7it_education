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

public class Solution {
    public long MaximumScore(int[][] grid) {
        int n = grid.Length;
        long[][] prefix = new long[n][];
        for (int j = 0; j < n; j++) {
            prefix[j] = new long[n + 1];
            for (int i = 0; i < n; i++) {
                prefix[j][i + 1] = prefix[j][i] + grid[i][j];
            }
        }

        long[] prevPick = new long[n + 1];
        long[] prevSkip = new long[n + 1];

        for (int j = 1; j < n; j++) {
            long[] currPick = new long[n + 1];
            long[] currSkip = new long[n + 1];

            for (int curr = 0; curr <= n; curr++) {
                for (int prev = 0; prev <= n; prev++) {
                    if (curr > prev) {
                        long score = prefix[j - 1][curr] - prefix[j - 1][prev];
                        currPick[curr] = Math.Max(currPick[curr], prevSkip[prev] + score);
                        currSkip[curr] = Math.Max(currSkip[curr], prevSkip[prev] + score);
                    } else {
                        long score = prefix[j][prev] - prefix[j][curr];
                        currPick[curr] = Math.Max(currPick[curr], prevPick[prev] + score);
                        currSkip[curr] = Math.Max(currSkip[curr], prevPick[prev]);
                    }
                }
            }
            prevPick = currPick;
            prevSkip = currSkip;
        }

        long ans = 0;
        foreach (long val in prevPick) {
            ans = Math.Max(ans, val);
        }
        return ans;
    }
}