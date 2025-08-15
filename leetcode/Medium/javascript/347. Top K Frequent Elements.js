/**
 * https://leetcode.com/problems/top-k-frequent-elements/
 */

/**
 * Возвращает k наиболее частых элементов.
 */
var topKFrequent = function(nums, k) {
    const cnt = new Map();
    for (const x of nums) cnt.set(x, (cnt.get(x) || 0) + 1);
    const buckets = Array.from({length: nums.length + 1}, () => []);
    for (const [num, f] of cnt) buckets[f].push(num);
    const res = [];
    for (let freq = buckets.length - 1; freq >= 0 && res.length < k; freq--) {
        res.push(...buckets[freq]);
    }
    return res.slice(0, k);
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