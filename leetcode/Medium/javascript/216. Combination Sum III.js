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
 * @param {number} k
 * @param {number} n
 * @return {number[][]}
 */
var combinationSum3 = function(k, n) {
    const result = [];
    
    function backtrack(start, current, remaining) {
        // Если комбинация достигла нужной длины
        if (current.length === k) {
            // Если остаток суммы равен 0 - нашли решение
            if (remaining === 0) {
                result.push([...current]);
            }
            return;
        }
        
        // Раннее отсечение
        const remainingNumbers = k - current.length;
        
        // Проверка минимальной и максимальной возможной суммы
        const minPossible = start * remainingNumbers + 
                           remainingNumbers * (remainingNumbers - 1) / 2;
        const maxPossible = 9 * remainingNumbers - 
                           remainingNumbers * (remainingNumbers - 1) / 2;
        
        if (remaining < minPossible || remaining > maxPossible) {
            return;
        }
        
        // Перебираем возможные числа
        for (let num = start; num <= 9; num++) {
            // Если число слишком большое
            if (num > remaining) break;
            
            current.push(num);
            backtrack(num + 1, current, remaining - num);
            current.pop();
        }
    }
    
    backtrack(1, [], n);
    return result;
};