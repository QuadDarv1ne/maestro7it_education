/**
 * https://leetcode.com/problems/house-robber-ii/description/
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Полезные ссылки:
 * 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
 * 2. Telegram №1 @quadd4rv1n7
 * 3. Telegram №2 @dupley_maxim_1999
 * 4. Rutube канал: https://rutube.ru/channel/4218729/
 * 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
 * 6. YouTube канал: https://www.youtube.com/@it-coders
 * 7. ВК группа: https://vk.com/science_geeks
 */

var numberOfSpecialChars = function(word) {
    const lower = new Array(26).fill(false);
    const upper = new Array(26).fill(false);

    for (const c of word) {
        if (c >= 'a' && c <= 'z') {
            lower[c.charCodeAt(0) - 97] = true;
        } else {
            upper[c.charCodeAt(0) - 65] = true;
        }
    }

    let ans = 0;
    for (let i = 0; i < 26; i++) {
        if (lower[i] && upper[i]) {
            ans++;
        }
    }
    return ans;
};