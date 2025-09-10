/**
 * https://leetcode.com/problems/minimum-number-of-people-to-teach/description/?envType=daily-question&envId=2025-09-10
 */

/**
 * Найти минимальное число людей, которым нужно преподать один язык,
 * чтобы все дружеские пары могли общаться (имели общий язык).
 * Стратегия: выбрать язык, который знают наибольшее число проблемных пользователей.
 */
var minimumTeachings = function(n, languages, friendships) {
    const bad = new Set();
    for (const [u, v] of friendships) {
        const langsU = new Set(languages[u - 1]);
        const can = languages[v - 1].some(l => langsU.has(l));
        if (!can) {
            bad.add(u - 1);
            bad.add(v - 1);
        }
    }
    if (bad.size === 0) return 0;
    const cnt = Array(n + 1).fill(0);
    for (const u of bad) {
        for (const lang of languages[u]) cnt[lang]++;
    }
    const maxKnown = Math.max(...cnt);
    return bad.size - maxKnown;
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