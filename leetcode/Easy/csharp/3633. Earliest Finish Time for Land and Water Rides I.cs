/**
 * https://leetcode.com/problems/house-robber-ii/description/
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

using System;
using System.Collections.Generic;
using System.Linq;

public class Solution {
    public int EarliestFinishTime(int[] landStartTime, int[] landDuration, 
                                  int[] waterStartTime, int[] waterDuration) {
        var landData = PrepareData(landStartTime, landDuration);
        var waterData = PrepareData(waterStartTime, waterDuration);
        
        long ans = long.MaxValue;
        
        foreach (var land in landData.Data) {
            long eL = land[1];
            long opt1a = MinEndAfter(waterData, eL);
            long opt1bDur = MinDurAtOrBefore(waterData, eL);
            long opt1b = opt1bDur == long.MaxValue ? long.MaxValue : eL + opt1bDur;
            ans = Math.Min(ans, Math.Min(opt1a, opt1b));
        }
        
        foreach (var water in waterData.Data) {
            long eW = water[1];
            long opt2a = MinEndAfter(landData, eW);
            long opt2bDur = MinDurAtOrBefore(landData, eW);
            long opt2b = opt2bDur == long.MaxValue ? long.MaxValue : eW + opt2bDur;
            ans = Math.Min(ans, Math.Min(opt2a, opt2b));
        }
        
        return (int)ans;
    }
    
    private (List<long[]> Data, long[] Suffix, long[] Prefix) PrepareData(int[] starts, int[] durs) {
        var data = new List<long[]>();
        for (int i = 0; i < starts.Length; i++) data.Add(new long[] { starts[i], (long)starts[i] + durs[i], durs[i] });
        data.Sort((a, b) => a[0].CompareTo(b[0]));
        
        int n = data.Count;
        var suffix = new long[n];
        var prefix = new long[n];
        if (n > 0) {
            suffix[n - 1] = data[n - 1][1];
            for (int i = n - 2; i >= 0; i--) suffix[i] = Math.Min(data[i][1], suffix[i + 1]);
            prefix[0] = data[0][2];
            for (int i = 1; i < n; i++) prefix[i] = Math.Min(data[i][2], prefix[i - 1]);
        }
        return (data, suffix, prefix);
    }
    
    private long MinEndAfter((List<long[]> Data, long[] Suffix, long[] Prefix) prep, long T) {
        int lo = 0, hi = prep.Data.Count;
        while (lo < hi) { int mid = lo + (hi - lo) / 2; if (prep.Data[mid][0] < T) lo = mid + 1; else hi = mid; }
        return lo == prep.Data.Count ? long.MaxValue : prep.Suffix[lo];
    }
    
    private long MinDurAtOrBefore((List<long[]> Data, long[] Suffix, long[] Prefix) prep, long T) {
        int lo = 0, hi = prep.Data.Count;
        while (lo < hi) { int mid = lo + (hi - lo) / 2; if (prep.Data[mid][0] <= T) lo = mid + 1; else hi = mid; }
        return lo == 0 ? long.MaxValue : prep.Prefix[lo - 1];
    }
}