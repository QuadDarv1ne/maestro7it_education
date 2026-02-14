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
 * @param {number} poured
 * @param {number} query_row
 * @param {number} query_glass
 * @return {number}
 */
var champagneTower = function(poured, query_row, query_glass) {
    // Текущий ряд
    let curr = [poured];

    for (let row = 0; row < query_row; row++) {
        // Следующий ряд: длина row+2, заполняем нулями
        const next = new Array(row + 2).fill(0);
        for (let i = 0; i < curr.length; i++) {
            if (curr[i] > 1) {
                const excess = (curr[i] - 1) / 2;
                next[i] += excess;
                next[i + 1] += excess;
            }
        }
        curr = next;
    }

    return Math.min(1, curr[query_glass]);
};