/**
 * https://leetcode.com/problems/add-binary/description/
 * Автор: Дуплей Максим Игоревич- AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "67. Add Binary"
 * 
 * Полезные ссылки:
 * 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
 * 2. Telegram №1 @quadd4rv1n7
 * 3. Telegram №2 @dupley_maxim_1999
 * 4. Rutube канал: https://rutube.ru/channel/4218729/
 * 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
 * 6. YouTube канал: https://www.youtube.com/@it-coders
 * 7. ВК группа: https://vk.com/science_geeks
 */

/**
 * @param {string} a
 * @param {string} b
 * @return {string}
 */
var addBinary = function(a, b) {
    let result = [];
    let i = a.length - 1;
    let j = b.length - 1;
    let carry = 0;

    while (i >= 0 || j >= 0 || carry) {
        let sum = carry;
        if (i >= 0) sum += +a[i--];
        if (j >= 0) sum += +b[j--];
        result.unshift(sum % 2);
        carry = Math.floor(sum / 2);
    }

    return result.join('');
};