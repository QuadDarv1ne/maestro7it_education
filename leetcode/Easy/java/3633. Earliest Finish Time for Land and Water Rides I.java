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

import java.util.*;

class Solution {
    public int earliestFinishTime(int[] landStartTime, int[] landDuration, 
                                  int[] waterStartTime, int[] waterDuration) {
        long[][] landData = prepareData(landStartTime, landDuration);
        long[][] waterData = prepareData(waterStartTime, waterDuration);
        
        long[] landSuffix = buildSuffix(landData);
        long[] landPrefix = buildPrefix(landData);
        long[] waterSuffix = buildSuffix(waterData);
        long[] waterPrefix = buildPrefix(waterData);
        
        long ans = Long.MAX_VALUE;
        
        for (long[] land : landData) {
            long eL = land[1];
            long opt1a = minEndAfter(waterData, waterSuffix, eL);
            long opt1bDur = minDurAtOrBefore(waterData, waterPrefix, eL);
            long opt1b = (opt1bDur == Long.MAX_VALUE) ? Long.MAX_VALUE : eL + opt1bDur;
            ans = Math.min(ans, Math.min(opt1a, opt1b));
        }
        
        for (long[] water : waterData) {
            long eW = water[1];
            long opt2a = minEndAfter(landData, landSuffix, eW);
            long opt2bDur = minDurAtOrBefore(landData, landPrefix, eW);
            long opt2b = (opt2bDur == Long.MAX_VALUE) ? Long.MAX_VALUE : eW + opt2bDur;
            ans = Math.min(ans, Math.min(opt2a, opt2b));
        }
        
        return (int)ans;
    }
    
    private long[][] prepareData(int[] starts, int[] durs) {
        long[][] data = new long[starts.length][3];
        for (int i = 0; i < starts.length; i++) {
            data[i][0] = starts[i];
            data[i][1] = (long)starts[i] + durs[i];
            data[i][2] = durs[i];
        }
        Arrays.sort(data, (a, b) -> Long.compare(a[0], b[0]));
        return data;
    }
    
    private long[] buildSuffix(long[][] data) {
        long[] suffix = new long[data.length];
        suffix[data.length - 1] = data[data.length - 1][1];
        for (int i = data.length - 2; i >= 0; i--) suffix[i] = Math.min(data[i][1], suffix[i + 1]);
        return suffix;
    }
    
    private long[] buildPrefix(long[][] data) {
        long[] prefix = new long[data.length];
        prefix[0] = data[0][2];
        for (int i = 1; i < data.length; i++) prefix[i] = Math.min(data[i][2], prefix[i - 1]);
        return prefix;
    }
    
    private long minEndAfter(long[][] data, long[] suffix, long T) {
        int lo = 0, hi = data.length;
        while (lo < hi) { int mid = lo + (hi - lo) / 2; if (data[mid][0] < T) lo = mid + 1; else hi = mid; }
        return lo == data.length ? Long.MAX_VALUE : suffix[lo];
    }
    
    private long minDurAtOrBefore(long[][] data, long[] prefix, long T) {
        int lo = 0, hi = data.length;
        while (lo < hi) { int mid = lo + (hi - lo) / 2; if (data[mid][0] <= T) lo = mid + 1; else hi = mid; }
        return lo == 0 ? Long.MAX_VALUE : prefix[lo - 1];
    }
}