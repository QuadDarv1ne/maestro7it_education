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

public class Solution {
    /// <summary>
    /// Поворачивает матрицу и применяет гравитацию к камням.
    /// </summary>
    /// <param name="boxGrid">Исходная матрица (вид сбоку).
    /// '#' - камень, '*' - препятствие, '.' - пустота.</param>
    /// <returns>Повёрнутая матрица после падения камней.</returns>
    public char[][] RotateTheBox(char[][] boxGrid) {
        int m = boxGrid.Length;
        int n = boxGrid[0].Length;

        // Этап 1: Симуляция гравитации справа-налево в каждой строке
        for (int i = 0; i < m; ++i) {
            int emptyPos = n - 1;
            for (int j = n - 1; j >= 0; --j) {
                if (boxGrid[i][j] == '*') {
                    emptyPos = j - 1;
                } else if (boxGrid[i][j] == '#') {
                    // Перемещаем камень в доступную позицию emptyPos
                    char temp = boxGrid[i][j];
                    boxGrid[i][j] = boxGrid[i][emptyPos];
                    boxGrid[i][emptyPos] = temp;
                    --emptyPos;
                }
            }
        }

        // Этап 2: Поворот матрицы на 90 градусов по часовой стрелке
        char[][] rotatedBox = new char[n][];
        for (int i = 0; i < n; ++i) {
            rotatedBox[i] = new char[m];
        }

        for (int i = 0; i < m; ++i) {
            for (int j = 0; j < n; ++j) {
                rotatedBox[j][m - 1 - i] = boxGrid[i][j];
            }
        }

        return rotatedBox;
    }
}