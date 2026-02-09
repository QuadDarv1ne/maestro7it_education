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
 * Вычисляет значение арифметического выражения без скобок.
 * 
 * Алгоритм:
 * 1. Использует стек для хранения промежуточных результатов.
 * 2. Операторы * и / обрабатываются немедленно.
 * 3. Операторы + и - откладываются (числа помещаются в стек с соответствующим знаком).
 * 4. В конце суммируются все элементы стека.
 * 
 * Сложность:
 * Время: O(n)
 * Пространство: O(n)
 * 
 * @param {string} s - Строка с арифметическим выражением
 * @return {number} Результат вычисления выражения
 * 
 * @example
 * calculate("3+2*2") // 7
 * calculate(" 3/2 ") // 1
 * calculate(" 3+5 / 2 ") // 5
 */
var calculate = function(s) {
    if (!s || s.length === 0) return 0;
    
    let stack = [];
    let num = 0;
    let sign = '+';  // Текущий оператор перед числом
    let n = s.length;
    
    for (let i = 0; i < n; i++) {
        let ch = s[i];
        
        // Если символ - цифра, собираем число
        if (ch >= '0' && ch <= '9') {
            num = num * 10 + (ch - '0');
        }
        
        // Если символ - оператор или последний символ
        if ((ch < '0' || ch > '9') && ch !== ' ' || i === n - 1) {
            if (sign === '+') {
                stack.push(num);
            } else if (sign === '-') {
                stack.push(-num);
            } else if (sign === '*') {
                stack.push(stack.pop() * num);
            } else if (sign === '/') {
                // Целочисленное деление с округлением к нулю
                let top = stack.pop();
                stack.push(Math.trunc(top / num));
            }
            
            // Сбрасываем число и обновляем оператор
            num = 0;
            sign = ch;
        }
    }
    
    // Суммируем все элементы в стеке
    return stack.reduce((sum, val) => sum + val, 0);
};