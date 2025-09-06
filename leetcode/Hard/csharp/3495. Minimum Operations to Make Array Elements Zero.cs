/**
 * https://leetcode.com/problems/minimum-operations-to-make-array-elements-zero/description/?envType=daily-question&envId=2025-09-06
 */

public class Solution {
    /// <summary>
    /// Задача: Для каждого диапазона [l, r] подсчитать количество операций,
    /// чтобы сделать все элементы нулями (заменяя пары чисел на floor(a/4), floor(b/4)).
    /// Возвращается сумма минимальных операций по всем запросам.
    /// </summary>
    public long MinOperations(int[][] queries) {
        long ans = 0;
        foreach (var q in queries) {
            int l = q[0], r = q[1];
            ans += (GetOps(r) - GetOps(l - 1) + 1) / 2;
        }
        return ans;
    }

    private long GetOps(int n) {
        long res = 0;
        long ops = 0, pw = 1;
        while (pw <= n) {
            long l = pw;
            long r = Math.Min(n, pw * 4 - 1);
            ops++;
            res += (r - l + 1) * ops;
            pw *= 4;
        }
        return res;
    }
}

/*
''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
*/