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
 * Проверяет, содержит ли строка s все бинарные коды длины k.
 *
 * @param {string} s - входная бинарная строка
 * @param {number} k - длина кода
 * @return {boolean} - true, если все коды присутствуют, иначе false
 */
var hasAllCodes = function(s, k) {
    const need = 1 << k;  // 2^k
    if (s.length < need + k - 1) {
        return false;
    }
    
    const seen = new Set();
    for (let i = 0; i <= s.length - k; i++) {
        seen.add(s.substring(i, i + k));
        if (seen.size === need) {
            return true;  // нашли все коды досрочно
        }
    }
    return seen.size === need;
};