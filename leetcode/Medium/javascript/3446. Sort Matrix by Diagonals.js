/**
 * https://leetcode.com/problems/sort-matrix-by-diagonals/description/?envType=daily-question&envId=2025-08-28
 */

/**
 * sortMatrix
 *
 * Сортировка диагоналей квадратной матрицы n x n.
 * - диагонали из левого столбца (включая главную): non-increasing (по убыванию)
 * - диагонали из верхней строки (кроме (0,0)): non-decreasing (по возрастанию)
 *
 * @param {number[][]} grid
 * @return {number[][]}
 */
function sortMatrix(grid) {
    const n = grid.length;
    if (n === 0) return grid;

    // Нижне-левая часть + главная
    for (let startRow = n - 1; startRow >= 0; --startRow) {
        let i = startRow, j = 0;
        const vals = [];
        while (i < n && j < n) {
            vals.push(grid[i][j]);
            i++; j++;
        }
        // non-increasing
        vals.sort((a, b) => b - a);
        i = startRow; j = 0;
        let k = 0;
        while (i < n && j < n) {
            grid[i][j] = vals[k++];
            i++; j++;
        }
    }

    // Верхне-правая часть (кроме главной)
    for (let startCol = 1; startCol < n; ++startCol) {
        let i = 0, j = startCol;
        const vals = [];
        while (i < n && j < n) {
            vals.push(grid[i][j]);
            i++; j++;
        }
        // non-decreasing
        vals.sort((a, b) => a - b);
        i = 0; j = startCol;
        let k = 0;
        while (i < n && j < n) {
            grid[i][j] = vals[k++];
            i++; j++;
        }
    }

    return grid;
}

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