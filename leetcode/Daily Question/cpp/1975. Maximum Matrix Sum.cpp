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

#include <vector>
#include <algorithm>
#include <climits>
using namespace std;

class Solution {
public:
    long long maxMatrixSum(vector<vector<int>>& matrix) {
        int n = matrix.size();
        
        // Если матрица 1x1, просто возвращаем значение
        if (n == 1) {
            return matrix[0][0];
        }
        
        long long total_abs_sum = 0;
        long long min_abs = LLONG_MAX;
        int negative_count = 0;
        bool has_zero = false;
        
        // Проходим по всем элементам матрицы
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                int value = matrix[i][j];
                int abs_value = abs(value);
                
                total_abs_sum += abs_value;
                
                // Обновляем минимальное абсолютное значение
                if (abs_value < min_abs) {
                    min_abs = abs_value;
                }
                
                // Считаем отрицательные элементы
                if (value < 0) {
                    negative_count++;
                }
                
                // Проверяем наличие нуля
                if (value == 0) {
                    has_zero = true;
                }
            }
        }
        
        // Если есть ноль или четное количество отрицательных элементов,
        // можно сделать все элементы положительными
        if (has_zero || negative_count % 2 == 0) {
            return total_abs_sum;
        }
        
        // Иначе нужно сделать один элемент отрицательным
        return total_abs_sum - 2 * min_abs;
    }
};