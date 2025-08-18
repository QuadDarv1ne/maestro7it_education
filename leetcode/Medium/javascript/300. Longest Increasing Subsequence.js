/**
 * https://leetcode.com/problems/longest-increasing-subsequence/description/?envType=study-plan-v2&envId=top-interview-150
 */

/**
 * Находит длину самой длинной строго возрастающей подпоследовательности в массиве nums.
 * Использует двоичный поиск для эффективного решения задачи за O(n log n).
 *
 * @param {number[]} nums - массив целых чисел
 * @return {number} длина самой длинной возрастающей подпоследовательности
 */
var lengthOfLIS = function(nums) {
    const tails = [];

    for (let num of nums) {
        // Двоичный поиск позиции для вставки num в массив tails
        let left = 0, right = tails.length;
        while (left < right) {
            const mid = Math.floor((left + right) / 2);
            if (tails[mid] < num) {
                left = mid + 1;
            } else {
                right = mid;
            }
        }

        if (left === tails.length) {
            tails.push(num);
        } else {
            tails[left] = num;
        }
    }

    return tails.length;
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