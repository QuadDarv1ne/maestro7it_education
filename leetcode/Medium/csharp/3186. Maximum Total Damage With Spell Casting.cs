/**
 * https://leetcode.com/problems/maximum-total-damage-with-spell-casting/?envType=daily-question&envId=2025-10-11
 */

using System;
using System.Collections.Generic;
using System.Linq;

public class Solution {
    public long MaximumTotalDamage(int[] power) {
        var cnt = power.GroupBy(x => x).ToDictionary(g => g.Key, g => g.Count());
        var uniq = cnt.Keys.OrderBy(x => x).ToList();
        int n = uniq.Count;

        int[] nxt = new int[n];
        for (int i = 0; i < n; i++) {
            int j = uniq.BinarySearch(uniq[i] + 3);
            if (j < 0) j = ~j;
            nxt[i] = j;
        }

        long[] dp = new long[n + 1];
        for (int i = n - 1; i >= 0; i--) {
            long skip = dp[i + 1];
            long take = (long)uniq[i] * cnt[uniq[i]] + dp[nxt[i]];
            dp[i] = Math.Max(skip, take);
        }
        return dp[0];
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