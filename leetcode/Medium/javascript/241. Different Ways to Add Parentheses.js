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
 * @param {string} expression - Строка с арифметическим выражением
 * @return {number[]} Все возможные результаты вычисления выражения
 * 
 * @example
 * diffWaysToCompute("2-1-1") → [0, 2]
 * diffWaysToCompute("2*3-4*5") → [-34, -14, -10, -10, 10]
 */
var diffWaysToCompute = function(expression) {
    const memo = new Map();
    
    const compute = (expr) => {
        // Проверяем, есть ли результат в кэше
        if (memo.has(expr)) {
            return memo.get(expr);
        }
        
        const results = [];
        
        // Проверяем, является ли выражение числом
        if (/^\d+$/.test(expr)) {
            results.push(parseInt(expr, 10));
            memo.set(expr, results);
            return results;
        }
        
        for (let i = 0; i < expr.length; i++) {
            const c = expr[i];
            
            // Если текущий символ - оператор
            if (c === '+' || c === '-' || c === '*') {
                // Разделяем выражение на левую и правую части
                const leftExpr = expr.substring(0, i);
                const rightExpr = expr.substring(i + 1);
                
                const leftResults = compute(leftExpr);
                const rightResults = compute(rightExpr);
                
                // Комбинируем результаты
                for (const left of leftResults) {
                    for (const right of rightResults) {
                        if (c === '+') {
                            results.push(left + right);
                        } else if (c === '-') {
                            results.push(left - right);
                        } else if (c === '*') {
                            results.push(left * right);
                        }
                    }
                }
            }
        }
        
        memo.set(expr, results);
        return results;
    };
    
    return compute(expression);
};

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
var diffWaysToComputeDP = function(expression) {
    if (!expression || expression.length === 0) {
        return [];
    }
    
    // Разделяем выражение на числа и операторы
    const nums = [];
    const ops = [];
    let num = 0;
    
    for (const c of expression) {
        if (c >= '0' && c <= '9') {
            num = num * 10 + (c - '0');
        } else {
            nums.push(num);
            ops.push(c);
            num = 0;
        }
    }
    nums.push(num);
    
    const n = nums.length;
    
    // Инициализируем таблицу DP
    const dp = Array.from({ length: n }, () => Array(n).fill().map(() => []));
    
    // Заполняем диагональ (выражения из одного числа)
    for (let i = 0; i < n; i++) {
        dp[i][i].push(nums[i]);
    }
    
    // Заполняем таблицу для подвыражений разной длины
    for (let length = 2; length <= n; length++) {
        for (let i = 0; i <= n - length; i++) {
            const j = i + length - 1;
            
            // Перебираем все возможные позиции операторов
            for (let k = i; k < j; k++) {
                const leftResults = dp[i][k];
                const rightResults = dp[k + 1][j];
                const op = ops[k];
                
                // Комбинируем результаты
                for (const left of leftResults) {
                    for (const right of rightResults) {
                        if (op === '+') {
                            dp[i][j].push(left + right);
                        } else if (op === '-') {
                            dp[i][j].push(left - right);
                        } else if (op === '*') {
                            dp[i][j].push(left * right);
                        }
                    }
                }
            }
        }
    }
    
    return dp[0][n - 1];
};