/*
Задача: Maximum Frequency of an Element After Performing Operations II
Источник: https://leetcode.com/problems/maximum-frequency-of-an-element-after-performing-operations-ii/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

using System;
using System.Collections.Generic;

public class Solution {
    static int LowerBound(long[] a, long x) {
        int l = 0, r = a.Length;
        while (l < r) {
            int m = (l + r) >> 1;
            if (a[m] < x) l = m + 1; else r = m;
        }
        return l;
    }
    static int UpperBound(long[] a, long x) {
        int l = 0, r = a.Length;
        while (l < r) {
            int m = (l + r) >> 1;
            if (a[m] <= x) l = m + 1; else r = m;
        }
        return l;
    }

    // Метод, который ожидает judge: nums, k, numOperations
    public int MaxFrequency(int[] nums, int k, int numOperations) {
        if (nums == null || nums.Length == 0) return 0;
        int n = nums.Length;
        long[] a = new long[n];
        for (int i = 0; i < n; ++i) a[i] = nums[i];
        Array.Sort(a);

        var freq = new Dictionary<long,int>();
        foreach (long x in a) freq[x] = freq.ContainsKey(x) ? freq[x] + 1 : 1;

        int ans = 1;
        var unique = new List<long>(freq.Keys);
        unique.Sort();

        // 1) проверка для каждого существующего значения v
        foreach (long v in unique) {
            long leftVal = v - (long)k;
            long rightVal = v + (long)k;
            int L = LowerBound(a, leftVal);
            int R = UpperBound(a, rightVal);
            int cover = R - L;
            int candidate = Math.Min(cover, freq[v] + numOperations);
            if (candidate > ans) ans = candidate;
        }

        // 2) sweep по отрезкам [a-k, a+k] — найти точку с максимальным покрытием
        var events = new List<KeyValuePair<long,int>>(2 * n);
        foreach (long x in a) {
            events.Add(new KeyValuePair<long,int>(x - k, 1));
            events.Add(new KeyValuePair<long,int>(x + k + 1, -1)); // end inclusive -> decrement at end+1
        }
        events.Sort((p,q) => {
            int c = p.Key.CompareTo(q.Key);
            if (c != 0) return c;
            return p.Value.CompareTo(q.Value);
        });

        int cur = 0, maxCover = 0;
        foreach (var ev in events) {
            cur += ev.Value;
            if (cur > maxCover) maxCover = cur;
        }

        int candidate2 = Math.Min(maxCover, numOperations);
        ans = Math.Max(ans, candidate2);

        return ans;
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