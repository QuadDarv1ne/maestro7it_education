/**
 * https://leetcode.com/problems/3sum/description/
 */

/**
 * Задача: Найти все уникальные тройки чисел в массиве nums,
 * сумма которых равна нулю.
 *
 * Метод:
 * - Сортируем массив
 * - Для каждого i ищем пару через два указателя
 * - Избегаем дубликатов
 *
 * Сложность:
 * Время: O(n^2), Память: O(1)
 */
var threeSum = function(nums) {
    nums.sort((a, b) => a - b);
    const res = [];
    const n = nums.length;

    for (let i = 0; i < n - 2; i++) {
        if (i > 0 && nums[i] === nums[i - 1]) continue;
        if (nums[i] > 0) break;

        let l = i + 1, r = n - 1;
        while (l < r) {
            const s = nums[i] + nums[l] + nums[r];
            if (s < 0) l++;
            else if (s > 0) r--;
            else {
                res.push([nums[i], nums[l], nums[r]]);
                while (l < r && nums[l] === nums[l + 1]) l++;
                while (l < r && nums[r] === nums[r - 1]) r--;
                l++; r--;
            }
        }
    }
    return res;
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