/**
 * https://leetcode.com/problems/two-sum/description/
 */

/**
 * Находит индексы двух чисел в массиве, сумма которых равна target.
 *
 * @param {number[]} nums - Массив целых чисел.
 * @param {number} target - Целевое значение суммы.
 * @return {number[]} Массив из двух индексов чисел, сумма которых равна target.
 */
function twoSum(nums, target) {
    const seen = new Map();

    for (let i = 0; i < nums.length; i++) {
        const complement = target - nums[i];
        if (seen.has(complement)) {
            return [seen.get(complement), i];
        }
        seen.set(nums[i], i);
    }

    return [];
}

/**
 * const nums = [2, 7, 11, 15];
 * const target = 9;
 * console.log(twoSum(nums, target)); // Вывод: [0, 1]
 */

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