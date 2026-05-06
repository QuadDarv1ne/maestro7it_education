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
#include <string>

using namespace std;

class Solution {
public:
    /**
     * Поворачивает матрицу и применяет гравитацию к камням.
     *
     * @param boxGrid Исходная матрица с символьным представлением коробки:
     *                '#' - камень, '*' - препятствие, '.' - пустота.
     * @return Новая матрица, повернутая на 90 градусов по часовой стрелке
     *         после применения гравитации.
     */
    vector<vector<char>> rotateTheBox(vector<vector<char>>& boxGrid) {
        int m = boxGrid.size();
        int n = boxGrid[0].size();

        // Этап 1: Применяем гравитацию в каждой строке (сдвигаем камни вправо)
        for (auto& row : boxGrid) {
            int emptyPos = n - 1; // Указывает на самую правую свободную позицию в строке
            for (int col = n - 1; col >= 0; --col) {
                if (row[col] == '*') {
                    // Наткнулись на препятствие - обнуляем позицию для вставки
                    emptyPos = col - 1;
                } else if (row[col] == '#') {
                    // Меняем местами камень и свободную ячейку
                    swap(row[col], row[emptyPos]);
                    --emptyPos;
                }
            }
        }

        // Этап 2: Поворачиваем матрицу на 90 градусов по часовой стрелке
        vector<vector<char>> rotatedBox(n, vector<char>(m));
        for (int i = 0; i < m; ++i) {
            for (int j = 0; j < n; ++j) {
                rotatedBox[j][m - 1 - i] = boxGrid[i][j];
            }
        }

        return rotatedBox;
    }
};