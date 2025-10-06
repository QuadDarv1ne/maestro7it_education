/*
https://leetcode.com/problems/swim-in-rising-water/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

/**
 * @param {number[][]} grid
 * @return {number}
 */
var swimInWater = function(grid) {
    const n = grid.length;
    const seen = Array.from({ length: n }, () => Array(n).fill(false));
    const dirs = [[1,0],[-1,0],[0,1],[0,-1]];

    // Реализуем min-heap через класс
    class MinHeap {
        constructor() { this.data = []; }
        push(val) {
            this.data.push(val);
            this._up(this.data.length - 1);
        }
        pop() {
            if (this.data.length === 1) return this.data.pop();
            const res = this.data[0];
            this.data[0] = this.data.pop();
            this._down(0);
            return res;
        }
        _up(i) {
            while (i > 0) {
                let p = (i - 1) >> 1;
                if (this.data[p][0] <= this.data[i][0]) break;
                [this.data[p], this.data[i]] = [this.data[i], this.data[p]];
                i = p;
            }
        }
        _down(i) {
            let n = this.data.length;
            while (true) {
                let l = i * 2 + 1, r = i * 2 + 2, s = i;
                if (l < n && this.data[l][0] < this.data[s][0]) s = l;
                if (r < n && this.data[r][0] < this.data[s][0]) s = r;
                if (s === i) break;
                [this.data[s], this.data[i]] = [this.data[i], this.data[s]];
                i = s;
            }
        }
        get size() { return this.data.length; }
    }

    const heap = new MinHeap();
    heap.push([grid[0][0], 0, 0]);
    seen[0][0] = true;
    let res = 0;

    while (heap.size) {
        const [time, x, y] = heap.pop();
        res = Math.max(res, time);
        if (x === n - 1 && y === n - 1) {
            return res;
        }
        for (const [dx, dy] of dirs) {
            const nx = x + dx, ny = y + dy;
            if (nx < 0 || nx >= n || ny < 0 || ny >= n) continue;
            if (seen[nx][ny]) continue;
            seen[nx][ny] = true;
            const nt = Math.max(time, grid[nx][ny]);
            heap.push([nt, nx, ny]);
        }
    }
    return -1;
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