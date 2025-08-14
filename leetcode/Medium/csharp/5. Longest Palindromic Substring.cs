/**
 * https://leetcode.com/problems/longest-palindromic-substring/description/
 */

/// <summary>
/// Находит самую длинную палиндромную подстроку в строке s.
/// </summary>
/// <param name="s">Входная строка</param>
/// <returns>Самая длинная палиндромная подстрока</returns>
public class Solution {
    public string LongestPalindrome(string s) {
        if (string.IsNullOrEmpty(s)) return "";
        string longest = "";
        for (int i = 0; i < s.Length; i++) {
            string odd = ExpandAroundCenter(s, i, i);
            if (odd.Length > longest.Length) longest = odd;
            string even = ExpandAroundCenter(s, i, i + 1);
            if (even.Length > longest.Length) longest = even;
        }
        return longest;
    }

    private string ExpandAroundCenter(string s, int left, int right) {
        while (left >= 0 && right < s.Length && s[left] == s[right]) {
            left--;
            right++;
        }
        return s.Substring(left + 1, right - left - 1);
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