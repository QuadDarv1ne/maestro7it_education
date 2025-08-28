/**
 * https://leetcode.com/problems/sort-matrix-by-diagonals/description/?envType=daily-question&envId=2025-08-28
 */

#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    /**
     * sortMatrix
     *
     * Сортировка диагоналей квадратной матрицы n x n.
     * Нижне-левая часть + главная — сортировать по убыванию.
     * Верхне-правая (кроме главной) — по возрастанию.
     */
    vector<vector<int>> sortMatrix(vector<vector<int>>& grid) {
        int n = grid.size();
        if (n == 0) return grid;

        // Нижне-левая часть + главная
        for (int startRow = n - 1; startRow >= 0; --startRow) {
            int i = startRow, j = 0;
            vector<int> vals;
            while (i < n && j < n) {
                vals.push_back(grid[i][j]);
                ++i; ++j;
            }
            // non-increasing
            sort(vals.begin(), vals.end(), greater<int>());
            i = startRow; j = 0;
            int k = 0;
            while (i < n && j < n) {
                grid[i][j] = vals[k++];
                ++i; ++j;
            }
        }

        // Верхне-правая часть (кроме главной)
        for (int startCol = 1; startCol < n; ++startCol) {
            int i = 0, j = startCol;
            vector<int> vals;
            while (i < n && j < n) {
                vals.push_back(grid[i][j]);
                ++i; ++j;
            }
            // non-decreasing
            sort(vals.begin(), vals.end());
            i = 0; j = startCol;
            int k = 0;
            while (i < n && j < n) {
                grid[i][j] = vals[k++];
                ++i; ++j;
            }
        }

        return grid;
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