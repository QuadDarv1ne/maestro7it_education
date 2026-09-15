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
 * Вычисляет зеркальное расстояние числа n.
 * @param {number} n - Исходное целое число.
 * @return {number} - Зеркальное расстояние.
 */
var mirrorDistance = function(n) {
    // 1. Преобразуем число в строку, разбиваем на массив символов,
    //    переворачиваем массив и собираем обратно в строку.
    const reversedStr = n.toString().split('').reverse().join('');
    
    // 2. Преобразуем обратно в число (ведущие нули отбрасываются).
    const reversedN = parseInt(reversedStr, 10);
    
    // 3. Возвращаем абсолютную разницу.
    return Math.abs(n - reversedN);
};