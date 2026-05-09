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

using System;
using System.Collections.Generic;
using System.Linq;

public class Solution {
    /*
     * Для каждого индекса i вычисляет максимальное значение в nums, 
     * которое может быть достигнуто, начиная с i, следуя правилам прыжков.
     */
    public int[] MaxValue(int[] nums) {
        int n = nums.Length;
        int[] ans = new int[n];

        int[] prefixMax = new int[n];
        int curMax = nums[0];
        for (int i = 0; i < n; i++) {
            curMax = Math.Max(curMax, nums[i]);
            prefixMax[i] = curMax;
        }

        int[] suffixMin = new int[n];
        int curMin = nums[n - 1];
        for (int i = n - 1; i >= 0; i--) {
            curMin = Math.Min(curMin, nums[i]);
            suffixMin[i] = curMin;
        }

        List<int> cutIndices = new List<int>();
        for (int i = 0; i < n - 1; i++) {
            if (prefixMax[i] <= suffixMin[i + 1]) {
                cutIndices.Add(i);
            }
        }

        int start = 0;
        foreach (int cut in cutIndices) {
            int end = cut;
            int segMax = nums[start..(end + 1)].Max();
            for (int i = start; i <= end; i++) {
                ans[i] = segMax;
            }
            start = end + 1;
        }

        if (start < n) {
            int lastSegMax = nums[start..].Max();
            for (int i = start; i < n; i++) {
                ans[i] = lastSegMax;
            }
        }

        return ans;
    }
}