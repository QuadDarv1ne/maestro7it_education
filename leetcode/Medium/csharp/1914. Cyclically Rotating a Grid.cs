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

public class Solution {
    /// <summary>
    /// Циклически сдвигает каждый слой матрицы на k шагов против часовой стрелки.
    /// </summary>
    /// <param name="grid">Исходная матрица m x n (m и n - чётные).</param>
    /// <param name="k">Количество циклических сдвигов.</param>
    /// <returns>Матрица после выполнения k циклических сдвигов для каждого слоя.</returns>
    public int[][] RotateGrid(int[][] grid, int k) {
        int m = grid.Length;
        int n = grid[0].Length;
        int layers = Math.Min(m, n) / 2;

        for (int layer = 0; layer < layers; layer++) {
            List<int> elements = new List<int>();

            // Верхняя строка
            for (int col = layer; col < n - layer; col++)
                elements.Add(grid[layer][col]);
            // Правый столбец
            for (int row = layer + 1; row < m - layer; row++)
                elements.Add(grid[row][n - 1 - layer]);
            // Нижняя строка
            if (m - 1 - layer > layer)
                for (int col = n - 2 - layer; col >= layer; col--)
                    elements.Add(grid[m - 1 - layer][col]);
            // Левый столбец
            if (n - 1 - layer > layer)
                for (int row = m - 2 - layer; row > layer; row--)
                    elements.Add(grid[row][layer]);

            int length = elements.Count;
            if (length == 0) continue;
            int shift = k % length;

            int idx = 0;
            // Верхняя строка
            for (int col = layer; col < n - layer; col++)
                grid[layer][col] = elements[(shift + idx++) % length];
            // Правый столбец
            for (int row = layer + 1; row < m - layer; row++)
                grid[row][n - 1 - layer] = elements[(shift + idx++) % length];
            // Нижняя строка
            if (m - 1 - layer > layer)
                for (int col = n - 2 - layer; col >= layer; col--)
                    grid[m - 1 - layer][col] = elements[(shift + idx++) % length];
            // Левый столбец
            if (n - 1 - layer > layer)
                for (int row = m - 2 - layer; row > layer; row--)
                    grid[row][layer] = elements[(shift + idx++) % length];
        }
        return grid;
    }
}