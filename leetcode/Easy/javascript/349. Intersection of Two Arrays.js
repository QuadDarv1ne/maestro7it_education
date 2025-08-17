/**
 * https://leetcode.com/problems/intersection-of-two-arrays/description/
 */

/**
 * Функция ищет пересечение двух массивов.
 * Каждый элемент результата уникален.
 *
 * @param {number[]} nums1 - первый массив чисел
 * @param {number[]} nums2 - второй массив чисел
 * @return {number[]} - массив уникальных элементов, встречающихся в обоих массивах
 */
var intersection = function(nums1, nums2) {
    let set1 = new Set(nums1);
    let result = new Set();

    for (let num of nums2) {
        if (set1.has(num)) {
            result.add(num);
        }
    }

    return Array.from(result);
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