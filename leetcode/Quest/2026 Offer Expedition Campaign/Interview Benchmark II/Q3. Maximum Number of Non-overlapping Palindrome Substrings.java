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
    public int maxPalindromes(String s, int k) {
        int n = s.length();
        int[] earliestEnd = new int[n];
        Arrays.fill(earliestEnd, Integer.MAX_VALUE);
        
        // Expand around centers
        for (int i = 0; i < n; i++) {
            expand(s, i, i, k, earliestEnd);      // odd
            expand(s, i, i + 1, k, earliestEnd);  // even
        }
        
        int[] dp = new int[n + 1];
        for (int i = n - 1; i >= 0; i--) {
            dp[i] = dp[i + 1];
            if (earliestEnd[i] != Integer.MAX_VALUE) {
                int j = earliestEnd[i];
                dp[i] = Math.max(dp[i], 1 + dp[j + 1]);
            }
        }
        return dp[0];
    }
    
    private void expand(String s, int l, int r, int k, int[] earliestEnd) {
        int n = s.length();
        while (l >= 0 && r < n && s.charAt(l) == s.charAt(r)) {
            if (r - l + 1 >= k) {
                earliestEnd[l] = Math.min(earliestEnd[l], r);
            }
            l--;
            r++;
        }
    }
}