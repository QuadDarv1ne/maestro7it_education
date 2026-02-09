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

import java.util.*;

class Solution {
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
     * diffWaysToCompute("2-1-1") → [0, 2]
     * diffWaysToCompute("2*3-4*5") → [-34, -14, -10, -10, 10]
     */
    public List<Integer> diffWaysToCompute(String expression) {
        Map<String, List<Integer>> memo = new HashMap<>();
        return compute(expression, memo);
    }
    
    private List<Integer> compute(String expr, Map<String, List<Integer>> memo) {
        // Проверяем, есть ли результат в кэше
        if (memo.containsKey(expr)) {
            return memo.get(expr);
        }
        
        List<Integer> results = new ArrayList<>();
        
        // Проверяем, является ли выражение числом
        boolean isNumber = true;
        for (char c : expr.toCharArray()) {
            if (!Character.isDigit(c)) {
                isNumber = false;
                break;
            }
        }
        
        if (isNumber) {
            results.add(Integer.parseInt(expr));
            memo.put(expr, results);
            return results;
        }
        
        for (int i = 0; i < expr.length(); i++) {
            char c = expr.charAt(i);
            
            // Если текущий символ - оператор
            if (c == '+' || c == '-' || c == '*') {
                // Разделяем выражение на левую и правую части
                String leftExpr = expr.substring(0, i);
                String rightExpr = expr.substring(i + 1);
                
                List<Integer> leftResults = compute(leftExpr, memo);
                List<Integer> rightResults = compute(rightExpr, memo);
                
                // Комбинируем результаты
                for (int left : leftResults) {
                    for (int right : rightResults) {
                        if (c == '+') {
                            results.add(left + right);
                        } else if (c == '-') {
                            results.add(left - right);
                        } else if (c == '*') {
                            results.add(left * right);
                        }
                    }
                }
            }
        }
        
        memo.put(expr, results);
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
    public List<Integer> diffWaysToComputeDP(String expression) {
        if (expression == null || expression.isEmpty()) {
            return new ArrayList<>();
        }
        
        // Разделяем выражение на числа и операторы
        List<Integer> nums = new ArrayList<>();
        List<Character> ops = new ArrayList<>();
        int num = 0;
        
        for (char c : expression.toCharArray()) {
            if (Character.isDigit(c)) {
                num = num * 10 + (c - '0');
            } else {
                nums.add(num);
                ops.add(c);
                num = 0;
            }
        }
        nums.add(num);
        
        int n = nums.size();
        
        // Инициализируем таблицу DP
        List<Integer>[][] dp = new List[n][n];
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                dp[i][j] = new ArrayList<>();
            }
        }
        
        // Заполняем диагональ (выражения из одного числа)
        for (int i = 0; i < n; i++) {
            dp[i][i].add(nums.get(i));
        }
        
        // Заполняем таблицу для подвыражений разной длины
        for (int length = 2; length <= n; length++) {
            for (int i = 0; i <= n - length; i++) {
                int j = i + length - 1;
                
                // Перебираем все возможные позиции операторов
                for (int k = i; k < j; k++) {
                    List<Integer> leftResults = dp[i][k];
                    List<Integer> rightResults = dp[k+1][j];
                    char op = ops.get(k);
                    
                    // Комбинируем результаты
                    for (int left : leftResults) {
                        for (int right : rightResults) {
                            if (op == '+') {
                                dp[i][j].add(left + right);
                            } else if (op == '-') {
                                dp[i][j].add(left - right);
                            } else if (op == '*') {
                                dp[i][j].add(left * right);
                            }
                        }
                    }
                }
            }
        }
        
        return dp[0][n-1];
    }
}