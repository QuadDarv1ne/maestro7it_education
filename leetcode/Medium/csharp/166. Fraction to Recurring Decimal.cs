/**
 * https://leetcode.com/problems/fraction-to-recurring-decimal/description/?envType=daily-question&envId=2025-09-24
 */

using System;
using System.Collections.Generic;
using System.Text;

public class Solution {
    /// <summary>
    /// Преобразует дробь numerator/denominator в строку с десятичным представлением.
    /// Если дробная часть повторяется, заключает её в скобки.
    /// </summary>
    public string FractionToDecimal(int numerator, int denominator) {
        if (numerator == 0) return "0";

        StringBuilder result = new StringBuilder();
        if ((numerator < 0) ^ (denominator < 0)) result.Append("-");

        long n = Math.Abs((long)numerator);
        long d = Math.Abs((long)denominator);

        result.Append(n / d);
        long remainder = n % d;
        if (remainder == 0) return result.ToString();

        result.Append(".");
        Dictionary<long, int> seen = new Dictionary<long, int>();

        while (remainder != 0) {
            if (seen.ContainsKey(remainder)) {
                result.Insert(seen[remainder], "(");
                result.Append(")");
                break;
            }
            seen[remainder] = result.Length;
            remainder *= 10;
            result.Append(remainder / d);
            remainder %= d;
        }

        return result.ToString();
    }
}

/*
''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
*/