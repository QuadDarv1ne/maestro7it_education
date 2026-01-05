/**
 * https://leetcode.com/problems/maximum-matrix-sum/
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "Maximum Matrix Sum"
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
    public long MaxMatrixSum(int[][] matrix) {
        int n = matrix.Length;
        
        // Если матрица 1x1, просто возвращаем значение
        if (n == 1) {
            return matrix[0][0];
        }
        
        long totalAbsSum = 0;
        long minAbs = long.MaxValue;
        int negativeCount = 0;
        bool hasZero = false;
        
        // Проходим по всем элементам матрицы
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                int value = matrix[i][j];
                int absValue = Math.Abs(value);
                
                totalAbsSum += absValue;
                
                // Обновляем минимальное абсолютное значение
                if (absValue < minAbs) {
                    minAbs = absValue;
                }
                
                // Считаем отрицательные элементы
                if (value < 0) {
                    negativeCount++;
                }
                
                // Проверяем наличие нуля
                if (value == 0) {
                    hasZero = true;
                }
            }
        }
        
        // Если есть ноль или четное количество отрицательных элементов,
        // можно сделать все элементы положительными
        if (hasZero || negativeCount % 2 == 0) {
            return totalAbsSum;
        }
        
        // Иначе нужно сделать один элемент отрицательным
        return totalAbsSum - 2 * minAbs;
    }
}