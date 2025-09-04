/**
 * https://leetcode.com/problems/find-closest-person/description/?envType=daily-question&envId=2025-09-04
 */

/**
 * Определяет, кто из двух людей ближе к цели.
 *
 * @param {number} x - позиция первого человека
 * @param {number} y - позиция второго человека
 * @param {number} z - позиция цели
 * @return {number} 1, если первый ближе;
 *                  2, если второй ближе;
 *                  0, если оба на одинаковом расстоянии
 */
var findClosest = function(x, y, z) {
    const a = Math.abs(x - z);
    const b = Math.abs(y - z);
    return a === b ? 0 : (a < b ? 1 : 2);
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