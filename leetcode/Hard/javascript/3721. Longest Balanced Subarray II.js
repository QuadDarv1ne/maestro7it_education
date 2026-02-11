/**
 * https://leetcode.com/problems/longest-balanced-subarray-ii/description/
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "3721. Longest Balanced Subarray II"
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
 * https://leetcode.com/problems/longest-balanced-subarray-ii/description/
 * Решение задачи "3721. Longest Balanced Subarray II"
 *
 * Дерево отрезков с ленивым обновлением.
 * Каждое нечётное число даёт +1, чётное -1.
 * Для индексов левых границ храним текущий баланс [l, i].
 * Словарь last хранит последнюю позицию числа.
 * При добавлении нового вхождения обновляем отрезок [i, n],
 * при удалении старого — отрезок [last[x], n] с противоположным знаком.
 * Запрос: найти самый ранний индекс с балансом, равным текущему now.
 * Длина кандидата = i - pos.
 * Сложность: O(n log n).
 */

class SegmentTree {
    constructor(n) {
        this.n = n;
        // дерево отрезков для индексов левых границ [0..n]
        this.tr = new Array((n + 1) * 4);
        for (let i = 0; i < this.tr.length; i++) {
            this.tr[i] = { l: 0, r: 0, mn: 0, mx: 0, lazy: 0 };
        }
        this.build(1, 0, n);
    }

    build(u, l, r) {
        this.tr[u].l = l;
        this.tr[u].r = r;
        this.tr[u].mn = this.tr[u].mx = 0;
        this.tr[u].lazy = 0;
        if (l === r) return;
        const mid = (l + r) >> 1;
        this.build(u << 1, l, mid);
        this.build((u << 1) | 1, mid + 1, r);
    }

    apply(u, v) {
        this.tr[u].mn += v;
        this.tr[u].mx += v;
        this.tr[u].lazy += v;
    }

    pushDown(u) {
        if (this.tr[u].lazy !== 0) {
            this.apply(u << 1, this.tr[u].lazy);
            this.apply((u << 1) | 1, this.tr[u].lazy);
            this.tr[u].lazy = 0;
        }
    }

    pushUp(u) {
        this.tr[u].mn = Math.min(this.tr[u << 1].mn, this.tr[(u << 1) | 1].mn);
        this.tr[u].mx = Math.max(this.tr[u << 1].mx, this.tr[(u << 1) | 1].mx);
    }

    // добавить v ко всем балансам на отрезке [l, r]
    modify(u, l, r, v) {
        if (this.tr[u].l >= l && this.tr[u].r <= r) {
            this.apply(u, v);
            return;
        }
        this.pushDown(u);
        const mid = (this.tr[u].l + this.tr[u].r) >> 1;
        if (l <= mid) this.modify(u << 1, l, r, v);
        if (r > mid) this.modify((u << 1) | 1, l, r, v);
        this.pushUp(u);
    }

    // найти наименьший индекс pos с балансом == target
    query(u, target) {
        if (this.tr[u].l === this.tr[u].r) return this.tr[u].l;
        this.pushDown(u);
        const lc = u << 1;
        const rc = (u << 1) | 1;
        if (this.tr[lc].mn <= target && target <= this.tr[lc].mx) {
            return this.query(lc, target);
        }
        return this.query(rc, target);
    }
}

/**
 * @param {number[]} nums
 * @return {number}
 */
function longestBalanced(nums) {
    const n = nums.length;
    const st = new SegmentTree(n);
    const last = new Map();

    let now = 0;
    let ans = 0;

    for (let i = 1; i <= n; i++) {
        const x = nums[i - 1];
        const det = (x & 1) ? 1 : -1;   // нечётное: +1, чётное: -1

        if (last.has(x)) {
            st.modify(1, last.get(x), n, -det);
            now -= det;
        }

        last.set(x, i);
        st.modify(1, i, n, det);
        now += det;

        const pos = st.query(1, now);
        ans = Math.max(ans, i - pos);
    }

    return ans;
}