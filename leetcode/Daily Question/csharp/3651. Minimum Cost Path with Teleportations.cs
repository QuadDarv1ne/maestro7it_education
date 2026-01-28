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
using System.Collections.Generic;
using System.Linq;

public class Solution {
    /// <summary>
    /// Находит минимальную стоимость пути от (0,0) до (m-1,n-1) с возможностью телепортации.
    /// </summary>
    /// <param name="grid">Сетка m×n с целыми числами</param>
    /// <param name="k">Максимальное количество телепортаций</param>
    /// <returns>Минимальная стоимость пути</returns>
    public int MinCost(int[][] grid, int k) {
        int m = grid.Length, n = grid[0].Length;
        const int INF = 1000000000;
        
        // f[t][i][j] = минимальная стоимость достижения (i,j) используя ровно t телепортаций
        int[][][] f = new int[k + 1][][];
        for (int t = 0; t <= k; t++) {
            f[t] = new int[m][];
            for (int i = 0; i < m; i++) {
                f[t][i] = new int[n];
                Array.Fill(f[t][i], INF);
            }
        }
        
        // Базовый случай: телепортации не используются
        f[0][0][0] = 0;
        
        // Заполняем таблицу DP для 0 телепортаций (только обычные ходы)
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (i > 0) {
                    f[0][i][j] = Math.Min(f[0][i][j], f[0][i-1][j] + grid[i][j]);
                }
                if (j > 0) {
                    f[0][i][j] = Math.Min(f[0][i][j], f[0][i][j-1] + grid[i][j]);
                }
            }
        }
        
        // Группируем клетки по их значениям для эффективной телепортации
        Dictionary<int, List<(int, int)>> valueToCells = new Dictionary<int, List<(int, int)>>();
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (!valueToCells.ContainsKey(grid[i][j])) {
                    valueToCells[grid[i][j]] = new List<(int, int)>();
                }
                valueToCells[grid[i][j]].Add((i, j));
            }
        }
        
        // Сортируем значения по убыванию
        var sortedValues = valueToCells.Keys.OrderByDescending(x => x).ToList();
        
        // Для каждого количества телепортаций
        for (int t = 1; t <= k; t++) {
            int minCost = INF;
            
            // Обрабатываем клетки в порядке убывания значений
            // Это гарантирует, что когда мы телепортируемся В клетку со значением v,
            // мы уже вычислили стоимости для всех клеток со значением >= v
            foreach (int val in sortedValues) {
                var cells = valueToCells[val];
                
                // Обновляем minCost клетками с текущим значением
                // Это потенциальные источники для телепортации
                foreach (var (i, j) in cells) {
                    minCost = Math.Min(minCost, f[t-1][i][j]);
                }
                
                // Все клетки с этим значением можно достичь телепортацией
                // из любой клетки со значением >= этого значения используя t телепортаций
                foreach (var (i, j) in cells) {
                    f[t][i][j] = minCost;
                }
            }
            
            // После телепортации можем делать обычные ходы
            for (int i = 0; i < m; i++) {
                for (int j = 0; j < n; j++) {
                    if (i > 0) {
                        f[t][i][j] = Math.Min(f[t][i][j], f[t][i-1][j] + grid[i][j]);
                    }
                    if (j > 0) {
                        f[t][i][j] = Math.Min(f[t][i][j], f[t][i][j-1] + grid[i][j]);
                    }
                }
            }
        }
        
        // Возвращаем минимальную стоимость используя любое количество телепортаций (от 0 до k)
        int result = INF;
        for (int t = 0; t <= k; t++) {
            result = Math.Min(result, f[t][m-1][n-1]);
        }
        return result;
    }
}