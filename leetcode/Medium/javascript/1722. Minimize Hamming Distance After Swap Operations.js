/**
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

/**
 * @param {number[]} source
 * @param {number[]} target
 * @param {number[][]} allowedSwaps
 * @return {number}
 */
var minimumHammingDistance = function(source, target, allowedSwaps) {
    const n = source.length;
    const parent = Array.from({ length: n }, (_, i) => i);
    const rank = new Array(n).fill(0);

    const find = (x) => {
        if (parent[x] !== x) parent[x] = find(parent[x]);
        return parent[x];
    };

    const union = (x, y) => {
        let rx = find(x), ry = find(y);
        if (rx === ry) return;
        if (rank[rx] < rank[ry]) parent[rx] = ry;
        else if (rank[rx] > rank[ry]) parent[ry] = rx;
        else { parent[ry] = rx; rank[rx]++; }
    };

    for (const [a, b] of allowedSwaps) union(a, b);

    const compCount = new Map();
    for (let i = 0; i < n; i++) {
        const root = find(i);
        if (!compCount.has(root)) compCount.set(root, new Map());
        const cnt = compCount.get(root);
        cnt.set(source[i], (cnt.get(source[i]) || 0) + 1);
    }

    let ans = 0;
    for (let i = 0; i < n; i++) {
        const root = find(i);
        const cnt = compCount.get(root);
        if (cnt.has(target[i]) && cnt.get(target[i]) > 0) {
            cnt.set(target[i], cnt.get(target[i]) - 1);
        } else ans++;
    }
    return ans;
};