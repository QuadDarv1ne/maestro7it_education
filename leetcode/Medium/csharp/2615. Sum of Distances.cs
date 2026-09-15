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

public class Solution {
    public long[] Distance(int[] nums) {
        int n = nums.Length;
        var dict = new Dictionary<int, List<int>>();
        for (int i = 0; i < n; i++) {
            if (!dict.ContainsKey(nums[i])) dict[nums[i]] = new List<int>();
            dict[nums[i]].Add(i);
        }
        
        long[] ans = new long[n];
        
        foreach (var kvp in dict) {
            var indices = kvp.Value;
            int m = indices.Count;
            long[] prefix = new long[m + 1];
            for (int i = 0; i < m; i++) {
                prefix[i + 1] = prefix[i] + indices[i];
            }
            
            for (int i = 0; i < m; i++) {
                long idx = indices[i];
                long leftCount = i;
                long leftSum = prefix[i];
                long leftDist = idx * leftCount - leftSum;
                
                long rightCount = m - i - 1;
                long rightSum = prefix[m] - prefix[i + 1];
                long rightDist = rightSum - idx * rightCount;
                
                ans[idx] = leftDist + rightDist;
            }
        }
        return ans;
    }
}