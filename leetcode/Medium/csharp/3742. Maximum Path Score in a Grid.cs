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

using System;

public class Solution {
    /// <summary>
    /// Находит максимальный счёт на пути из левого верхнего в правый нижний угол,
    /// двигаясь только вправо или вниз, при условии, что суммарная стоимость не превышает k.
    ///
    /// Значения ячеек:
    /// - 0: добавляет 0 очков, стоимость 0
    /// - 1: добавляет 1 очко, стоимость 1
    /// - 2: добавляет 2 очка, стоимость 1
    ///
    /// Если ни один путь не укладывается в бюджет k, возвращает -1.
    /// </summary>
    /// <param name="grid">матрица m x n, значения 0, 1 или 2.</param>
    /// <param name="k">максимальная допустимая стоимость.</param>
    /// <returns>максимальное количество очков, или -1, если путь невозможен.</returns>
    public int MaxPathScore(int[][] grid, int k) {
        int m = grid.Length, n = grid[0].Length;
        int[,,] dp = new int[m, n, k+1];
        for (int i = 0; i < m; i++)
            for (int j = 0; j < n; j++)
                for (int c = 0; c <= k; c++)
                    dp[i, j, c] = -1;

        int start_cost = (grid[0][0] == 0) ? 0 : 1;
        int start_score = (grid[0][0] == 0) ? 0 : (grid[0][0] == 1 ? 1 : 2);
        if (start_cost <= k) dp[0, 0, start_cost] = start_score;

        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (i == 0 && j == 0) continue;
                int add_cost = (grid[i][j] == 0) ? 0 : 1;
                int add_score = (grid[i][j] == 0) ? 0 : (grid[i][j] == 1 ? 1 : 2);

                // сверху
                if (i > 0) {
                    for (int prev_cost = 0; prev_cost <= k - add_cost; prev_cost++) {
                        if (dp[i-1, j, prev_cost] != -1) {
                            int new_cost = prev_cost + add_cost;
                            int new_score = dp[i-1, j, prev_cost] + add_score;
                            if (new_score > dp[i, j, new_cost]) {
                                dp[i, j, new_cost] = new_score;
                            }
                        }
                    }
                }
                // слева
                if (j > 0) {
                    for (int prev_cost = 0; prev_cost <= k - add_cost; prev_cost++) {
                        if (dp[i, j-1, prev_cost] != -1) {
                            int new_cost = prev_cost + add_cost;
                            int new_score = dp[i, j-1, prev_cost] + add_score;
                            if (new_score > dp[i, j, new_cost]) {
                                dp[i, j, new_cost] = new_score;
                            }
                        }
                    }
                }
            }
        }

        int ans = -1;
        for (int cost = 0; cost <= k; cost++) {
            ans = Math.Max(ans, dp[m-1, n-1, cost]);
        }
        return ans;
    }
}