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
 * @param {string} s
 * @param {number} k
 * @return {number}
 */
var minOperations = function(s, k) {
    const n = s.length;
    let z0 = 0;
    for (let c of s) if (c === '0') z0++;
    if (z0 === 0) return 0;

    const parentEven = new Array(n + 3);
    const parentOdd = new Array(n + 3);
    for (let i = 0; i < n + 3; i++) {
        parentEven[i] = i;
        parentOdd[i] = i;
    }

    function find(parent, x) {
        if (parent[x] !== x) parent[x] = find(parent, parent[x]);
        return parent[x];
    }

    function markVisited(z) {
        if (z % 2 === 0) {
            parentEven[z] = find(parentEven, z + 2);
        } else {
            parentOdd[z] = find(parentOdd, z + 2);
        }
    }

    const queue = [];
    queue.push([z0, 0]);
    markVisited(z0);

    let head = 0;
    while (head < queue.length) {
        const [z, dist] = queue[head++];

        const max_i = Math.min(k, z);
        const min_i = Math.max(0, k - (n - z));
        let low = z + k - 2 * max_i;
        let high = z + k - 2 * min_i;
        if (low > high) continue;

        const targetParity = (z + k) % 2;
        const parent = targetParity === 0 ? parentEven : parentOdd;

        if (low % 2 !== targetParity) low++;
        if (low > high) continue;

        let x = find(parent, low);
        while (x <= high && x <= n) {
            if (x === 0) return dist + 1;
            queue.push([x, dist + 1]);
            parent[x] = find(parent, x + 2);
            x = find(parent, x);
        }
    }
    return -1;
};