/**
 * Решение задачи "Count Square Sum Triples" (LeetCode 1925)
 * 
 * <p>Алгоритм подсчёта упорядоченных пифагоровых троек в диапазоне [1, n].</p>
 * 
 * <p>Сложность:
 * <ul>
 *   <li>Время: O(n²), где n - верхняя граница</li>
 *   <li>Память: O(1) для базового решения, O(n) для оптимизированного</li>
 * </ul></p>
 * 
 * <p>Автор: Дулей Максим Игоревич<br>
 * ORCID: https://orcid.org/0009-0007-7605-539X<br>
 * GitHub: https://github.com/QuadDarv1ne/</p>
 */
public class Solution {
    /**
     * Подсчитывает количество упорядоченных пифагоровых троек
     * 
     * @param n Верхняя граница диапазона (1 ≤ n ≤ 250)
     * @return Количество троек, удовлетворяющих a² + b² = c²
     * 
     * @example
     * <pre>
     * Solution sol = new Solution();
     * int result1 = sol.countTriples(5);   // 2
     * int result2 = sol.countTriples(10);  // 4
     * </pre>
     * 
     * @algorithm
     * 1. Для каждой пары (a, b) вычисляем сумму квадратов
     * 2. Находим целую часть квадратного корня
     * 3. Проверяем, что квадрат этой части равен сумме и c ≤ n
     * 4. Учитываем упорядоченность троек
     */
    public int countTriples(int n) {
        int count = 0;
        
        for (int a = 1; a <= n; a++) {
            for (int b = 1; b <= n; b++) {
                int c_sq = a * a + b * b;
                int c = (int) Math.sqrt(c_sq);
                
                if (c <= n && c * c == c_sq) {
                    count++;
                }
            }
        }
        
        return count;
    }
    
    /**
     * Оптимизированная версия с использованием HashSet
     * 
     * @param n Верхняя граница диапазона
     * @return Количество троек
     */
    public int countTriplesOptimized(int n) {
        java.util.HashSet<Integer> squares = new java.util.HashSet<>();
        
        // Предварительно вычисляем все квадраты
        for (int i = 1; i <= n; i++) {
            squares.add(i * i);
        }
        
        int count = 0;
        int maxSquare = n * n;
        
        // Перебираем все пары квадратов
        for (int a_sq : squares) {
            for (int b_sq : squares) {
                int sum = a_sq + b_sq;
                if (sum <= maxSquare && squares.contains(sum)) {
                    count++;
                }
            }
        }
        
        return count;
    }
    
    /**
     * Версия с массивом для быстрой проверки
     */
    public int countTriplesArray(int n) {
        int maxSquare = n * n;
        boolean[] isPerfectSquare = new boolean[maxSquare + 1];
        
        // Отмечаем совершенные квадраты
        for (int i = 1; i <= n; i++) {
            isPerfectSquare[i * i] = true;
        }
        
        int count = 0;
        
        // Перебираем все пары (a, b)
        for (int a = 1; a <= n; a++) {
            int a_sq = a * a;
            for (int b = 1; b <= n; b++) {
                int sum = a_sq + b * b;
                if (sum <= maxSquare && isPerfectSquare[sum]) {
                    count++;
                }
            }
        }
        
        return count;
    }
    
    /**
     * Расширенная версия с возвратом списка троек (для отладки)
     */
    public java.util.List<int[]> findTriples(int n) {
        java.util.List<int[]> triples = new java.util.ArrayList<>();
        
        for (int a = 1; a <= n; a++) {
            for (int b = 1; b <= n; b++) {
                int c_sq = a * a + b * b;
                int c = (int) Math.sqrt(c_sq);
                
                if (c <= n && c * c == c_sq) {
                    triples.add(new int[]{a, b, c});
                }
            }
        }
        
        return triples;
    }
    
    // Пример использования
    public static void main(String[] args) {
        Solution solution = new Solution();
        
        System.out.println("Тестирование Count Square Sum Triples:");
        System.out.println("======================================");
        
        // Тестовые случаи
        int[][] tests = {{5, 2}, {10, 4}, {1, 0}, {2, 0}, {13, 6}, {250, 650}};
        
        for (int[] test : tests) {
            int n = test[0];
            int expected = test[1];
            int result = solution.countTriples(n);
            String status = result == expected ? "✓" : "✗";
            System.out.printf("%s n=%d: %d (ожидалось %d)%n", 
                status, n, result, expected);
        }
        
        // Демонстрация нахождения троек
        System.out.println("\nТройки для n=13:");
        java.util.List<int[]> triples = solution.findTriples(13);
        for (int[] triple : triples) {
            System.out.printf("(%d, %d, %d)%n", triple[0], triple[1], triple[2]);
        }
    }
}