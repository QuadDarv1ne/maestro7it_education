/**
 * https://leetcode.com/problems/expression-add-operators/description/
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "282. Expression Add Operators"
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
 * Генерирует все комбинации операторов +, -, *, которые дают target.
 * 
 * @param {string} num - Строка цифр (например, "123")
 * @param {number} target - Целевое значение выражения
 * @return {string[]} Массив строк с валидными выражениями
 * 
 * @example
 * // Возвращает ["1+2+3", "1*2*3"]
 * addOperators("123", 6)
 * @example
 * // Возвращает ["2*3+2", "2+3*2"]
 * addOperators("232", 8)
 * 
 * Сложность:
 *   Время: O(4^n) — на каждой позиции 4 варианта
 *   Память: O(n) для рекурсии
 */
var addOperators = function(num, target) {
    const result = [];
    
    function backtrack(index, path, currentVal, prevOperand) {
        if (index === num.length) {
            if (currentVal === target) {
                result.push(path);
            }
            return;
        }
        
        for (let i = index; i < num.length; i++) {
            // Пропускаем числа с ведущим нулем
            if (i > index && num[index] === '0') {
                break;
            }
            
            const currentStr = num.substring(index, i + 1);
            const currentNum = parseInt(currentStr, 10);
            
            if (index === 0) {
                // Первое число
                backtrack(i + 1, currentStr, currentNum, currentNum);
            } else {
                // Сложение
                backtrack(i + 1, `${path}+${currentStr}`, 
                         currentVal + currentNum, currentNum);
                
                // Вычитание
                backtrack(i + 1, `${path}-${currentStr}`, 
                         currentVal - currentNum, -currentNum);
                
                // Умножение: корректируем предыдущую операцию
                backtrack(i + 1, `${path}*${currentStr}`, 
                         currentVal - prevOperand + prevOperand * currentNum, 
                         prevOperand * currentNum);
            }
        }
    }
    
    backtrack(0, '', 0, 0);
    return result;
};