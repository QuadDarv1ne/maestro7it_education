/**
 * https://leetcode.com/problems/roman-to-integer/description/
 */

using System;
using System.Collections.Generic;

/**
 * Преобразует римское число s в целое число.
 */
public class Solution {
    public int RomanToInt(string s) {
        var romanMap = new Dictionary<char, int> {
            {'I',1}, {'V',5}, {'X',10}, {'L',50},
            {'C',100}, {'D',500}, {'M',1000}
        };

        int total = 0;
        for (int i = 0; i < s.Length - 1; i++) {
            if (romanMap[s[i]] < romanMap[s[i + 1]])
                total -= romanMap[s[i]];
            else
                total += romanMap[s[i]];
        }
        total += romanMap[s[s.Length - 1]];
        return total;
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