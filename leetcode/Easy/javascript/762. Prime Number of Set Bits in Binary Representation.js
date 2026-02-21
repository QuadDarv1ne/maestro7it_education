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
 * @param {number} left
 * @param {number} right
 * @return {number}
 */
var countPrimeSetBits = function(left, right) {
    /**
     * Подсчитывает количество чисел в диапазоне [left, right],
     * у которых количество единиц в двоичном представлении является простым числом.
     *
     * Алгоритм:
     * Перебираем числа от left до right включительно.
     * Для каждого числа подсчитываем количество установленных битов (единиц).
     * Проверяем, является ли это количество простым числом из множества
     * {2, 3, 5, 7, 11, 13, 17, 19} (так как максимальное количество битов <= 19).
     * Если да, увеличиваем счетчик.
     *
     * @param {number} left - Левая граница диапазона (включительно).
     * @param {number} right - Правая граница диапазона (включительно).
     * @return {number} Количество чисел с простым числом установленных битов.
     */
    const primes = new Set([2, 3, 5, 7, 11, 13, 17, 19]);
    let count = 0;
    for (let num = left; num <= right; num++) {
        // Подсчёт единичных битов через преобразование в двоичную строку
        const bits = num.toString(2).split('1').length - 1;
        if (primes.has(bits)) {
            count++;
        }
    }
    return count;
};