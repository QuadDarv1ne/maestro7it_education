/**
 * https://leetcode.com/problems/number-of-islands/description/
 */

public class Solution {
    /// <summary>
    /// Считает количество островов на карте.
    /// 
    /// Алгоритм:
    /// 1. Пробегаем по всем клеткам матрицы grid.
    /// 2. Если встречаем '1' (земля), увеличиваем счетчик островов.
    /// 3. Запускаем DFS от этой клетки, чтобы пометить все смежные клетки как посещённые ('0').
    /// 4. DFS рекурсивно проходит вверх, вниз, влево и вправо.
    ///
    /// Временная сложность: O(m * n), где m — число строк, n — число столбцов.
    /// Память: O(m * n) в худшем случае из-за рекурсии.
    /// </summary>
    /// <param name="grid">Двумерный массив символов '1' и '0'</param>
    /// <returns>Количество островов</returns>
    public int NumIslands(char[][] grid) {
        if (grid == null || grid.Length == 0) return 0;
        
        int count = 0;
        int rows = grid.Length;
        int cols = grid[0].Length;
        
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                if (grid[i][j] == '1') {
                    count++;
                    DFS(grid, i, j, rows, cols);
                }
            }
        }
        return count;
    }

    /// <summary>
    /// Рекурсивный DFS для пометки всех смежных клеток острова как посещённые.
    /// </summary>
    /// <param name="grid">Карта островов</param>
    /// <param name="i">Текущая строка</param>
    /// <param name="j">Текущий столбец</param>
    /// <param name="rows">Количество строк</param>
    /// <param name="cols">Количество столбцов</param>
    private void DFS(char[][] grid, int i, int j, int rows, int cols) {
        if (i < 0 || i >= rows || j < 0 || j >= cols || grid[i][j] == '0') return;

        grid[i][j] = '0'; // Помечаем клетку как посещённую

        DFS(grid, i + 1, j, rows, cols);
        DFS(grid, i - 1, j, rows, cols);
        DFS(grid, i, j + 1, rows, cols);
        DFS(grid, i, j - 1, rows, cols);
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