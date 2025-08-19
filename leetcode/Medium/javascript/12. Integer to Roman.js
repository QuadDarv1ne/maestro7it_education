/**
 * https://leetcode.com/problems/integer-to-roman/description/
 */

/**
 * Преобразует целое число (1 ≤ num ≤ 3999) в римское число.
 *
 * Подход:
 * - Жадный: проходим по списку объектов {value, symbol} от большего к меньшему.
 * - Пока num ≥ value, вычитаем и добавляем symbol к строке результата.
 *
 * @param {number} num - входное число.
 * @return {string} - строка с римским числом.
 */
var intToRoman = function(num) {
    const romanMap = [
        { value: 1000, symbol: 'M' },
        { value: 900, symbol: 'CM' },
        { value: 500, symbol: 'D' },
        { value: 400, symbol: 'CD' },
        { value: 100, symbol: 'C' },
        { value: 90, symbol: 'XC' },
        { value: 50, symbol: 'L' },
        { value: 40, symbol: 'XL' },
        { value: 10, symbol: 'X' },
        { value: 9, symbol: 'IX' },
        { value: 5, symbol: 'V' },
        { value: 4, symbol: 'IV' },
        { value: 1, symbol: 'I' },
    ];
    let result = '';
    for (const { value, symbol } of romanMap) {
        while (num >= value) {
            result += symbol;
            num -= value;
        }
    }
    return result;
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