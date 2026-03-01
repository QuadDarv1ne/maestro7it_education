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
 * @param {Function} fn
 * @return {Function}
 */
var once = function(fn) {
    // Переменная-флаг для отслеживания состояния вызова.
    // Она существует в замыкании и доступна только внутри возвращаемой функции.
    let hasBeenCalled = false;
    
    return function(...args) {
        // Если функция еще не вызывалась
        if (!hasBeenCalled) {
            // Помечаем, что вызов произошел
            hasBeenCalled = true;
            // Выполняем исходную функцию и возвращаем результат
            return fn(...args);
        }
        
        // Если функция уже вызывалась, возвращаем undefined
        // (в JS можно просто написать return; но для ясности можно вернуть undefined)
        return undefined;
    };
};

/**
 * let fn = (a,b,c) => (a + b + c)
 * let onceFn = once(fn)
 *
 * onceFn(1,2,3); // 6
 * onceFn(2,3,6); // undefined
 */