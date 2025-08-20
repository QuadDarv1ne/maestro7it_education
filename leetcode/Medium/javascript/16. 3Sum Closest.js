/**
 * https://leetcode.com/problems/3sum-closest/description/
 */
/**
 * Возвращает сумму трёх чисел из nums, ближайшую к target.
 *
 * Подход: сортировка + два указателя.
 * Время: O(n^2), Доп. память: O(1).
 *
 * @param {number[]} nums
 * @param {number} target
 * @return {number}
 */
var threeSumClosest = function(nums, target) {
    nums.sort((a, b) => a - b);
    let n = nums.length;
    let closest_sum = nums[0] + nums[1] + nums[2];

    for (let i = 0; i < n - 2; i++) {
        let l = i + 1;
        let r = n - 1;
        while (l < r) {
            let sum = nums[i] + nums[l] + nums[r];
            if (sum === target) return sum;
            if (Math.abs(sum - target) < Math.abs(closest_sum - target)) {
                closest_sum = sum;
            }
            if (sum < target) {
                l++;
            } else {
                r--;
            }
        }
    }
    return closest_sum;
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