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
 * Находит пропущенное число в диапазоне [0, n] в массиве длины n.
 *
 * @param {number[]} nums - Массив длиной n, содержащий n различных чисел из [0, n]
 * @return {number} Единственное пропущенное число
 *
 * @example
 * // Возвращает 2
 * missingNumber([3, 0, 1])
 * @example
 * // Возвращает 2
 * missingNumber([0, 1])
 * @example
 * // Возвращает 8
 * missingNumber([9,6,4,2,3,5,7,0,1])
 *
 * Сложность:
 *   Время: O(n)
 *   Память: O(1)
 */
var missingNumber = function(nums) {
    const n = nums.length;
    // Способ 1: Формула суммы
    const expectedSum = n * (n + 1) / 2;
    const actualSum = nums.reduce((sum, num) => sum + num, 0);
    return expectedSum - actualSum;
    
    // Способ 2: XOR
    // let result = nums.length;
    // for (let i = 0; i < nums.length; i++) {
    //     result ^= i ^ nums[i];
    // }
    // return result;
};