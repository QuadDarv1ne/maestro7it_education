/**
 * https://leetcode.com/problems/largest-perimeter-triangle/description/?envType=daily-question&envId=2025-09-28
 */

/**
 * Находит максимальный периметр треугольника, который можно построить
 * из трёх длин массива nums.
 *
 * Алгоритм:
 * 1. Сортируем массив.
 * 2. Идём от конца (nums[i] — наибольшая сторона).
 * 3. Проверяем условие треугольника для троек (a, b, c).
 * 4. Если условие выполняется — возвращаем периметр.
 * 5. Если ни один треугольник невозможен — возвращаем 0.
 *
 * @param {number[]} nums
 * @return {number}
 */
var largestPerimeter = function(nums) {
    nums.sort((a, b) => a - b);
    let n = nums.length;
    for (let i = n - 1; i >= 2; i--) {
        let a = nums[i - 2], b = nums[i - 1], c = nums[i];
        if (a + b > c) {
            return a + b + c;
        }
    }
    return 0;
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