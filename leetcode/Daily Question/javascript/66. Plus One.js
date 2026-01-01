/**
 * https://leetcode.com/problems/plus-one/description/
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "Plus One"
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
 * Увеличивает большое число, представленное массивом цифр, на единицу.
 * 
 * @param {number[]} digits - массив цифр числа от старшего разряда к младшему
 * @return {number[]} - массив цифр результата увеличения на 1
 */
var plusOne = function(digits) {
    const n = digits.length;
    
    // Идем с конца массива (младшего разряда)
    for (let i = n - 1; i >= 0; i--) {
        if (digits[i] < 9) {
            // Если цифра меньше 9, просто увеличиваем ее
            digits[i]++;
            return digits;
        } else {
            // Если цифра равна 9, устанавливаем 0 и продолжаем перенос
            digits[i] = 0;
        }
    }
    
    // Если дошли сюда, значит все цифры были 9
    // Создаем новый массив с 1 в начале
    const result = new Array(n + 1).fill(0);
    result[0] = 1;
    return result;
};