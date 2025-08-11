/**
 * https://leetcode.com/contest/weekly-contest-462/problems/flip-square-submatrix-vertically/submissions/
 */

class Solution {
public:
    /**
     * reverseSubmatrix:
     * Переворачивает по вертикали квадратную подматрицу k×k внутри grid.
     *
     * @param grid m×n матрица целых чисел
     * @param x индекс строки верхнего левого угла подматрицы
     * @param y индекс столбца верхнего левого угла подматрицы
     * @param k длина стороны подматрицы
     * @return изменённая матрица после переворота
     *
     * Алгоритм:
     * - Меняем местами верхнюю и нижнюю строки внутри подматрицы.
     * - Делаем это до середины области.
     * Сложность: O(k²) по времени, O(1) по памяти.
     */
    vector<vector<int>> reverseSubmatrix(vector<vector<int>>& grid, int x, int y, int k) {
        for (int i = 0; i < k / 2; i++) {
            int topRow = x + i;
            int bottomRow = x + k - 1 - i;
            for (int j = 0; j < k; j++) {
                int col = y + j;
                swap(grid[topRow][col], grid[bottomRow][col]);
            }
        }
        return grid; // обязательно возвращаем матрицу
    }
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