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
 * 
 * Находит максимальное неотрицательное произведение на пути из (0,0) в (m-1,n-1).
 * 
 * Параметры:
 *     grid - матрица целых чисел размером m x n
 * 
 * Возвращает:
 *     максимальное неотрицательное произведение по модулю 10^9+7,
 *     или -1, если такого произведения нет
 * 
 * Примечания:
 *     - Движение возможно только вправо или вниз
 *     - Отрицательные числа могут менять знак произведения
 *     - Используется динамическое программирование с отслеживанием
 *       максимального и минимального произведения в каждой ячейке
 *     - Сложность: O(m*n) по времени и O(m*n) по памяти
 */

class Solution {
    public int maxProductPath(int[][] grid) {
        final int MOD = 1_000_000_007;
        int m = grid.length, n = grid[0].length;
        
        long[][] maxDP = new long[m][n];
        long[][] minDP = new long[m][n];
        
        // Инициализация начальной ячейки
        maxDP[0][0] = minDP[0][0] = grid[0][0];
        
        // Заполняем первую строку
        for (int j = 1; j < n; j++) {
            maxDP[0][j] = minDP[0][j] = maxDP[0][j-1] * grid[0][j];
        }
        
        // Заполняем первый столбец
        for (int i = 1; i < m; i++) {
            maxDP[i][0] = minDP[i][0] = maxDP[i-1][0] * grid[i][0];
        }
        
        // Основной DP
        for (int i = 1; i < m; i++) {
            for (int j = 1; j < n; j++) {
                long curr = grid[i][j];
                long[] candidates = {
                    maxDP[i-1][j] * curr,
                    minDP[i-1][j] * curr,
                    maxDP[i][j-1] * curr,
                    minDP[i][j-1] * curr
                };
                
                long maxVal = Long.MIN_VALUE;
                long minVal = Long.MAX_VALUE;
                for (long val : candidates) {
                    maxVal = Math.max(maxVal, val);
                    minVal = Math.min(minVal, val);
                }
                maxDP[i][j] = maxVal;
                minDP[i][j] = minVal;
            }
        }
        
        long result = maxDP[m-1][n-1];
        if (result < 0) return -1;
        return (int)(result % MOD);
    }
}