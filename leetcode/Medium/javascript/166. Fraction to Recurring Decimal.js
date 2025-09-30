/**
 * https://leetcode.com/problems/fraction-to-recurring-decimal/description/?envType=daily-question&envId=2025-09-24
 */

/**
 * Преобразует дробь numerator/denominator в строку с десятичным представлением.
 * Если дробная часть повторяется, заключает её в скобки.
 *
 * @param {number} numerator - числитель
 * @param {number} denominator - знаменатель (≠ 0)
 * @return {string} строка, например "0.5", "2", "0.(6)", "-0.1(6)"
 */
var fractionToDecimal = function(numerator, denominator) {
    if (numerator === 0) return "0";

    let result = "";
    if ((numerator < 0) ^ (denominator < 0)) result += "-";

    let n = Math.abs(numerator);
    let d = Math.abs(denominator);

    result += Math.floor(n / d);
    let remainder = n % d;
    if (remainder === 0) return result;

    result += ".";
    let seen = new Map();

    while (remainder !== 0) {
        if (seen.has(remainder)) {
            let idx = seen.get(remainder);
            result = result.slice(0, idx) + "(" + result.slice(idx) + ")";
            break;
        }
        seen.set(remainder, result.length);
        remainder *= 10;
        result += Math.floor(remainder / d);
        remainder %= d;
    }

    return result;
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