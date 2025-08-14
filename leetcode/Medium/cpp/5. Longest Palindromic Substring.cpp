/**
 * https://leetcode.com/problems/longest-palindromic-substring/description/
 */

#include <string>
using namespace std;

/**
 * @brief Находит самую длинную палиндромную подстроку в строке s.
 *
 * Алгоритм:
 * - Расширяем палиндром из каждого центра.
 * - Для каждого символа проверяем два варианта:
 *     1) Палиндром нечётной длины (центр один символ).
 *     2) Палиндром чётной длины (центр между двумя символами).
 * - Возвращаем самую длинную палиндромную подстроку.
 *
 * Время: O(n^2), память: O(1)
 */
class Solution {
public:
    string longestPalindrome(string s) {
        if (s.empty()) return "";
        string longest = "";
        for (int i = 0; i < s.size(); ++i) {
            // Нечётная длина
            string odd = expandAroundCenter(s, i, i);
            if (odd.size() > longest.size()) longest = odd;
            // Чётная длина
            string even = expandAroundCenter(s, i, i + 1);
            if (even.size() > longest.size()) longest = even;
        }
        return longest;
    }

private:
    string expandAroundCenter(const string& s, int left, int right) {
        while (left >= 0 && right < s.size() && s[left] == s[right]) {
            --left;
            ++right;
        }
        return s.substr(left + 1, right - left - 1);
    }
};

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