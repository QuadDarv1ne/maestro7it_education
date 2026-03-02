/**
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
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
 * @param {string} s
 * @return {number}
 */
var firstUniqChar = function(s) {
    // Массив для подсчёта 26 строчных букв
    const count = new Array(26).fill(0);

    // Подсчитываем частоту каждого символа
    for (let i = 0; i < s.length; i++) {
        const index = s.charCodeAt(i) - 'a'.charCodeAt(0);
        count[index]++;
    }

    // Ищем первый символ с частотой 1
    for (let i = 0; i < s.length; i++) {
        const index = s.charCodeAt(i) - 'a'.charCodeAt(0);
        if (count[index] === 1) {
            return i;
        }
    }

    return -1;
};