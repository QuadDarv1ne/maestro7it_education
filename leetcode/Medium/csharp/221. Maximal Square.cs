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
    /**
     * Находит максимальную площадь квадрата из '1' в бинарной матрице.
     * 
     * Алгоритм использует динамическое программирование с оптимизацией памяти.
     * Вместо полной матрицы dp используется только два массива:
     * - prev: предыдущая строка
     * - curr: текущая строка
     * 
     * @param matrix Двоичная матрица из символов '0' и '1'
     * @return Площадь максимального квадрата
     */
    public int MaximalSquare(char[][] matrix) {
        if (matrix == null || matrix.Length == 0 || matrix[0].Length == 0) 
            return 0;
        
        int m = matrix.Length;
        int n = matrix[0].Length;
        int[] prev = new int[n];
        int[] curr = new int[n];
        int maxSide = 0;
        
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (matrix[i][j] == '1') {
                    if (i == 0 || j == 0) {
                        curr[j] = 1;
                    } else {
                        curr[j] = Math.Min(Math.Min(prev[j], curr[j-1]), prev[j-1]) + 1;
                    }
                    maxSide = Math.Max(maxSide, curr[j]);
                } else {
                    curr[j] = 0;
                }
            }
            
            // Обновляем массивы для следующей строки
            int[] temp = prev;
            prev = curr;
            curr = temp;
            // Очищаем curr для следующей итерации
            Array.Clear(curr, 0, n);
        }
        
        return maxSide * maxSide;
    }
}