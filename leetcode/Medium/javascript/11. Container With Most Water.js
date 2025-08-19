/**
 * https://leetcode.com/problems/container-with-most-water/description/
 */

/**
 * Находит максимальную площадь контейнера для воды.
 * 
 * height[i] — это высота линии.
 * Нужно выбрать две линии так, чтобы контейнер вмещал максимум воды.
 * 
 * Алгоритм:
 * - Два указателя: left = 0, right = n - 1.
 * - Считаем площадь = (right - left) * Math.min(height[left], height[right]).
 * - Двигаем меньший по высоте указатель.
 * - Сложность: O(n), память: O(1).
 * 
 * @param {number[]} height - массив высот линий
 * @return {number} - максимальная площадь контейнера
 */
var maxArea = function(height) {
    let left = 0, right = height.length - 1;
    let maxArea = 0;
    while (left < right) {
        let area = (right - left) * Math.min(height[left], height[right]);
        maxArea = Math.max(maxArea, area);
        if (height[left] < height[right]) {
            left++;
        } else {
            right--;
        }
    }
    return maxArea;
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