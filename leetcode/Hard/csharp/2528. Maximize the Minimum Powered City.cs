/*
https://leetcode.com/problems/maximize-the-minimum-powered-city/?envType=daily-question&envId=2025-11-07

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

using System;
using System.Linq;

public class Solution {
    public long MaxPower(int[] stations, int r, int k) {
        int n = stations.Length;
        long[] diff = new long[n + 1];
        
        for (int i = 0; i < n; i++) {
            int left = Math.Max(0, i - r);
            int right = Math.Min(n - 1, i + r);
            diff[left] += stations[i];
            diff[right + 1] -= stations[i];
        }
        
        long[] power = new long[n];
        power[0] = diff[0];
        for (int i = 1; i < n; i++) {
            power[i] = power[i - 1] + diff[i];
        }
        
        bool CanAchieve(long target) {
            long[] addDiff = new long[n + 1];
            long currAdd = 0;
            long used = 0;
            
            for (int i = 0; i < n; i++) {
                currAdd += addDiff[i];
                long total = power[i] + currAdd;
                if (total < target) {
                    long need = target - total;
                    used += need;
                    if (used > k) return false;
                    
                    int j = Math.Min(i + r, n - 1);
                    currAdd += need;
                    int end = j + r + 1;
                    if (end < n) addDiff[end] -= need;
                }
            }
            return true;
        }
        
        long lo = power.Min();
        long hi = power.Max() + k;
        long ans = lo;
        
        while (lo <= hi) {
            long mid = lo + (hi - lo) / 2;
            if (CanAchieve(mid)) {
                ans = mid;
                lo = mid + 1;
            } else {
                hi = mid - 1;
            }
        }
        return ans;
    }
}

/* Полезные ссылки:
 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
 2. Telegram №1 @quadd4rv1n7
 3. Telegram №2 @dupley_maxim_1999
 4. Rutube канал: https://rutube.ru/channel/4218729/
 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
 6. YouTube канал: https://www.youtube.com/@it-coders
 7. ВК группа: https://vk.com/science_geeks
*/