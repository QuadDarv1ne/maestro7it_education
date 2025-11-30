/**
 * https://leetcode.com/problems/number-of-paths/description/
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "Number of Paths" на JavaScript
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
 * Вычисляет количество путей от левого верхнего угла до правого нижнего угла сетки,
 * где сумма чисел по пути делится на k.
 * 
 * Алгоритм использует динамическое программирование с тремя измерениями:
 * - i, j: координаты в сетке
 * - r: остаток от деления суммы пути на k
 * 
 * @param {number[][]} grid - Двумерная сетка с целыми числами
 * @param {number} k - Делитель для проверки суммы пути
 * @returns {number} Количество путей от (0,0) до (m-1,n-1), где сумма делится на k
 * 
 * Time Complexity: O(m * n * k)
 * Space Complexity: O(m * n * k)
 */
var numberOfPaths = function(grid, k) {
    const MOD = 1000000007;
    const m = grid.length, n = grid[0].length;
    
    // Инициализация DP таблицы
    const dp = Array(m).fill(0).map(() => 
        Array(n).fill(0).map(() => Array(k).fill(0))
    );
    dp[0][0][grid[0][0] % k] = 1;
    
    // Заполнение DP таблицы
    for (let i = 0; i < m; i++) {
        for (let j = 0; j < n; j++) {
            for (let r = 0; r < k; r++) {
                const currentCount = dp[i][j][r];
                if (currentCount > 0) {
                    // Движение вправо
                    if (j + 1 < n) {
                        const newRemainder = (r + grid[i][j + 1]) % k;
                        dp[i][j + 1][newRemainder] = (dp[i][j + 1][newRemainder] + currentCount) % MOD;
                    }
                    // Движение вниз
                    if (i + 1 < m) {
                        const newRemainder = (r + grid[i + 1][j]) % k;
                        dp[i + 1][j][newRemainder] = (dp[i + 1][j][newRemainder] + currentCount) % MOD;
                    }
                }
            }
        }
    }
    
    return dp[m - 1][n - 1][0] % MOD;
};