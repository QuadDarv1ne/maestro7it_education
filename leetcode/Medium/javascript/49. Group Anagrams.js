/**
 * https://leetcode.com/problems/group-anagrams/description/
 */

/**
 * Группируем строки по частоте букв:
 * - Создаем строковый ключ вида "1#0#...#1"
 */
var groupAnagrams = function(strs) {
    const map = {};
    for (const s of strs) {
        const cnt = Array(26).fill(0);
        for (const c of s) cnt[c.charCodeAt(0) - 97]++;
        const key = cnt.join('#');
        if (!map[key]) map[key] = [];
        map[key].push(s);
    }
    return Object.values(map);
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