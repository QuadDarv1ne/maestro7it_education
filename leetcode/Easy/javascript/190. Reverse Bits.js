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
 * @param {number} n - положительное целое число
 * @return {number} - число с обращенными битами
 * 
 * Обращает биты 32-битного беззнакового целого числа.
 */
var reverseBits = function(n) {
    let result = 0;
    
    for (let i = 0; i < 32; i++) {
        // Сдвигаем результат влево для освобождения места
        result <<= 1;
        
        // Получаем младший бит числа n
        const bit = n & 1;
        
        // Добавляем бит к результату
        result |= bit;
        
        // Сдвигаем n вправо для обработки следующего бита
        // Используем беззнаковый сдвиг для правильной работы
        n >>>= 1;
    }
    
    // Преобразуем результат в беззнаковое 32-битное число
    return result >>> 0;
};