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
 * @param {Array} args
 * @param {number} t
 * @return {Function}
 */
var cancellable = function(fn, args, t) {
    // 1. Планируем вызов функции через t миллисекунд.
    // setTimeout возвращает уникальный идентификатор таймера.
    const timerId = setTimeout(() => {
        fn(...args);
    }, t);

    // 2. Возвращаем функцию отмены.
    // Эта функция замыкает в себе переменную timerId.
    return function() {
        // clearTimeout отменяет запланированный вызов, если он еще не произошел.
        clearTimeout(timerId);
    };
};