/**
 * https://leetcode.com/problems/letter-combinations-of-a-phone-number/description/
 */

#include <vector>
#include <string>
using namespace std;

/**
 * @brief Генерирует все возможные комбинации букв для строки цифр digits.
 */
class Solution {
public:
    vector<string> letterCombinations(string digits) {
        if (digits.empty()) return {};
        
        vector<string> result;
        string current;
        vector<string> digit_map = {
            "", "", "abc", "def", "ghi", "jkl",
            "mno", "pqrs", "tuv", "wxyz"
        };
        backtrack(digits, 0, current, result, digit_map);
        return result;
    }

private:
    void backtrack(const string& digits, int index, string& current, vector<string>& result, const vector<string>& digit_map) {
        if (index == digits.size()) {
            result.push_back(current);
            return;
        }
        string letters = digit_map[digits[index] - '0'];
        for (char c : letters) {
            current.push_back(c);
            backtrack(digits, index + 1, current, result, digit_map);
            current.pop_back();
        }
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