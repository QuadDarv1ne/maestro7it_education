/**
 * https://leetcode.com/problems/integer-to-roman/description/
 */

#include <string>
#include <vector>
using namespace std;

class Solution {
public:
    /**
     * Преобразует целое число num (1 ≤ num ≤ 3999) в строку римского числа.
     *
     * Жадная стратегия:
     * - Перебираем соответствия value ↔ symbol от больших к меньшим (включая вычитание).
     * - Пока num >= value, вычитаем и добавляем символ.
     */
    string intToRoman(int num) {
        vector<pair<int, string>> vs = {
            {1000,"M"}, {900,"CM"}, {500,"D"}, {400,"CD"},
            {100,"C"}, {90,"XC"}, {50,"L"}, {40,"XL"},
            {10,"X"}, {9,"IX"}, {5,"V"}, {4,"IV"}, {1,"I"}
        };
        string res = "";
        for (auto &p : vs) {
            while (num >= p.first) {
                num -= p.first;
                res += p.second;
            }
        }
        return res;
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