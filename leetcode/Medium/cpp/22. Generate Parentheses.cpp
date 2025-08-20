/**
 * https://leetcode.com/problems/generate-parentheses/description/
 */

#include <vector>
#include <string>
using namespace std;

class Solution {
public:
    /**
     * Генерирует все возможные корректные скобочные последовательности длины 2n.
     *
     * Алгоритм:
     * - Используем рекурсию с двумя счётчиками: открытых и закрытых скобок.
     * - Добавляем открывающую скобку, если их меньше n.
     * - Добавляем закрывающую скобку, если их меньше открытых.
     * - Рекурсивно строим строку и добавляем её в результат, когда длина строки достигает 2n.
     *
     * Время: O(4^n / sqrt(n)), Память: O(4^n / sqrt(n)).
     */
    vector<string> generateParenthesis(int n) {
        vector<string> result;
        generateParenthesisHelper(result, "", 0, 0, n);
        return result;
    }

    void generateParenthesisHelper(vector<string>& result, string current, int open, int close, int max) {
        if (current.length() == 2 * max) {
            result.push_back(current);
            return;
        }
        if (open < max) {
            generateParenthesisHelper(result, current + "(", open + 1, close, max);
        }
        if (close < open) {
            generateParenthesisHelper(result, current + ")", open, close + 1, max);
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