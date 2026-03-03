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
    public int MaxPalindromes(string s, int k) {
        int n = s.Length;
        int[] earliestEnd = new int[n];
        Array.Fill(earliestEnd, int.MaxValue);
        
        for (int i = 0; i < n; i++) {
            Expand(s, i, i, k, earliestEnd);      // odd
            Expand(s, i, i + 1, k, earliestEnd);  // even
        }
        
        int[] dp = new int[n + 1];
        for (int i = n - 1; i >= 0; i--) {
            dp[i] = dp[i + 1];
            if (earliestEnd[i] != int.MaxValue) {
                int j = earliestEnd[i];
                dp[i] = Math.Max(dp[i], 1 + dp[j + 1]);
            }
        }
        return dp[0];
    }
    
    private void Expand(string s, int l, int r, int k, int[] earliestEnd) {
        int n = s.Length;
        while (l >= 0 && r < n && s[l] == s[r]) {
            if (r - l + 1 >= k) {
                earliestEnd[l] = Math.Min(earliestEnd[l], r);
            }
            l--;
            r++;
        }
    }
}