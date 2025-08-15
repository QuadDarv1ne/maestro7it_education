/**
 * https://leetcode.com/problems/power-of-four/description/?envType=daily-question&envId=2025-08-15
 */

/**
 * Проверяет, является ли число n степенью четырёх.
 * Условия:
 * 1. n > 0
 * 2. (n & (n - 1)) === 0 — только один бит
 * 3. (n & 0x55555555) === n — бит в чётной позиции
 *
 * @param {number} n — исходное целое число
 * @return {boolean} — true, если n == 4^k, иначе false
 */
function isPowerOfFour(n) {
    return n > 0
        && (n & (n - 1)) === 0
        && (n & 0x55555555) === n;
}

/*
''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
*/