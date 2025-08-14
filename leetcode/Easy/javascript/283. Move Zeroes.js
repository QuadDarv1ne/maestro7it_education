/**
 * https://leetcode.com/problems/move-zeroes/description/
 */

/**
 * Перемещает все нули в конец массива, сохраняя порядок ненулевых элементов.
 * 
 * Алгоритм:
 * - Два указателя: i (позиция для следующего ненулевого элемента) и j (текущий индекс)
 * - Если nums[j] != 0, меняем nums[i] и nums[j], увеличиваем i
 *
 * Время: O(n), Память: O(1)
 * 
 * @param {number[]} nums - исходный массив чисел
 */
var moveZeroes = function(nums) {
    let i = 0;
    for (let j = 0; j < nums.length; j++) {
        if (nums[j] !== 0) {
            [nums[i], nums[j]] = [nums[j], nums[i]];
            i++;
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