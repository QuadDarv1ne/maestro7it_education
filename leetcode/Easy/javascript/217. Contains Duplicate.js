/**
 * https://leetcode.com/problems/contains-duplicate/description/
 */

/**
 * Проверяет, содержит ли массив повторяющиеся элементы.
 * Используется Set для отслеживания уже встреченных значений.
 *
 * @param {number[]} nums — массив целых чисел
 * @return {boolean} — true, если обнаружен дубликат; иначе false
 */
var containsDuplicate = function(nums) {
    const seen = new Set();
    for (const num of nums) {
        if (seen.has(num)) {
            return true;
        }
        seen.add(num);
    }
    return false;
};

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