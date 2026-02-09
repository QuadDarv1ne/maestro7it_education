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

using System;
using System.Collections.Generic;

public class Solution {
    /**
     * Вычисляет все возможные результаты расстановки скобок в арифметическом выражении.
     * 
     * Алгоритм (разделяй и властвуй с мемоизацией):
     * 1. Для каждого оператора в выражении:
     *    - Разделяем выражение на левую и правую части
     *    - Рекурсивно вычисляем результаты для левой части
     *    - Рекурсивно вычисляем результаты для правой части
     *    - Комбинируем результаты, применяя оператор
     * 2. Если в выражении нет операторов (только число), возвращаем это число
     * 
     * Сложность:
     * Время: O(C_n), где C_n - n-е каталонское число
     * Пространство: O(C_n) для хранения результатов
     * 
     * @param expression Строка с арифметическим выражением
     * @return Все возможные результаты вычисления выражения
     * 
     * Примеры:
     * DiffWaysToCompute("2-1-1") → [0, 2]
     * DiffWaysToCompute("2*3-4*5") → [-34, -14, -10, -10, 10]
     */
    public IList<int> DiffWaysToCompute(string expression) {
        var memo = new Dictionary<string, IList<int>>();
        return Compute(expression, memo);
    }
    
    private IList<int> Compute(string expr, Dictionary<string, IList<int>> memo) {
        // Проверяем, есть ли результат в кэше
        if (memo.ContainsKey(expr)) {
            return memo[expr];
        }
        
        var results = new List<int>();
        
        // Проверяем, является ли выражение числом
        bool isNumber = true;
        foreach (char c in expr) {
            if (!char.IsDigit(c)) {
                isNumber = false;
                break;
            }
        }
        
        if (isNumber) {
            results.Add(int.Parse(expr));
            memo[expr] = results;
            return results;
        }
        
        for (int i = 0; i < expr.Length; i++) {
            char c = expr[i];
            
            // Если текущий символ - оператор
            if (c == '+' || c == '-' || c == '*') {
                // Разделяем выражение на левую и правую части
                string leftExpr = expr.Substring(0, i);
                string rightExpr = expr.Substring(i + 1);
                
                IList<int> leftResults = Compute(leftExpr, memo);
                IList<int> rightResults = Compute(rightExpr, memo);
                
                // Комбинируем результаты
                foreach (int left in leftResults) {
                    foreach (int right in rightResults) {
                        if (c == '+') {
                            results.Add(left + right);
                        } else if (c == '-') {
                            results.Add(left - right);
                        } else if (c == '*') {
                            results.Add(left * right);
                        }
                    }
                }
            }
        }
        
        memo[expr] = results;
        return results;
    }
    
    /**
     * Итеративное решение с использованием динамического программирования.
     * 
     * Алгоритм:
     * 1. Разбиваем выражение на числа и операторы
     * 2. Используем DP: dp[i][j] содержит все возможные результаты для подвыражения от i до j
     * 3. Заполняем диагонали таблицы DP
     * 
     * Сложность:
     * Время: O(n^3) в худшем случае
     * Пространство: O(n^2) для таблицы DP
     */
    public IList<int> DiffWaysToComputeDP(string expression) {
        if (string.IsNullOrEmpty(expression)) {
            return new List<int>();
        }
        
        // Разделяем выражение на числа и операторы
        var nums = new List<int>();
        var ops = new List<char>();
        int num = 0;
        
        foreach (char c in expression) {
            if (char.IsDigit(c)) {
                num = num * 10 + (c - '0');
            } else {
                nums.Add(num);
                ops.Add(c);
                num = 0;
            }
        }
        nums.Add(num);
        
        int n = nums.Count;
        
        // Инициализируем таблицу DP
        var dp = new List<int>[n, n];
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                dp[i, j] = new List<int>();
            }
        }
        
        // Заполняем диагональ (выражения из одного числа)
        for (int i = 0; i < n; i++) {
            dp[i, i].Add(nums[i]);
        }
        
        // Заполняем таблицу для подвыражений разной длины
        for (int length = 2; length <= n; length++) {
            for (int i = 0; i <= n - length; i++) {
                int j = i + length - 1;
                
                // Перебираем все возможные позиции операторов
                for (int k = i; k < j; k++) {
                    List<int> leftResults = dp[i, k];
                    List<int> rightResults = dp[k + 1, j];
                    char op = ops[k];
                    
                    // Комбинируем результаты
                    foreach (int left in leftResults) {
                        foreach (int right in rightResults) {
                            if (op == '+') {
                                dp[i, j].Add(left + right);
                            } else if (op == '-') {
                                dp[i, j].Add(left - right);
                            } else if (op == '*') {
                                dp[i, j].Add(left * right);
                            }
                        }
                    }
                }
            }
        }
        
        return dp[0, n - 1];
    }
}