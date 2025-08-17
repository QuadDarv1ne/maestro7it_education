/**
 * https://leetcode.com/problems/subarray-sum-equals-k/description/
 */

/**
 * Задача: найти количество подмассивов, сумма которых равна k.
 *
 * Алгоритм:
 * 1. Используем префиксные суммы.
 * 2. Map хранит количество вхождений каждой суммы.
 * 3. Для каждого элемента проверяем, встречался ли prefixSum - k.
 *
 * Сложность:
 * - Время: O(n)
 * - Память: O(n)
 *
 * @param {number[]} nums - массив чисел
 * @param {number} k - целевое значение суммы
 * @return {number} количество подмассивов
 */
var subarraySum = function(nums, k) {
    let prefixCounts = new Map();
    prefixCounts.set(0, 1);

    let currentSum = 0, count = 0;
    for (let num of nums) {
        currentSum += num;
        if (prefixCounts.has(currentSum - k)) {
            count += prefixCounts.get(currentSum - k);
        }
        prefixCounts.set(currentSum, (prefixCounts.get(currentSum) || 0) + 1);
    }
    return count;
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