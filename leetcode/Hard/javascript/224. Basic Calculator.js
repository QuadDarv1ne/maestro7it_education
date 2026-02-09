/**
 * https://leetcode.com/problems/basic-calculator/description/
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "224. Basic Calculator"
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
 * Вычисляет значение арифметического выражения.
 * 
 * Алгоритм:
 * - Использует стек для хранения знаков операций при вложенных скобках.
 * - Обрабатывает символы по одному, собирая числа и применяя знаки.
 * 
 * Сложность:
 * Время: O(n)
 * Пространство: O(n)
 * 
 * @param {string} s - Строка с арифметическим выражением
 * @return {number} Результат вычисления выражения
 * 
 * @example
 * calculate("1 + 1") // 2
 * calculate(" 2-1 + 2 ") // 3
 * calculate("(1+(4+5+2)-3)+(6+8)") // 23
 */
var calculate = function(s) {
    let stack = [1]; // Инициализируем стек со знаком '+'
    let sign = 1; // Текущий знак
    let result = 0;
    let n = s.length;
    let i = 0;
    
    while (i < n) {
        let ch = s[i];
        if (ch >= '0' && ch <= '9') {
            // Считываем все цифры числа
            let num = 0;
            while (i < n && s[i] >= '0' && s[i] <= '9') {
                num = num * 10 + (s[i] - '0');
                i++;
            }
            // Добавляем число с текущим знаком
            result += sign * num;
            continue; // Уже увеличили i, пропускаем инкремент в конце
        } else if (ch === '+') {
            sign = stack[stack.length - 1];
        } else if (ch === '-') {
            sign = -stack[stack.length - 1];
        } else if (ch === '(') {
            // Сохраняем текущий знак в стек
            stack.push(sign);
        } else if (ch === ')') {
            // Извлекаем знак из стека
            stack.pop();
        }
        // Пробелы пропускаем
        i++;
    }
    
    return result;
};