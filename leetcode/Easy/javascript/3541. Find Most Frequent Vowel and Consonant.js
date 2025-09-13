/**
 * https://leetcode.com/problems/find-most-frequent-vowel-and-consonant/description/?envType=daily-question&envId=2025-09-13
 */

/**
 * Задача: вернуть сумму максимальной частоты гласной и максимальной
 * частоты согласной в строке s.
 *
 * Уточнения:
 * - Рассматриваются буквы 'a'..'z' (LeetCode даёт нижний регистр).
 * - Гласные: a, e, i, o, u.
 * - Если гласных/согласных нет — вклад равен 0.
 *
 * Сложность: O(n) по времени, O(1) по памяти.
 * @param {string} s
 * @return {number}
 */
var maxFreqSum = function(s) {
    const cnt = new Array(26).fill(0);
    for (const ch of s) {
        if (ch >= 'a' && ch <= 'z') cnt[ch.charCodeAt(0) - 97]++;
        else {
            const c = ch.toLowerCase();
            if (c >= 'a' && c <= 'z') cnt[c.charCodeAt(0) - 97]++;
        }
    }
    const vowels = 'aeiou';
    let maxV = 0, maxC = 0;
    for (const v of vowels) maxV = Math.max(maxV, cnt[v.charCodeAt(0) - 97]);
    for (let i = 0; i < 26; ++i) {
        const ch = String.fromCharCode(97 + i);
        if (vowels.includes(ch)) continue;
        maxC = Math.max(maxC, cnt[i]);
    }
    return maxV + maxC;
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