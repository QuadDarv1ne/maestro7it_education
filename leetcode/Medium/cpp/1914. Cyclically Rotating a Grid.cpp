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

#include <vector>
using namespace std;

class Solution {
public:
    /*
     * Циклически сдвигает каждый слой матрицы на k шагов против часовой стрелки.
     * @param grid Исходная матрица m x n (m и n - чётные).
     * @param k Количество циклических сдвигов.
     * @return Матрица после выполнения k циклических сдвигов для каждого слоя.
     */
    vector<vector<int>> rotateGrid(vector<vector<int>>& grid, int k) {
        int m = grid.size();
        int n = grid[0].size();
        int layers = min(m, n) / 2;

        for (int layer = 0; layer < layers; ++layer) {
            vector<int> elements;

            // Верхняя строка
            for (int col = layer; col < n - layer; ++col)
                elements.push_back(grid[layer][col]);
            // Правый столбец
            for (int row = layer + 1; row < m - layer; ++row)
                elements.push_back(grid[row][n - 1 - layer]);
            // Нижняя строка
            if (m - 1 - layer > layer)
                for (int col = n - 2 - layer; col >= layer; --col)
                    elements.push_back(grid[m - 1 - layer][col]);
            // Левый столбец
            if (n - 1 - layer > layer)
                for (int row = m - 2 - layer; row > layer; --row)
                    elements.push_back(grid[row][layer]);

            int length = elements.size();
            if (length == 0) continue;
            int shift = k % length;

            // Записываем обратно со сдвигом
            int idx = 0;
            // Верхняя строка
            for (int col = layer; col < n - layer; ++col)
                grid[layer][col] = elements[(shift + idx++) % length];
            // Правый столбец
            for (int row = layer + 1; row < m - layer; ++row)
                grid[row][n - 1 - layer] = elements[(shift + idx++) % length];
            // Нижняя строка
            if (m - 1 - layer > layer)
                for (int col = n - 2 - layer; col >= layer; --col)
                    grid[m - 1 - layer][col] = elements[(shift + idx++) % length];
            // Левый столбец
            if (n - 1 - layer > layer)
                for (int row = m - 2 - layer; row > layer; --row)
                    grid[row][layer] = elements[(shift + idx++) % length];
        }
        return grid;
    }
};