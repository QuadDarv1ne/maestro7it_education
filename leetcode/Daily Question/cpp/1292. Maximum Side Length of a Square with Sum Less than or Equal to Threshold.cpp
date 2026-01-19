/**
 * @file Solution.cpp
 * @brief Решение задачи "Максимальная длина стороны квадрата с суммой не превышающей порог"
 * 
 * Задача:
 * Дан двумерный массив mat размера m x n и целочисленный порог threshold.
 * Необходимо найти максимальную длину стороны квадрата, сумма элементов которого
 * не превышает заданный порог. Если такого квадрата не существует, вернуть 0.
 * 
 * Алгоритм:
 * 1. Вычисление матрицы префиксных сумм для быстрого определения суммы любого подмассива.
 * 2. Использование бинарного поиска для нахождения максимальной длины стороны квадрата.
 * 3. Для каждой проверяемой длины k проверяем все возможные квадраты со стороной k.
 * 4. Если существует квадрат со стороной k и суммой ≤ threshold, пытаемся увеличить k.
 * 
 * Сложность:
 *    Время: O(m * n * log(min(m, n)))
 *    Память: O(m * n)
 * 
 * Автор: Дуплей Максим Игоревич - AGLA
 * Контакты:
 *    - GitHub: https://github.com/QuadDarv1ne/
 *    - ORCID: https://orcid.org/0009-0007-7605-539X
 * 
 * Полезные ссылки:
 * 1. ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
 * 2. Telegram №1: @quadd4rv1n7
 * 3. Telegram №2: @dupley_maxim_1999
 * 4. Rutube канал: https://rutube.ru/channel/4218729/
 * 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
 * 6. YouTube канал: https://www.youtube.com/@it-coders
 * 7. ВК группа: https://vk.com/science_geeks
 *
 * Дата: 19.01.2026
 */

#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    /**
     * @brief Находит максимальную длину стороны квадрата с суммой ≤ threshold
     * 
     * @param mat Входная матрица целых чисел размера m x n
     * @param threshold Максимально допустимая сумма элементов квадрата
     * @return int Максимальная длина стороны квадрата, или 0 если такого нет
     */
    int maxSideLength(vector<vector<int>>& mat, int threshold) {
        int m = mat.size();
        int n = mat[0].size();
        
        // Матрица префиксных сумм с дополнительными строкой и столбцом из нулей
        vector<vector<int>> prefix(m + 1, vector<int>(n + 1, 0));
        
        // Заполнение матрицы префиксных сумм
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                prefix[i + 1][j + 1] = mat[i][j] + prefix[i][j + 1] + 
                                        prefix[i + 1][j] - prefix[i][j];
            }
        }
        
        // Вспомогательная лямбда-функция для вычисления суммы квадрата
        auto squareSum = [&](int i, int j, int k) -> int {
            // Используем принцип включения-исключения для вычисления суммы квадрата
            return prefix[i + k][j + k] - prefix[i][j + k] - 
                   prefix[i + k][j] + prefix[i][j];
        };
        
        // Бинарный поиск максимальной длины стороны
        int left = 1, right = min(m, n);
        int ans = 0;
        
        while (left <= right) {
            int k = left + (right - left) / 2;
            bool found = false;
            
            // Проверяем все возможные верхние левые углы для квадрата со стороной k
            for (int i = 0; i <= m - k; i++) {
                for (int j = 0; j <= n - k; j++) {
                    if (squareSum(i, j, k) <= threshold) {
                        found = true;
                        break;
                    }
                }
                if (found) break;
            }
            
            if (found) {
                ans = k;        // Обновляем наилучший результат
                left = k + 1;   // Пробуем больший квадрат
            } else {
                right = k - 1;  // Пробуем меньший квадрат
            }
        }
        
        return ans;
    }
};