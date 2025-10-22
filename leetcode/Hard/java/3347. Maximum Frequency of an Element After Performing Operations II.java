/*
Задача: Maximum Frequency of an Element After Performing Operations II
Источник: https://leetcode.com/problems/maximum-frequency-of-an-element-after-performing-operations-ii/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X  
GitHub: https://github.com/QuadDarv1ne/
*/

import java.util.*;

public class Solution {
    public int maxFrequency(int[] nums, int k, int numOperations) {
        if (nums == null || nums.length == 0) return 0;
        int n = nums.length;
        long[] a = new long[n];
        for (int i = 0; i < n; ++i) a[i] = nums[i];
        Arrays.sort(a);

        Map<Long,Integer> freq = new HashMap<>();
        for (long x : a) freq.put(x, freq.getOrDefault(x, 0) + 1);

        int ans = 1;
        ArrayList<Long> unique = new ArrayList<>(freq.keySet());
        Collections.sort(unique);

        // 1) для каждого существующего значения v
        for (long v : unique) {
            long leftVal = v - (long)k;
            long rightVal = v + (long)k;
            int L = lowerBound(a, leftVal);
            int R = upperBound(a, rightVal);
            int cover = R - L;
            int candidate = Math.min(cover, freq.get(v) + numOperations);
            ans = Math.max(ans, candidate);
        }

        // 2) sweep по отрезкам [a-k, a+k] для поиска точки с максимальным покрытием
        int m = 2 * n;
        long[] evPos = new long[m];
        int[] evDelta = new int[m];
        int idx = 0;
        for (long x : a) {
            evPos[idx] = x - k; evDelta[idx] = 1; idx++;
            evPos[idx] = x + k + 1; evDelta[idx] = -1; idx++;
        }

        Integer[] ord = new Integer[m];
        for (int i = 0; i < m; ++i) ord[i] = i;
        Arrays.sort(ord, (i, j) -> {
            int c = Long.compare(evPos[i], evPos[j]);
            if (c != 0) return c;
            return Integer.compare(evDelta[i], evDelta[j]);
        });

        int cur = 0, maxCover = 0;
        for (int id : ord) {
            cur += evDelta[id];
            if (cur > maxCover) maxCover = cur;
        }

        int candidate2 = Math.min(maxCover, numOperations);
        ans = Math.max(ans, candidate2);

        return ans;
    }

    private static int lowerBound(long[] a, long x) {
        int l = 0, r = a.length;
        while (l < r) {
            int m = (l + r) >>> 1;
            if (a[m] < x) l = m + 1; else r = m;
        }
        return l;
    }

    private static int upperBound(long[] a, long x) {
        int l = 0, r = a.length;
        while (l < r) {
            int m = (l + r) >>> 1;
            if (a[m] <= x) l = m + 1; else r = m;
        }
        return l;
    }
}

/*
Полезные ссылки:
1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
2. Telegram №1 @quadd4rv1n7
3. Telegram №2 @dupley_maxim_1999
4. Rutube канал: https://rutube.ru/channel/4218729/
5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
6. YouTube канал: https://www.youtube.com/@it-coders
7. ВК группа: https://vk.com/science_geeks
8. Официальный сайт школы Maestro7IT: https://school-maestro7it.ru/
*/