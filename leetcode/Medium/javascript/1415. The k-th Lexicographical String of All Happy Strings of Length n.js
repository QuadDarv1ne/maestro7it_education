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
 * @param {number} n
 * @param {number} k
 * @return {string}
 */
var getHappyString = function(n, k) {
    // Общее количество строк: 3 * 2^(n-1)
    const total = 3 * (1 << (n - 1));
    if (k > total) return "";

    let result = "";
    let prev = '';

    for (let i = 0; i < n; i++) {
        // Перебираем символы в порядке 'a', 'b', 'c'
        for (const c of ['a', 'b', 'c']) {
            if (c === prev) continue;

            // Количество строк с данным префиксом для оставшихся позиций
            const count = 1 << (n - i - 1);

            if (k > count) {
                k -= count;
            } else {
                result += c;
                prev = c;
                break;
            }
        }
    }
    return result;
};