/**
 * https://leetcode.com/problems/sort-matrix-by-diagonals/description/?envType=daily-question&envId=2025-08-28
 */

using System;
using System.Collections.Generic;

public class Solution {
    /// <summary>
    /// SortMatrix
    ///
    /// Сортирует диагонали квадратной матрицы n x n:
    /// - диагонали, начинающиеся в левом столбце (включая главную) — сортировать по убыванию;
    /// - диагонали, начинающиеся в верхней строке (кроме (0,0)) — сортировать по возрастанию.
    /// </summary>
    /// <param name="grid">Входная матрица (jagged int[][])</param>
    /// <returns>Матрица с отсортированными диагоналями</returns>
    public int[][] SortMatrix(int[][] grid) {
        int n = grid.Length;
        if (n == 0) return grid;

        // Нижне-левая часть + главная диагональ (startRow от n-1 до 0)
        for (int startRow = n - 1; startRow >= 0; startRow--) {
            int i = startRow, j = 0;
            var vals = new List<int>();
            while (i < n && j < n) {
                vals.Add(grid[i][j]);
                i++; j++;
            }
            // non-increasing (по убыванию)
            vals.Sort((a, b) => b.CompareTo(a));
            i = startRow; j = 0;
            int k = 0;
            while (i < n && j < n) {
                grid[i][j] = vals[k++];
                i++; j++;
            }
        }

        // Верхне-правая часть (кроме главной): startCol от 1 до n-1
        for (int startCol = 1; startCol < n; startCol++) {
            int i = 0, j = startCol;
            var vals = new List<int>();
            while (i < n && j < n) {
                vals.Add(grid[i][j]);
                i++; j++;
            }
            // non-decreasing (по возрастанию)
            vals.Sort();
            i = 0; j = startCol;
            int k = 0;
            while (i < n && j < n) {
                grid[i][j] = vals[k++];
                i++; j++;
            }
        }

        return grid;
    }

    // Альтернативный метод с маленькой буквы (оставил на случай автогенераторов, которые ожидают sortMatrix)
    public int[][] sortMatrix(int[][] grid) {
        return SortMatrix(grid);
    }
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