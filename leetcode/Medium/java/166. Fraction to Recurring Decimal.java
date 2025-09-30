/**
 * https://leetcode.com/problems/fraction-to-recurring-decimal/description/?envType=daily-question&envId=2025-09-24
 */

import java.util.*;

class Solution {
    /**
     * Преобразует дробь numerator/denominator в строку с десятичным представлением.
     * Если дробная часть повторяется, заключает её в скобки.
     *
     * @param numerator числитель
     * @param denominator знаменатель (≠ 0)
     * @return строка, например "0.5", "2", "0.(6)", "-0.1(6)"
     */
    public String fractionToDecimal(int numerator, int denominator) {
        if (numerator == 0) return "0";

        StringBuilder result = new StringBuilder();
        if ((numerator < 0) ^ (denominator < 0)) result.append("-");

        long n = Math.abs((long) numerator);
        long d = Math.abs((long) denominator);

        result.append(n / d);
        long remainder = n % d;
        if (remainder == 0) return result.toString();

        result.append(".");
        Map<Long, Integer> seen = new HashMap<>();

        while (remainder != 0) {
            if (seen.containsKey(remainder)) {
                result.insert(seen.get(remainder), "(");
                result.append(")");
                break;
            }
            seen.put(remainder, result.length());
            remainder *= 10;
            result.append(remainder / d);
            remainder %= d;
        }

        return result.toString();
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