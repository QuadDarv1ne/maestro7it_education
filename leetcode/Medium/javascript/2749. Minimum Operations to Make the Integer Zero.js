/**
 * https://leetcode.com/problems/minimum-operations-to-make-the-integer-zero/description/?envType=daily-question&envId=2025-09-05
 */

/**
 * Задача: найти минимальное количество операций, чтобы из num1 получить 0.
 * В каждой операции выбирается i ∈ [0, 60], и выполняется:
 *     num1 = num1 - (2^i + num2).
 *
 * Условие:
 *   - k = количество операций.
 *   - target = num1 - k * num2.
 *   Требуется: popcount(target) <= k <= target.
 *
 * Возвращает:
 *   Минимальное k, если возможно, иначе -1.
 * @param {number} num1
 * @param {number} num2
 * @return {number}
 */
var makeTheIntegerZero = function(num1, num2) {
    const popcount = (x) => x.toString(2).split('0').join('').length;
    for (let k = 0; k <= 60; k++) {
        let target = num1 - k * num2;
        if (target >= 0 && popcount(target) <= k && k <= target) {
            return k;
        }
    }
    return -1;
};

/*
''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
*/