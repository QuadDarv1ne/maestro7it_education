/*
https://leetcode.com/problems/trapping-rain-water-ii/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

/**
 * @param {number[][]} heightMap
 * @return {number}
 * 
 * Решение задачи "Trapping Rain Water II" (LeetCode 407).
 * 
 * Идея:
 * - Используем min-heap для обхода клеток по возрастанию высоты.
 * - Начинаем с внешних границ, постепенно "затягиваем" внутрь.
 * - Если сосед ниже текущего уровня, добавляем воду.
 * - visited реализован через замену на -1 прямо в heightMap для оптимизации памяти.
 */
var trapRainWater = function(heightMap) {
    const m = heightMap.length;
    if (!m) return 0;
    const n = heightMap[0].length;
    if (m < 3 || n < 3) return 0;

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
                let p = (i-1) >> 1;
                if (this.data[p][0] <= this.data[i][0]) break;
                [this.data[p], this.data[i]] = [this.data[i], this.data[p]];
                i = p;
            }
        }
        _down(i) {
            let n = this.data.length;
            while (true) {
                let l = i*2+1, r = i*2+2, s = i;
                if (l<n && this.data[l][0] < this.data[s][0]) s=l;
                if (r<n && this.data[r][0] < this.data[s][0]) s=r;
                if (s===i) break;
                [this.data[s], this.data[i]] = [this.data[i], this.data[s]];
                i=s;
            }
        }
        get size() { return this.data.length; }
    }

    const heap = new MinHeap();
    for (let i=0;i<m;i++){
        heap.push([heightMap[i][0], i, 0]);
        heap.push([heightMap[i][n-1], i, n-1]);
        heightMap[i][0] = -1;
        heightMap[i][n-1] = -1;
    }
    for (let j=1;j<n-1;j++){
        heap.push([heightMap[0][j], 0, j]);
        heap.push([heightMap[m-1][j], m-1, j]);
        heightMap[0][j] = -1;
        heightMap[m-1][j] = -1;
    }

    let water = 0;
    const dirs = [[1,0],[-1,0],[0,1],[0,-1]];

    while (heap.size){
        const [h,x,y] = heap.pop();
        for (let [dx,dy] of dirs){
            let nx = x + dx, ny = y + dy;
            if (nx<0 || nx>=m || ny<0 || ny>=n || heightMap[nx][ny]===-1) continue;
            let nh = heightMap[nx][ny];
            if (nh < h) water += h - nh;
            heap.push([Math.max(h, nh), nx, ny]);
            heightMap[nx][ny] = -1;
        }
    }

    return water;
};

/* Полезные ссылки:
 * 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07 
 * 2. Telegram №1 @quadd4rv1n7 
 * 3. Telegram №2 @dupley_maxim_1999 
 * 4. Rutube канал: https://rutube.ru/channel/4218729/
 * 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
 * 6. YouTube канал: https://www.youtube.com/@it-coders
 * 7. ВК группа: https://vk.com/science_geeks
 */
