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

class Solution {
    /**
     * Поворачивает матрицу и применяет гравитацию к камням.
     *
     * @param boxGrid Исходная матрица символов, где
     *                '#' представляет камень,
     *                '*' представляет препятствие,
     *                '.' представляет пустую ячейку.
     * @return Новая матрица, повёрнутая на 90 градусов по часовой стрелке после падения камней.
     */
    public char[][] rotateTheBox(char[][] boxGrid) {
        int m = boxGrid.length;
        int n = boxGrid[0].length;

        // Этап 1: Двигаем камни вправо до упора
        for (int i = 0; i < m; i++) {
            int emptyPos = n - 1;
            for (int j = n - 1; j >= 0; j--) {
                if (boxGrid[i][j] == '*') {
                    // Препятствие останавливает камни, обновляем целевую позицию
                    emptyPos = j - 1;
                } else if (boxGrid[i][j] == '#') {
                    // Меняем местами камень и пустоту
                    char temp = boxGrid[i][j];
                    boxGrid[i][j] = boxGrid[i][emptyPos];
                    boxGrid[i][emptyPos] = temp;
                    emptyPos--;
                }
            }
        }

        // Этап 2: Создаём и заполняем повёрнутую матрицу
        char[][] rotatedBox = new char[n][m];
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                rotatedBox[j][m - 1 - i] = boxGrid[i][j];
            }
        }

        return rotatedBox;
    }
}