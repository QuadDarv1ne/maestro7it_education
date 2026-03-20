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
    public int[][] minAbsDiff(int[][] grid, int k) {
        int m = grid.length;
        int n = grid[0].length;
        int rows = m - k + 1;
        int cols = n - k + 1;
        
        int[][] result = new int[rows][cols];
        
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                // TreeSet для автоматической сортировки уникальных значений
                TreeSet<Integer> uniqueVals = new TreeSet<>();
                for (int x = i; x < i + k; x++) {
                    for (int y = j; y < j + k; y++) {
                        uniqueVals.add(grid[x][y]);
                    }
                }
                
                // Если все значения одинаковы
                if (uniqueVals.size() == 1) {
                    result[i][j] = 0;
                    continue;
                }
                
                // Преобразуем TreeSet в массив (уже отсортирован)
                Integer[] sortedVals = uniqueVals.toArray(new Integer[0]);
                
                // Ищем минимальную разность
                int minDiff = Integer.MAX_VALUE;
                for (int idx = 1; idx < sortedVals.length; idx++) {
                    int diff = sortedVals[idx] - sortedVals[idx - 1];
                    if (diff < minDiff) {
                        minDiff = diff;
                    }
                }
                
                result[i][j] = minDiff;
            }
        }
        
        return result;
    }
}