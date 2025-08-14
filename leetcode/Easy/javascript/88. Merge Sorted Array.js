/**
 * https://leetcode.com/problems/merge-sorted-array/description/
 */

/**
 * Сливает nums2 в nums1 in-place.
 * nums1 имеет длину m + n, первые m элементов значимы.
 *
 * @param {number[]} nums1
 * @param {number} m
 * @param {number[]} nums2
 * @param {number} n
 * @return {void} Изменяет nums1 на месте.
 */
var merge = function(nums1, m, nums2, n) {
    let write = m + n - 1;
    let i = m - 1;
    let j = n - 1;
    while (j >= 0) {
        if (i >= 0 && nums1[i] > nums2[j]) {
            nums1[write--] = nums1[i--];
        } else {
            nums1[write--] = nums2[j--];
        }
    }
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