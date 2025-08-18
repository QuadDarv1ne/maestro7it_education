/**
 * https://leetcode.com/problems/decode-ways/description/
 */
class Solution {
    /**
     * Подсчитывает количество способов декодирования строки цифр по схеме A-Z = 1-26.
     *
     * @param s строка, содержащая цифры
     * @return число способов декодирования
     *
     * Алгоритм:
     * dp[0] = 1;
     * Для каждого i:
     *   если s[i-1] != '0': dp[i] += dp[i-1]
     *   если 10 <= Integer.parseInt(s[i-2..i-1]) <= 26: dp[i] += dp[i-2]
     *
     * Время: O(n)
     * Память: O(n), можно уменьшить до O(1)
     */
    public int numDecodings(String s) {
        if (s == null || s.isEmpty() || s.charAt(0) == '0') {
            return 0;
        }
        int n = s.length();
        int[] dp = new int[n + 1];
        dp[0] = 1;
        dp[1] = 1;
        for (int i = 2; i <= n; i++) {
            char c = s.charAt(i - 1);
            if (c != '0') {
                dp[i] += dp[i - 1];
            }
            char p = s.charAt(i - 2);
            if (p != '0') {
                int two = Integer.parseInt(s.substring(i - 2, i));
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