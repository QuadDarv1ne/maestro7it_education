/**
 * https://leetcode.com/problems/valid-palindrome/description/
 */

#include <string>
#include <cctype>
using namespace std;

/**
 * @brief Проверяет, является ли строка палиндромом, игнорируя небуквенно-цифровые символы и регистр.
 *
 * @param s Входная строка.
 * @return true если после удаления небуквенно-цифровых символов и приведения к нижнему регистру
 *         строка читается одинаково в обе стороны, иначе false.
 */
class Solution {
public:
    bool isPalindrome(string s) {
        int i = 0, j = (int)s.size() - 1;
        while (i < j) {
            while (i < j && !isalnum((unsigned char)s[i])) ++i;
            while (i < j && !isalnum((unsigned char)s[j])) --j;
            if (i < j) {
                if (tolower((unsigned char)s[i]) != tolower((unsigned char)s[j])) return false;
                ++i; --j;
            }
        }
        return true;
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