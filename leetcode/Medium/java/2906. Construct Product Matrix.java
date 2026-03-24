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
 * Строит матрицу произведений, где каждый элемент p[i][j] равен произведению
 * всех элементов исходной матрицы, кроме grid[i][j], по модулю 12345.
 * 
 * Параметры:
 *     grid - исходная матрица целых чисел размером n x m
 * 
 * Возвращает:
 *     матрицу произведений по модулю 12345
 * 
 * Примечания:
 *     - Модуль 12345 = 3 * 5 * 823 (составное число)
 *     - Нельзя использовать деление или обратные элементы
 *     - Используется метод префиксных и суффиксных произведений
 *     - Сложность: O(n*m) по времени и O(n*m) по памяти
 */

class Solution {
    public int[][] constructProductMatrix(int[][] grid) {
        final int MOD = 12345;
        int n = grid.length, m = grid[0].length;
        int total = n * m;
        
        // Преобразуем 2D матрицу в 1D массив для удобства
        int[] arr = new int[total];
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < m; ++j) {
                arr[i * m + j] = grid[i][j] % MOD;
            }
        }
        
        // Префиксные произведения
        int[] prefix = new int[total];
        prefix[0] = 1;
        for (int i = 1; i < total; ++i) {
            prefix[i] = (int)(((long)prefix[i - 1] * arr[i - 1]) % MOD);
        }
        
        // Суффиксные произведения
        int[] suffix = new int[total];
        suffix[total - 1] = 1;
        for (int i = total - 2; i >= 0; --i) {
            suffix[i] = (int)(((long)suffix[i + 1] * arr[i + 1]) % MOD);
        }
        
        // Результат для каждого элемента
        int[][] result = new int[n][m];
        for (int i = 0; i < total; ++i) {
            int row = i / m, col = i % m;
            result[row][col] = (int)(((long)prefix[i] * suffix[i]) % MOD);
        }
        
        return result;
    }
}