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
 * Вычисляет выражение в обратной польской записи.
 * 
 * @param {string[]} tokens - Массив строк, представляющих токены выражения
 * @return {number} Результат вычисления выражения
 * 
 * Алгоритм:
 * 1. Используется массив как стек для хранения операндов.
 * 2. Каждый токен обрабатывается:
 *    - Если токен является числом, он преобразуется в число и помещается в стек.
 *    - Если токен является оператором, из стека извлекаются два операнда,
 *      выполняется операция и результат помещается обратно в стек.
 * 3. После обработки всех токенов в стеке остается один элемент - результат.
 * 
 * Примечание: Для деления используется Math.trunc() для округления к нулю.
 */
var evalRPN = function(tokens) {
    const stack = [];
    
    for (const token of tokens) {
        // Проверяем, является ли токен оператором
        if (token !== "+" && token !== "-" && token !== "*" && token !== "/") {
            // Токен - число, добавляем в стек
            stack.push(parseInt(token));
        } else {
            // Токен - оператор, извлекаем два операнда
            const b = stack.pop();
            const a = stack.pop();
            
            // Выполняем соответствующую операцию
            switch (token) {
                case "+":
                    stack.push(a + b);
                    break;
                case "-":
                    stack.push(a - b);
                    break;
                case "*":
                    stack.push(a * b);
                    break;
                case "/":
                    // Math.trunc() округляет к нулю (отбрасывает дробную часть)
                    stack.push(Math.trunc(a / b));
                    break;
            }
        }
    }
    
    return stack.pop();
};