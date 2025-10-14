/**
 * https://leetcode.com/problems/maximum-total-damage-with-spell-casting/?envType=daily-question&envId=2025-10-11
 */

/**
 * Решает задачу "Maximum Total Damage With Spell Casting".
 * --------------------------------------------------------
 * Идея:
 * - Считаем количество заклинаний каждого значения урона.
 * - Сортируем уникальные значения.
 * - Для каждого d решаем: брать (d * count[d]) или пропустить.
 * - Если берём, переходим к первому значению > d + 2.
 */
var maximumTotalDamage = function(power) {
    const cnt = new Map();
    for (const p of power) cnt.set(p, (cnt.get(p) || 0) + 1);
    const uniq = Array.from(cnt.keys()).sort((a, b) => a - b);
    const n = uniq.length;

    const nxt = new Array(n);
    for (let i = 0; i < n; i++) {
        // бинарный поиск (O(log n))
        let lo = i + 1, hi = n;
        while (lo < hi) {
            const mid = (lo + hi) >> 1;
            if (uniq[mid] > uniq[i] + 2) hi = mid;
            else lo = mid + 1;
        }
        nxt[i] = lo;
    }

    const dp = new Array(n + 1).fill(0);
    for (let i = n - 1; i >= 0; i--) {
        const skip = dp[i + 1];
        const take = uniq[i] * cnt.get(uniq[i]) + dp[nxt[i]];
        dp[i] = Math.max(skip, take);
    }
    return dp[0];
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