/**
 * https://leetcode.com/problems/minimum-path-sum/description/
 */

/**
 * Находит минимальную сумму пути из верхнего левого
 * в нижний правый угол сетки, двигаясь только вправо или вниз.
 *
 * @param {number[][]} grid - m × n сетка неотрицательных чисел
 * @return {number} минимальная сумма пути
 *
 * Алгоритм:
 * dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1])
 *
 * Время: O(m * n)
 * Память: O(m * n)
 */
var minPathSum = function(grid) {
    const m = grid.length, n = grid[0].length;
    const dp = Array.from({ length: m }, () => Array(n).fill(0));

    dp[0][0] = grid[0][0];

    for (let j = 1; j < n; j++) {
        dp[0][j] = dp[0][j - 1] + grid[0][j];
    }
    for (let i = 1; i < m; i++) {
        dp[i][0] = dp[i - 1][0] + grid[i][0];
    }
    for (let i = 1; i < m; i++) {
        for (let j = 1; j < n; j++) {
            dp[i][j] = grid[i][j] + Math.min(dp[i - 1][j], dp[i][j - 1]);
        }
    }

    return dp[m - 1][n - 1];
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