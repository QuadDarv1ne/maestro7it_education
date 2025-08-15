/**
 * https://leetcode.com/problems/sliding-window-maximum/description/
 */

/**
 * Возвращает массив максимумов для каждого окна размера k.
 * Используется массив как deque индексов.
 */
var maxSlidingWindow = function(nums, k) {
    const q = [];  // хранит индексы, в порядке убывания по значению
    const ans = [];
    for (let i = 0; i < nums.length; i++) {
        // Удаляем индексы вне окна
        if (q.length && q[0] < i - k + 1) q.shift();
        // Удаляем менее значимые элементы с конца
        while (q.length && nums[q[q.length - 1]] <= nums[i]) q.pop();
        q.push(i);
        if (i >= k - 1) ans.push(nums[q[0]]);
    }
    return ans;
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