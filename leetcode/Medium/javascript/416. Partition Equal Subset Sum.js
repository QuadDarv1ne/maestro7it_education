/**
 * https://leetcode.com/problems/partition-equal-subset-sum/description/
 */

/**
 * Определяет, можно ли разделить массив nums на два подмножества с одинаковой суммой.
 *
 * @param {number[]} nums — массив чисел
 * @return {boolean} — true, если можно разделить, иначе false
 */
var canPartition = function(nums) {
    const totalSum = nums.reduce((sum, num) => sum + num, 0);
    if (totalSum % 2 !== 0) return false;

    const target = totalSum / 2;
    const dp = new Array(target + 1).fill(false);
    dp[0] = true;

    for (const num of nums) {
        for (let i = target; i >= num; i--) {
            dp[i] = dp[i] || dp[i - num];
        }
    }

    return dp[target];
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