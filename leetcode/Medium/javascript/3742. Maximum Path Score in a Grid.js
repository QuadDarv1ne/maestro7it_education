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
 * @param {number[][]} grid - матрица m x n, значения 0, 1 или 2.
 * @param {number} k - максимальная допустимая стоимость.
 * @return {number} максимальное количество очков, или -1, если путь невозможен.
 */
var maxPathScore = function(grid, k) {
    const m = grid.length, n = grid[0].length;
    // dp[i][j][c] = максимальный счёт в клетке (i,j) при точной стоимости c
    let dp = Array(m).fill().map(() => Array(n).fill().map(() => Array(k+1).fill(-1)));

    const start_cost = (grid[0][0] === 0) ? 0 : 1;
    const start_score = (grid[0][0] === 0) ? 0 : (grid[0][0] === 1 ? 1 : 2);
    if (start_cost <= k) dp[0][0][start_cost] = start_score;

    for (let i = 0; i < m; i++) {
        for (let j = 0; j < n; j++) {
            if (i === 0 && j === 0) continue;
            const add_cost = (grid[i][j] === 0) ? 0 : 1;
            const add_score = (grid[i][j] === 0) ? 0 : (grid[i][j] === 1 ? 1 : 2);

            // сверху
            if (i > 0) {
                for (let prev_cost = 0; prev_cost <= k - add_cost; prev_cost++) {
                    if (dp[i-1][j][prev_cost] !== -1) {
                        const new_cost = prev_cost + add_cost;
                        const new_score = dp[i-1][j][prev_cost] + add_score;
                        if (new_score > dp[i][j][new_cost]) {
                            dp[i][j][new_cost] = new_score;
                        }
                    }
                }
            }
            // слева
            if (j > 0) {
                for (let prev_cost = 0; prev_cost <= k - add_cost; prev_cost++) {
                    if (dp[i][j-1][prev_cost] !== -1) {
                        const new_cost = prev_cost + add_cost;
                        const new_score = dp[i][j-1][prev_cost] + add_score;
                        if (new_score > dp[i][j][new_cost]) {
                            dp[i][j][new_cost] = new_score;
                        }
                    }
                }
            }
        }
    }

    let ans = -1;
    for (let cost = 0; cost <= k; cost++) {
        if (dp[m-1][n-1][cost] > ans) ans = dp[m-1][n-1][cost];
    }
    return ans;
};