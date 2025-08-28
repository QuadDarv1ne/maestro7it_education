/**
 * https://leetcode.com/problems/sort-matrix-by-diagonals/description/?envType=daily-question&envId=2025-08-28
 */

import java.util.*;

class Solution {
    /**
     * sortMatrix
     *
     * Сортирует диагонали квадратной матрицы n x n:
     * - диагонали, начинающиеся в левой колонке (включая главную), сортировать по убыванию;
     * - диагонали, начинающиеся в верхней строке (кроме (0,0)), сортировать по возрастанию.
     *
     * @param grid n x n матрица
     * @return модифицированная матрица
     */
    public int[][] sortMatrix(int[][] grid) {
        int n = grid.length;
        if (n == 0) return grid;

        // Нижне-левая часть + главная диагональ (start_row от n-1 до 0)
        for (int startRow = n - 1; startRow >= 0; startRow--) {
            int i = startRow, j = 0;
            List<Integer> vals = new ArrayList<>();
            while (i < n && j < n) {
                vals.add(grid[i][j]);
                i++; j++;
            }
            // non-increasing
            vals.sort(Collections.reverseOrder());
            i = startRow; j = 0;
            int k = 0;
            while (i < n && j < n) {
                grid[i][j] = vals.get(k++);
                i++; j++;
            }
        }

        // Верхне-правая часть (кроме главной): start_col от 1 до n-1
        for (int startCol = 1; startCol < n; startCol++) {
            int i = 0, j = startCol;
            List<Integer> vals = new ArrayList<>();
            while (i < n && j < n) {
                vals.add(grid[i][j]);
                i++; j++;
            }
            // non-decreasing
            Collections.sort(vals);
            i = 0; j = startCol;
            int k = 0;
            while (i < n && j < n) {
                grid[i][j] = vals.get(k++);
                i++; j++;
            }
        }

        return grid;
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