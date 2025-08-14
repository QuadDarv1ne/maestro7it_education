/**
 * https://leetcode.com/problems/reverse-string/description/
 */

#include <vector>
using namespace std;

/**
 * @brief Переворачивает массив символов на месте.
 *
 * @param s Ссылка на вектор<char>, представляющий строку.
 * Изменяет входной вектор так, что порядок символов становится обратным.
 */
class Solution {
public:
    void reverseString(vector<char>& s) {
        int i = 0, j = (int)s.size() - 1;
        while (i < j) swap(s[i++], s[j--]);
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