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

import java.util.ArrayList;
import java.util.List;

class Solution {
    /**
     * Циклически сдвигает каждый слой матрицы на k шагов против часовой стрелки.
     * @param grid Исходная матрица m x n (m и n - чётные).
     * @param k Количество циклических сдвигов.
     * @return Матрица после выполнения k циклических сдвигов для каждого слоя.
     */
    public int[][] rotateGrid(int[][] grid, int k) {
        int m = grid.length;
        int n = grid[0].length;
        int layers = Math.min(m, n) / 2;

        for (int layer = 0; layer < layers; layer++) {
            List<Integer> elements = new ArrayList<>();

            // Верхняя строка
            for (int col = layer; col < n - layer; col++)
                elements.add(grid[layer][col]);
            // Правый столбец
            for (int row = layer + 1; row < m - layer; row++)
                elements.add(grid[row][n - 1 - layer]);
            // Нижняя строка
            if (m - 1 - layer > layer)
                for (int col = n - 2 - layer; col >= layer; col--)
                    elements.add(grid[m - 1 - layer][col]);
            // Левый столбец
            if (n - 1 - layer > layer)
                for (int row = m - 2 - layer; row > layer; row--)
                    elements.add(grid[row][layer]);

            int length = elements.size();
            if (length == 0) continue;
            int shift = k % length;

            int idx = 0;
            // Верхняя строка
            for (int col = layer; col < n - layer; col++)
                grid[layer][col] = elements.get((shift + idx++) % length);
            // Правый столбец
            for (int row = layer + 1; row < m - layer; row++)
                grid[row][n - 1 - layer] = elements.get((shift + idx++) % length);
            // Нижняя строка
            if (m - 1 - layer > layer)
                for (int col = n - 2 - layer; col >= layer; col--)
                    grid[m - 1 - layer][col] = elements.get((shift + idx++) % length);
            // Левый столбец
            if (n - 1 - layer > layer)
                for (int row = m - 2 - layer; row > layer; row--)
                    grid[row][layer] = elements.get((shift + idx++) % length);
        }
        return grid;
    }
}