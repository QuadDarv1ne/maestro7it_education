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
    /// Возвращает индексы k самых слабых строк бинарной матрицы.
    /// </summary>
    /// <param name="mat">матрица m x n из 0 и 1</param>
    /// <param name="k">количество слабейших строк</param>
    /// <returns>массив индексов строк от самой слабой к более сильной</returns>
    public int[] KWeakestRows(int[][] mat, int k) {
        int m = mat.Length;
        int n = mat[0].Length;
        var soldiers = new int[m];
        
        for (int i = 0; i < m; i++) {
            int left = 0, right = n;
            while (left < right) {
                int mid = left + (right - left) / 2;
                if (mat[i][mid] == 1)
                    left = mid + 1;
                else
                    right = mid;
            }
            soldiers[i] = left;
        }
        
        // Сортировка индексов
        var indices = Enumerable.Range(0, m).OrderBy(i => soldiers[i]).ThenBy(i => i).ToArray();
        return indices.Take(k).ToArray();
    }
}