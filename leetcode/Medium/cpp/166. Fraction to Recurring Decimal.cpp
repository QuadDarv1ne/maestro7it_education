/**
 * https://leetcode.com/problems/fraction-to-recurring-decimal/description/?envType=daily-question&envId=2025-09-24
 */

#include <string>
#include <unordered_map>
#include <cstdlib>
using namespace std;

class Solution {
public:
    /**
     * Преобразует дробь numerator/denominator в строку с десятичным представлением.
     * Если дробная часть повторяется, заключает её в скобки.
     *
     * @param numerator числитель
     * @param denominator знаменатель (≠ 0)
     * @return строка, например "0.5", "2", "0.(6)", "-0.1(6)"
     */
    string fractionToDecimal(long long numerator, long long denominator) {
        if (numerator == 0) return "0";

        string result;
        if ((numerator < 0) ^ (denominator < 0)) result += "-";

        long long n = llabs(numerator), d = llabs(denominator);
        result += to_string(n / d);
        long long remainder = n % d;
        if (remainder == 0) return result;

        result += ".";
        unordered_map<long long, int> seen;

        while (remainder) {
            if (seen.count(remainder)) {
                result.insert(seen[remainder], "(");
                result.push_back(')');
                break;
            }
            seen[remainder] = result.size();
            remainder *= 10;
            result += to_string(remainder / d);
            remainder %= d;
        }

        return result;
    }
};

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