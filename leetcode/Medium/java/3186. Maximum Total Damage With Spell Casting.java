/**
 * https://leetcode.com/problems/maximum-total-damage-with-spell-casting/?envType=daily-question&envId=2025-10-11
 */

import java.util.*;

class Solution {
    public long maximumTotalDamage(int[] power) {
        Map<Integer, Integer> cnt = new HashMap<>();
        for (int p : power) cnt.put(p, cnt.getOrDefault(p, 0) + 1);
        List<Integer> uniq = new ArrayList<>(cnt.keySet());
        Collections.sort(uniq);
        int n = uniq.size();

        int[] nxt = new int[n];
        for (int i = 0; i < n; i++) {
            int target = uniq.get(i) + 2;
            int j = Collections.binarySearch(uniq, target + 1);
            if (j < 0) j = -j - 1;
            nxt[i] = j;
        }

        long[] dp = new long[n + 1];
        for (int i = n - 1; i >= 0; i--) {
            long skip = dp[i + 1];
            long take = (long) uniq.get(i) * cnt.get(uniq.get(i)) + dp[nxt[i]];
            dp[i] = Math.max(skip, take);
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