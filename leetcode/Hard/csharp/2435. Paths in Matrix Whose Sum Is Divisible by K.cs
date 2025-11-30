/**
 * https://leetcode.com/problems/number-of-paths/description/
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "Number of Paths" на C#
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
    /**
     * <summary>
     * Вычисляет количество путей от левого верхнего угла до правого нижнего угла сетки,
     * где сумма чисел по пути делится на k.
     * 
     * Алгоритм использует динамическое программирование с тремя измерениями:
     * - i, j: координаты в сетке
     * - r: остаток от деления суммы пути на k
     * </summary>
     * 
     * <param name="grid">Двумерная сетка с целыми числами</param>
     * <param name="k">Делитель для проверки суммы пути</param>
     * <returns>Количество путей от (0,0) до (m-1,n-1), где сумма делится на k</returns>
     * 
     * <remarks>
     * Time Complexity: O(m * n * k)
     * Space Complexity: O(m * n * k)
     * </remarks>
     */
    public int NumberOfPaths(int[][] grid, int k) {
        const int MOD = 1000000007;
        int m = grid.Length, n = grid[0].Length;
        
        // Инициализация DP таблицы
        int[,,] dp = new int[m, n, k];
        dp[0, 0, grid[0][0] % k] = 1;
        
        // Заполнение DP таблицы
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                for (int r = 0; r < k; r++) {
                    int currentCount = dp[i, j, r];
                    if (currentCount > 0) {
                        // Движение вправо
                        if (j + 1 < n) {
                            int newRemainder = (r + grid[i][j + 1]) % k;
                            dp[i, j + 1, newRemainder] = (dp[i, j + 1, newRemainder] + currentCount) % MOD;
                        }
                        // Движение вниз
                        if (i + 1 < m) {
                            int newRemainder = (r + grid[i + 1][j]) % k;
                            dp[i + 1, j, newRemainder] = (dp[i + 1, j, newRemainder] + currentCount) % MOD;
                        }
                    }
                }
            }
        }
        
        return dp[m - 1, n - 1, 0] % MOD;
    }
}