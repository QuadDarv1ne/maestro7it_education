/**
 * https://leetcode.com/problems/spiral-matrix/description/
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "Spiral Matrix" на C#
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

using System;
using System.Collections.Generic;

public class Solution {
    public IList<int> SpiralOrder(int[][] matrix) {
        var result = new List<int>();
        if (matrix == null || matrix.Length == 0 || matrix[0].Length == 0) {
            return result;
        }
        
        int top = 0, bottom = matrix.Length - 1;
        int left = 0, right = matrix[0].Length - 1;
        
        while (top <= bottom && left <= right) {
            // Слева направо
            for (int i = left; i <= right; i++) {
                result.Add(matrix[top][i]);
            }
            top++;
            
            // Сверху вниз
            for (int i = top; i <= bottom; i++) {
                result.Add(matrix[i][right]);
            }
            right--;
            
            // Справа налево
            if (top <= bottom) {
                for (int i = right; i >= left; i--) {
                    result.Add(matrix[bottom][i]);
                }
                bottom--;
            }
            
            // Снизу вверх
            if (left <= right) {
                for (int i = bottom; i >= top; i--) {
                    result.Add(matrix[i][left]);
                }
                left++;
            }
        }
        
        return result;
    }
}