/**
 * https://leetcode.com/problems/zigzag-conversion/description/
 */

#include <string>
#include <vector>
using namespace std;

/**
 * @brief Преобразует строку s в зигзагообразный паттерн с numRows строками.
 *
 * Алгоритм:
 * - Если numRows == 1 или numRows >= s.length(), возвращаем s.
 * - Инициализируем вектор строк rows для хранения каждой строки паттерна.
 * - Распределяем символы строки по строкам зигзагообразного паттерна.
 * - Объединяем строки в один результат.
 *
 * Время: O(n), память: O(n)
 */
class Solution {
public:
    string convert(string s, int numRows) {
        if (numRows == 1 || numRows >= s.size()) return s;

        vector<string> rows(numRows);
        int currentRow = 0;
        bool goingDown = false;

        for (char c : s) {
            rows[currentRow] += c;
            if (currentRow == 0 || currentRow == numRows - 1)
                goingDown = !goingDown;
            currentRow += goingDown ? 1 : -1;
        }

        string result;
        for (const string& row : rows) {
            result += row;
        }
        return result;
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