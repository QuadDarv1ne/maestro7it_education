/**
 * https://leetcode.com/problems/compare-version-numbers/description/?envType=daily-question&envId=2025-09-23
 */

/**
 * Сравнение двух версий version1 и version2.
 *
 * Алгоритм:
 * 1. Разбить строки по точке.
 * 2. Сравнивать числа поочередно.
 * 3. Недостающие части считать равными 0.
 * 4. Если все равны, вернуть 0.
 *
 * @param {string} version1 - первая версия
 * @param {string} version2 - вторая версия
 * @return {number} -1 если version1 < version2,
 *                   1 если version1 > version2,
 *                   0 если равны
 */
var compareVersion = function(version1, version2) {
    const parts1 = version1.split('.');
    const parts2 = version2.split('.');
    const maxLen = Math.max(parts1.length, parts2.length);
    for (let i = 0; i < maxLen; i++) {
        const v1 = i < parts1.length ? parseInt(parts1[i], 10) : 0;
        const v2 = i < parts2.length ? parseInt(parts2[i], 10) : 0;
        if (v1 < v2) return -1;
        if (v1 > v2) return 1;
    }
    return 0;
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