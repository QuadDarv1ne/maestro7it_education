/**
 * https://leetcode.com/problems/find-the-minimum-area-to-cover-all-ones-i/description/?envType=daily-question&envId=2025-08-22
 */

public class Solution {
    /// <summary>
    /// Функция вычисляет минимальную площадь прямоугольника, покрывающего все единицы в матрице.
    ///
    /// Алгоритм:
    /// 1. Находим минимальные и максимальные индексы строк и столбцов, где встречается '1'.
    /// 2. Площадь вычисляется как:
    ///    (maxRow - minRow + 1) * (maxCol - minCol + 1).
    /// 3. Если в матрице нет единиц, возвращаем 0.
    ///
    /// Сложность:
    /// - Время: O(m * n), где m и n — размеры матрицы.
    /// - Память: O(1).
    /// </summary>
    public int MinimumArea(int[][] grid) {
        int m = grid.Length;
        int n = grid[0].Length;

        int minR = int.MaxValue, minC = int.MaxValue;
        int maxR = -1, maxC = -1;

        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (grid[i][j] == 1) {
                    if (i < minR) minR = i;
                    if (j < minC) minC = j;
                    if (i > maxR) maxR = i;
                    if (j > maxC) maxC = j;
                }
            }
        }

        if (maxR == -1) return 0; // если единиц нет
        return (maxR - minR + 1) * (maxC - minC + 1);
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