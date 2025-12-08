/**
 * @file count_square_sum_triples.cpp
 * @brief Решение задачи "Count Square Sum Triples" (LeetCode 1925)
 * 
 * @author Дулей Максим Игоревич
 * @see ORCID: https://orcid.org/0009-0007-7605-539X
 * @see GitHub: https://github.com/QuadDarv1ne/
 * 
 * @details
 * Алгоритм подсчёта упорядоченных пифагоровых троек в диапазоне [1, n]
 * Сложность: O(n²) по времени, O(1) по памяти
 * 
 * @approach
 * 1. Для каждой пары (a, b) вычисляем сумму квадратов
 * 2. Находим целую часть квадратного корня
 * 3. Проверяем, что квадрат этой части равен сумме и c ≤ n
 * 4. Учитываем упорядоченность: (a,b,c) и (b,a,c) - разные тройки
 */

#include <cmath>
#include <vector>
#include <algorithm>

class Solution {
public:
    /**
     * @brief Подсчитывает количество упорядоченных пифагоровых троек
     * 
     * @param n Верхняя граница диапазона (1 ≤ n ≤ 250)
     * @return int Количество троек, удовлетворяющих a² + b² = c²
     * 
     * @example
     *   Solution sol;
     *   int result = sol.countTriples(5);    // Возвращает 2
     *   int result = sol.countTriples(10);   // Возвращает 4
     * 
     * @note
     * - Используется проверка через целочисленный квадратный корень
     * - Тройки упорядочены: (3,4,5) и (4,3,5) считаются разными
     * - Максимальное n=250 гарантирует O(n²) решение
     */
    int countTriples(int n) {
        int count = 0;
        
        for (int a = 1; a <= n; ++a) {
            for (int b = 1; b <= n; ++b) {
                int c_sq = a * a + b * b;                // a² + b²
                int c = static_cast<int>(sqrt(c_sq));    // ⌊√(a²+b²)⌋
                
                // Проверяем, что c² = a² + b² и c ≤ n
                if (c <= n && c * c == c_sq) {
                    ++count;
                }
            }
        }
        
        return count;
    }
    
    /**
     * @brief Оптимизированная версия с предварительным вычислением квадратов
     * 
     * @param n Верхняя граница диапазона
     * @return int Количество троек
     * 
     * @complexity
     * - Время: O(n²)
     * - Память: O(n) для хранения массива квадратов
     */
    int countTriplesOptimized(int n) {
        int count = 0;
        int max_sq = n * n;
        
        // Создаём массив для отметки совершенных квадратов
        std::vector<bool> is_perfect_square(max_sq + 1, false);
        for (int i = 1; i <= n; ++i) {
            is_perfect_square[i * i] = true;
        }
        
        // Перебираем все пары (a, b)
        for (int a = 1; a <= n; ++a) {
            int a_sq = a * a;
            for (int b = 1; b <= n; ++b) {
                int sum = a_sq + b * b;
                if (sum <= max_sq && is_perfect_square[sum]) {
                    ++count;
                }
            }
        }
        
        return count;
    }
};