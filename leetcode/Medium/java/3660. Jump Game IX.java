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

import java.util.*;

class Solution {
    /*
     * Для каждого индекса i вычисляет максимальное значение в nums, 
     * которое может быть достигнуто, начиная с i, следуя правилам прыжков.
     */
    public int[] maxValue(int[] nums) {
        int n = nums.length;
        int[] ans = new int[n];

        int[] prefixMax = new int[n];
        int curMax = nums[0];
        for (int i = 0; i < n; i++) {
            curMax = Math.max(curMax, nums[i]);
            prefixMax[i] = curMax;
        }

        int[] suffixMin = new int[n];
        int curMin = nums[n - 1];
        for (int i = n - 1; i >= 0; i--) {
            curMin = Math.min(curMin, nums[i]);
            suffixMin[i] = curMin;
        }

        List<Integer> cutIndices = new ArrayList<>();
        for (int i = 0; i < n - 1; i++) {
            if (prefixMax[i] <= suffixMin[i + 1]) {
                cutIndices.add(i);
            }
        }

        int start = 0;
        for (int cut : cutIndices) {
            int end = cut;
            int segMax = Arrays.stream(nums, start, end + 1).max().getAsInt();
            for (int i = start; i <= end; i++) {
                ans[i] = segMax;
            }
            start = end + 1;
        }

        if (start < n) {
            int lastSegMax = Arrays.stream(nums, start, n).max().getAsInt();
            for (int i = start; i < n; i++) {
                ans[i] = lastSegMax;
            }
        }

        return ans;
    }
}