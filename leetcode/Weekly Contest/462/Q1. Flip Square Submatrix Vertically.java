/**
 * https://leetcode.com/contest/weekly-contest-462/problems/flip-square-submatrix-vertically/submissions/
 */

public class Solution {
    /**
     * Переворачивает по вертикали квадратную подматрицу k×k в матрице grid.
     *
     * @param grid m×n матрица целых чисел
     * @param x индекс строки верхнего левого угла подматрицы
     * @param y индекс столбца верхнего левого угла подматрицы
     * @param k размер стороны подматрицы
     * @return матрица после вертикального переворота подматрицы
     *
     * Алгоритм:
     * 1. Идём от верхней границы подматрицы к середине.
     * 2. Меняем строки местами внутри выбранной области.
     * 3. Остальная часть матрицы не изменяется.
     * Сложность: O(k²) времени, O(1) памяти.
     */
    public int[][] reverseSubmatrix(int[][] grid, int x, int y, int k) {
        for (int i = 0; i < k / 2; i++) {
            int topRow = x + i;
            int bottomRow = x + k - 1 - i;
            for (int j = 0; j < k; j++) {
                int col = y + j;
                int temp = grid[topRow][col];
                grid[topRow][col] = grid[bottomRow][col];
                grid[bottomRow][col] = temp;
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