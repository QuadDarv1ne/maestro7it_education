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
 * @param {character[][]} grid
 * @return {number}
 */
var numberOfSubmatrices = function(grid) {
    const m = grid.length;
    const n = grid[0].length;
    // Создаём двумерные массивы, заполненные 0
    const prefixX = Array.from({ length: m }, () => Array(n).fill(0));
    const prefixY = Array.from({ length: m }, () => Array(n).fill(0));
    let count = 0;

    for (let i = 0; i < m; i++) {
        for (let j = 0; j < n; j++) {
            if (i > 0) {
                prefixX[i][j] += prefixX[i-1][j];
                prefixY[i][j] += prefixY[i-1][j];
            }
            if (j > 0) {
                prefixX[i][j] += prefixX[i][j-1];
                prefixY[i][j] += prefixY[i][j-1];
            }
            if (i > 0 && j > 0) {
                prefixX[i][j] -= prefixX[i-1][j-1];
                prefixY[i][j] -= prefixY[i-1][j-1];
            }

            if (grid[i][j] === 'X') {
                prefixX[i][j] += 1;
            } else if (grid[i][j] === 'Y') {
                prefixY[i][j] += 1;
            }

            if (prefixX[i][j] === prefixY[i][j] && prefixX[i][j] > 0) {
                count++;
            }
        }
    }
    return count;
};