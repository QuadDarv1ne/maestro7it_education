/**
 * https://leetcode.com/problems/decode-ways/description/
 */
public class Solution {
    /**
     * Подсчитывает количество способов декодирования строки цифр по схеме A-Z = 1-26.
     *
     * @param s строка цифр
     * @return число способов декодирования
     *
     * Алгоритм:
     * dp[0] = 1
     * Для i от 1..n:
     *   если s[i-1] != '0': dp[i] += dp[i-1]
     *   если i>=2 и substring s[i-2..i-1] в диапазоне "10".."26": dp[i] += dp[i-2]
     *
     * Время: O(n)
     * Память: O(n)
     */
    public int NumDecodings(string s) {
        if (string.IsNullOrEmpty(s) || s[0] == '0') return 0;
        int n = s.Length;
        int[] dp = new int[n + 1];
        dp[0] = 1;
        dp[1] = 1;
        for (int i = 2; i <= n; i++) {
            if (s[i - 1] != '0') {
                dp[i] += dp[i - 1];
            }
            if (s[i - 2] != '0') {
                int two = int.Parse(s.Substring(i - 2, 2));
                if (two >= 10 && two <= 26) {
                    dp[i] += dp[i - 2];
                }
            }
        }
        return dp[n];
    }
}

/*
''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
*/