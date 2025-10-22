/*
Задача: Maximum Frequency of an Element After Performing Operations II  
Источник: https://leetcode.com/problems/maximum-frequency-of-an-element-after-performing-operations-ii/
Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X  
GitHub: https://github.com/QuadDarv1ne/  
*/

function lowerBound(arr, x) {
    let l = 0, r = arr.length;
    while (l < r) {
        const m = (l + r) >> 1;
        if (arr[m] < x) l = m + 1; else r = m;
    }
    return l;
}
function upperBound(arr, x) {
    let l = 0, r = arr.length;
    while (l < r) {
        const m = (l + r) >> 1;
        if (arr[m] <= x) l = m + 1; else r = m;
    }
    return l;
}

function maxFrequency(nums, k, numOperations) {
    if (!nums || nums.length === 0) return 0;
    nums.sort((a,b) => a - b);
    const n = nums.length;

    const freq = new Map();
    for (const x of nums) freq.set(x, (freq.get(x) || 0) + 1);

    let ans = 1;
    const unique = Array.from(freq.keys()).sort((a,b) => a - b);

    // 1) для каждого существующего значения v
    for (const v of unique) {
        const leftVal = v - k;
        const rightVal = v + k;
        const L = lowerBound(nums, leftVal);
        const R = upperBound(nums, rightVal);
        const cover = R - L;
        const candidate = Math.min(cover, freq.get(v) + numOperations);
        if (candidate > ans) ans = candidate;
    }

    // 2) sweep по интервалам [a-k, a+k]
    const events = [];
    for (const a of nums) {
        events.push([a - k, 1]);
        events.push([a + k + 1, -1]);
    }
    events.sort((p,q) => p[0] - q[0] || p[1] - q[1]);

    let cur = 0, maxCover = 0;
    for (const [pos, delta] of events) {
        cur += delta;
        if (cur > maxCover) maxCover = cur;
    }

    const candidate2 = Math.min(maxCover, numOperations);
    ans = Math.max(ans, candidate2);

    return ans;
}

// если нужно экспортировать для Node/LeetCode:
// module.exports = maxFrequency;

/*
Полезные ссылки:
1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
2. Telegram №1 @quadd4rv1n7
3. Telegram №2 @dupley_maxim_1999
4. Rutube канал: https://rutube.ru/channel/4218729/
5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
6. YouTube канал: https://www.youtube.com/@it-coders
7. ВК группа: https://vk.com/science_geeks
8. Официальный сайт школы Maestro7IT: https://school-maestro7it.ru/
*/