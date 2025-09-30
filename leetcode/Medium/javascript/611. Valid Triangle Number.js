/**
 * https://leetcode.com/problems/valid-triangle-number/description/?envType=daily-question&envId=2025-09-26
 */

/**
 * @param {number[]} nums
 * @return {number}
 */
var triangleNumber = function(nums) {
    /*
    Возвращает количество троек (i, j, k), которые могут образовать треугольник.
    
    Алгоритм:
    1. Сортировка массива.
    2. Фиксируем наибольшую сторону nums[k].
    3. Два указателя l и r для поиска остальных сторон.
    */
    nums.sort((a, b) => a - b);
    let n = nums.length;
    let ans = 0;
    for (let k = n - 1; k >= 2; k--) {
        let l = 0, r = k - 1;
        while (l < r) {
            if (nums[l] + nums[r] > nums[k]) {
                ans += (r - l);
                r--;
            } else {
                l++;
            }
        }
    }
    return ans;
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