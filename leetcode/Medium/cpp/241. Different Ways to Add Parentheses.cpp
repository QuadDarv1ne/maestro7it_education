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

#include <vector>
#include <string>
#include <unordered_map>
#include <functional>
#include <cctype>
using namespace std;

class Solution {
public:
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
     * diffWaysToCompute("2-1-1") → {0, 2}
     * diffWaysToCompute("2*3-4*5") → {-34, -14, -10, -10, 10}
     */
    vector<int> diffWaysToCompute(string expression) {
        unordered_map<string, vector<int>> memo;
        return compute(expression, memo);
    }
    
private:
    vector<int> compute(const string& expr, unordered_map<string, vector<int>>& memo) {
        // Проверяем, есть ли результат в кэше
        if (memo.find(expr) != memo.end()) {
            return memo[expr];
        }
        
        vector<int> results;
        
        // Проверяем, является ли выражение числом
        bool isNumber = true;
        for (char c : expr) {
            if (!isdigit(c)) {
                isNumber = false;
                break;
            }
        }
        
        if (isNumber) {
            results.push_back(stoi(expr));
            memo[expr] = results;
            return results;
        }
        
        for (int i = 0; i < expr.length(); i++) {
            char c = expr[i];
            
            // Если текущий символ - оператор
            if (c == '+' || c == '-' || c == '*') {
                // Разделяем выражение на левую и правую части
                string leftExpr = expr.substr(0, i);
                string rightExpr = expr.substr(i + 1);
                
                vector<int> leftResults = compute(leftExpr, memo);
                vector<int> rightResults = compute(rightExpr, memo);
                
                // Комбинируем результаты
                for (int left : leftResults) {
                    for (int right : rightResults) {
                        if (c == '+') {
                            results.push_back(left + right);
                        } else if (c == '-') {
                            results.push_back(left - right);
                        } else if (c == '*') {
                            results.push_back(left * right);
                        }
                    }
                }
            }
        }
        
        memo[expr] = results;
        return results;
    }
    
public:
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
    vector<int> diffWaysToComputeDP(string expression) {
        if (expression.empty()) {
            return {};
        }
        
        // Разделяем выражение на числа и операторы
        vector<int> nums;
        vector<char> ops;
        int num = 0;
        
        for (char c : expression) {
            if (isdigit(c)) {
                num = num * 10 + (c - '0');
            } else {
                nums.push_back(num);
                ops.push_back(c);
                num = 0;
            }
        }
        nums.push_back(num);
        
        int n = nums.size();
        
        // Инициализируем таблицу DP
        vector<vector<vector<int>>> dp(n, vector<vector<int>>(n));
        
        // Заполняем диагональ (выражения из одного числа)
        for (int i = 0; i < n; i++) {
            dp[i][i].push_back(nums[i]);
        }
        
        // Заполняем таблицу для подвыражений разной длины
        for (int length = 2; length <= n; length++) {
            for (int i = 0; i <= n - length; i++) {
                int j = i + length - 1;
                
                // Перебираем все возможные позиции операторов
                for (int k = i; k < j; k++) {
                    vector<int> leftResults = dp[i][k];
                    vector<int> rightResults = dp[k+1][j];
                    char op = ops[k];
                    
                    // Комбинируем результаты
                    for (int left : leftResults) {
                        for (int right : rightResults) {
                            if (op == '+') {
                                dp[i][j].push_back(left + right);
                            } else if (op == '-') {
                                dp[i][j].push_back(left - right);
                            } else if (op == '*') {
                                dp[i][j].push_back(left * right);
                            }
                        }
                    }
                }
            }
        }
        
        return dp[0][n-1];
    }
};