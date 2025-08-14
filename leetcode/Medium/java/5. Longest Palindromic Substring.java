/**
 * https://leetcode.com/problems/longest-palindromic-substring/description/
 */

/**
 * Находит самую длинную палиндромную подстроку в строке s.
 *
 * Алгоритм:
 * - Расширяем палиндром из каждого центра.
 * - Проверяем два варианта: нечётная и чётная длина.
 * - Возвращаем самую длинную палиндромную подстроку.
 */
class Solution {
    public String longestPalindrome(String s) {
        if (s == null || s.length() < 1) return "";
        String longest = "";
        for (int i = 0; i < s.length(); i++) {
            String odd = expandAroundCenter(s, i, i);
            if (odd.length() > longest.length()) longest = odd;
            String even = expandAroundCenter(s, i, i + 1);
            if (even.length() > longest.length()) longest = even;
        }
        return longest;
    }

    private String expandAroundCenter(String s, int left, int right) {
        while (left >= 0 && right < s.length() && s.charAt(left) == s.charAt(right)) {
            left--;
            right++;
        }
        return s.substring(left + 1, right);
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