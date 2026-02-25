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
 * @param {number[]} arr
 * @return {number[]}
 */
var sortByBits = function(arr) {
    /**
     * Сортирует массив по количеству единичных битов,
     * а затем по значению числа.
     */
    
    // Функция подсчёта единичных битов
    function countBits(n) {
        // Можно также использовать n.toString(2).split('1').length - 1
        let count = 0;
        while (n) {
            count += n & 1;
            n >>= 1;
        }
        return count;
    }

    return arr.sort((a, b) => {
        const bitsA = countBits(a);
        const bitsB = countBits(b);
        if (bitsA === bitsB) return a - b;
        return bitsA - bitsB;
    });
};