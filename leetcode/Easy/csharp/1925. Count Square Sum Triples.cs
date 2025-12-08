/// <summary>
/// Решение задачи "Count Square Sum Triples" (LeetCode 1925)
/// </summary>
/// <remarks>
/// <para>Алгоритм подсчёта упорядоченных пифагоровых троек в диапазоне [1, n].</para>
/// 
/// <para>Сложность:</para>
/// <list type="bullet">
///   <item><description>Время: O(n²), где n - верхняя граница</description></item>
///   <item><description>Память: O(1) для базового решения, O(n) для оптимизированного</description></item>
/// </list>
/// 
/// <para>Автор: Дулей Максим Игоревич</para>
/// <para>ORCID: https://orcid.org/0009-0007-7605-539X</para>
/// <para>GitHub: https://github.com/QuadDarv1ne/</para>
/// </remarks>
public class Solution {
    /// <summary>
    /// Подсчитывает количество упорядоченных пифагоровых троек
    /// </summary>
    /// <param name="n">Верхняя граница диапазона (1 ≤ n ≤ 250)</param>
    /// <returns>Количество троек, удовлетворяющих a² + b² = c²</returns>
    /// 
    /// <example>
    /// <code>
    /// var solution = new Solution();
    /// int result1 = solution.CountTriples(5);   // 2
    /// int result2 = solution.CountTriples(10);  // 4
    /// </code>
    /// </example>
    /// 
    /// <algorithm>
    /// 1. Для каждой пары (a, b) вычисляем сумму квадратов
    /// 2. Находим целую часть квадратного корня
    /// 3. Проверяем, что квадрат этой части равен сумме и c ≤ n
    /// 4. Учитываем упорядоченность троек
    /// </algorithm>
    public int CountTriples(int n) {
        int count = 0;
        
        for (int a = 1; a <= n; a++) {
            for (int b = 1; b <= n; b++) {
                int c_sq = a * a + b * b;
                int c = (int)Math.Sqrt(c_sq);
                
                if (c <= n && c * c == c_sq) {
                    count++;
                }
            }
        }
        
        return count;
    }
    
    /// <summary>
    /// Оптимизированная версия с использованием HashSet
    /// </summary>
    /// <param name="n">Верхняя граница диапазона</param>
    /// <returns>Количество троек</returns>
    public int CountTriplesOptimized(int n) {
        var squares = new HashSet<int>();
        
        // Предварительно вычисляем все квадраты
        for (int i = 1; i <= n; i++) {
            squares.Add(i * i);
        }
        
        int count = 0;
        int maxSquare = n * n;
        
        // Перебираем все пары квадратов
        foreach (int a_sq in squares) {
            foreach (int b_sq in squares) {
                int sum = a_sq + b_sq;
                if (sum <= maxSquare && squares.Contains(sum)) {
                    count++;
                }
            }
        }
        
        return count;
    }
    
    /// <summary>
    /// Версия с массивом для быстрой проверки
    /// </summary>
    public int CountTriplesArray(int n) {
        int maxSquare = n * n;
        bool[] isPerfectSquare = new bool[maxSquare + 1];
        
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
}