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

class Solution {
    public long[] distance(int[] nums) {
        int n = nums.length;
        Map<Integer, List<Integer>> map = new HashMap<>();
        for (int i = 0; i < n; i++) {
            map.computeIfAbsent(nums[i], k -> new ArrayList<>()).add(i);
        }
        
        long[] ans = new long[n];
        
        for (List<Integer> indices : map.values()) {
            int m = indices.size();
            long[] prefix = new long[m + 1];
            for (int i = 0; i < m; i++) {
                prefix[i + 1] = prefix[i] + indices.get(i);
            }
            
            for (int i = 0; i < m; i++) {
                long idx = indices.get(i);
                long leftCount = i;
                long leftSum = prefix[i];
                long leftDist = idx * leftCount - leftSum;
                
                long rightCount = m - i - 1;
                long rightSum = prefix[m] - prefix[i + 1];
                long rightDist = rightSum - idx * rightCount;
                
                ans[(int) idx] = leftDist + rightDist;
            }
        }
        return ans;
    }
}