/**
 * Решение для Separate Squares II на JavaScript
 * Алгоритм сканирующей прямой с деревом отрезков
 * 
 * Сложность: O(n log n) время, O(n) память.
 * Алгоритм:
 * 1. Сбор уникальных X-координат и создание дерева отрезков
 * 2. Создание и сортировка событий (начало/конец квадратов)
 * 3. Первый проход: вычисление общей площади
 * 4. Второй проход: поиск y, где накопленная площадь = половина
 * 
 * Автор: Дуплей Максим Игоревич
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
class SegmentTree {
    constructor(xs) {
        this.xs = xs;
        this.n = xs.length - 1;
        this.cnt = new Array(4 * this.n).fill(0);
        this.width = new Array(4 * this.n).fill(0);
    }

    _update(idx, l, r, ql, qr, val) {
        if (qr <= this.xs[l] || this.xs[r + 1] <= ql) return;
        
        if (ql <= this.xs[l] && this.xs[r + 1] <= qr) {
            this.cnt[idx] += val;
        } else {
            const mid = Math.floor((l + r) / 2);
            this._update(idx * 2 + 1, l, mid, ql, qr, val);
            this._update(idx * 2 + 2, mid + 1, r, ql, qr, val);
        }
        
        if (this.cnt[idx] > 0) {
            this.width[idx] = this.xs[r + 1] - this.xs[l];
        } else if (l === r) {
            this.width[idx] = 0;
        } else {
            this.width[idx] = this.width[idx * 2 + 1] + this.width[idx * 2 + 2];
        }
    }

    add(l, r, val) {
        if (l < r) this._update(0, 0, this.n - 1, l, r, val);
    }

    getCoveredWidth() {
        return this.width[0];
    }
}

/**
 * @param {number[][]} squares
 * @return {number}
 */
var separateSquares = function(squares) {
    // Создаем события и собираем уникальные X
    const events = [];
    const xsSet = new Set();
    
    for (const [x, y, l] of squares) {
        const xr = x + l;
        events.push([y, 1, x, xr]);
        events.push([y + l, -1, x, xr]);
        xsSet.add(x);
        xsSet.add(xr);
    }
    
    // Сортируем события по y
    events.sort((a, b) => a[0] - b[0]);
    
    // Подготовка массива X
    const xs = Array.from(xsSet).sort((a, b) => a - b);
    
    // Вычисляем общую площадь
    const totalArea = calculateTotalArea(events, xs);
    const halfArea = totalArea / 2.0;
    
    // Поиск разделяющей линии
    const tree = new SegmentTree(xs);
    let accumulated = 0.0;
    let prevY = 0;
    
    for (const [y, delta, xl, xr] of events) {
        const covered = tree.getCoveredWidth();
        if (covered > 0) {
            const areaGain = covered * (y - prevY);
            if (accumulated + areaGain >= halfArea - 1e-12) {
                return prevY + (halfArea - accumulated) / covered;
            }
            accumulated += areaGain;
        }
        
        tree.add(xl, xr, delta);
        prevY = y;
    }
    
    return prevY;
};

function calculateTotalArea(events, xs) {
    const tree = new SegmentTree(xs);
    let total = 0.0;
    let prevY = 0;
    
    for (const [y, delta, xl, xr] of events) {
        total += tree.getCoveredWidth() * (y - prevY);
        tree.add(xl, xr, delta);
        prevY = y;
    }
    
    return total;
}