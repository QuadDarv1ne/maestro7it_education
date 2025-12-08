/**
 * Решение задачи "Count Square Sum Triples" (LeetCode 1925)
 * 
 * @file count_square_sum_triples.rs
 * @brief Подсчёт всех упорядоченных троек (a, b, c), удовлетворяющих условию a² + b² = c²
 * 
 * @author Дулей Максим Игоревич
 * @see ORCID: https://orcid.org/0009-0007-7605-539X
 * @see GitHub: https://github.com/QuadDarv1ne/
 * 
 * @details
 * Алгоритм: Двойной цикл с проверкой через вычисление квадратного корня
 * Сложность: O(n²) по времени, O(1) по памяти
 * 
 * @approach
 * 1. Для каждой пары (a, b) вычисляем a² + b²
 * 2. Находим целую часть квадратного корня суммы
 * 3. Проверяем, что c² = a² + b² и c ≤ n
 * 4. Учитываем, что тройки (a, b, c) и (b, a, c) считаются разными
 */

impl Solution {
    /**
     * Подсчитывает количество троек Пифагора в диапазоне [1, n]
     * 
     * @param n Верхняя граница диапазона (1 ≤ n ≤ 250)
     * @return i32 Количество упорядоченных троек (a, b, c)
     * 
     * @example
     * let solution = Solution::new();
     * assert_eq!(solution.count_triples(5), 2);   // (3,4,5) и (4,3,5)
     * assert_eq!(solution.count_triples(10), 4);  // добавляется (6,8,10) и (8,6,10)
     * 
     * @note
     * - Используется проверка через целочисленный квадратный корень
     * - Тройки считаются упорядоченными: (3,4,5) ≠ (4,3,5)
     * - Максимальное n = 250, что гарантирует работу O(n²)
     */
    pub fn count_triples(n: i32) -> i32 {
        let mut count = 0;
        
        // Перебираем все возможные значения a и b
        for a in 1..=n {
            for b in 1..=n {
                let c_sq = a * a + b * b;        // Вычисляем a² + b²
                let c = (c_sq as f64).sqrt() as i32;  // Целая часть √(a² + b²)
                
                // Проверяем, что c² = a² + b² и c не превышает n
                if c <= n && c * c == c_sq {
                    count += 1;
                }
            }
        }
        
        count
    }
}

// Модульные тесты
#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_basic_cases() {
        let solution = Solution;
        assert_eq!(solution.count_triples(5), 2);
        assert_eq!(solution.count_triples(10), 4);
        assert_eq!(solution.count_triples(1), 0);
        assert_eq!(solution.count_triples(2), 0);
        assert_eq!(solution.count_triples(13), 6);
    }
    
    #[test]
    fn test_edge_cases() {
        let solution = Solution;
        assert_eq!(solution.count_triples(250), 650); // Для n=250
    }
}