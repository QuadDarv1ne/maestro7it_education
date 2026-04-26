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

import java.util.*;

class Solution {
    /**
     * Возвращает индексы k самых слабых строк бинарной матрицы.
     *
     * @param mat матрица m x n из 0 и 1
     * @param k   количество слабейших строк
     * @return массив индексов от самой слабой к более сильной
     */
    public int[] kWeakestRows(int[][] mat, int k) {
        int m = mat.length;
        int n = mat[0].length;
        int[] soldiers = new int[m];
        
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
        
        // Создаём список индексов и сортируем
        Integer[] indices = new Integer[m];
        for (int i = 0; i < m; i++) indices[i] = i;
        Arrays.sort(indices, (a, b) -> {
            if (soldiers[a] != soldiers[b])
                return Integer.compare(soldiers[a], soldiers[b]);
            return Integer.compare(a, b);
        });
        
        int[] ans = new int[k];
        for (int i = 0; i < k; i++) ans[i] = indices[i];
        return ans;
    }
}