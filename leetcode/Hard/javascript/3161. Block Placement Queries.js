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
 * Обрабатывает запросы двух типов в обратном порядке:
 * 1: [1, x] — установить препятствие в точке x.
 * 2: [2, x, sz] — проверить, можно ли разместить блок размера sz на отрезке [0, x].
 * 
 * @param {number[][]} queries
 * @return {boolean[]}
 */
var getResults = function(queries) {
    const n = Math.min(50000, queries.length * 3);
    const tree = new Array(n + 1).fill(0); // Дерево Фенвика
    
    function fenwickMaximize(i, val) {
        while (i <= n) {
            tree[i] = Math.max(tree[i], val);
            i += i & -i;
        }
    }
    
    function fenwickGet(i) {
        let res = 0;
        while (i > 0) {
            res = Math.max(res, tree[i]);
            i -= i & -i;
        }
        return res;
    }
    
    // Собираем все препятствия
    const obstacleSet = new Set([0, n]);
    for (const q of queries) {
        if (q[0] === 1) {
            const x = q[1];
            if (x > 0 && x < n) {
                obstacleSet.add(x);
            }
        }
    }
    
    const obstacles = Array.from(obstacleSet).sort((a, b) => a - b);
    
    // Начальное заполнение дерева
    for (let i = 1; i < obstacles.length; i++) {
        const x1 = obstacles[i - 1];
        const x2 = obstacles[i];
        fenwickMaximize(x2, x2 - x1);
    }
    
    const ans = [];
    
    function lowerBound(arr, target) {
        let lo = 0, hi = arr.length;
        while (lo < hi) {
            const mid = (lo + hi) >>> 1;
            if (arr[mid] < target) lo = mid + 1;
            else hi = mid;
        }
        return lo;
    }
    
    // Обрабатываем запросы с конца
    for (let i = queries.length - 1; i >= 0; i--) {
        if (queries[i][0] === 1) {
            const x = queries[i][1];
            if (x === 0 || x >= n) continue;
            
            const idx = lowerBound(obstacles, x);
            if (idx > 0 && idx < obstacles.length - 1) {
                const leftObstacle = obstacles[idx - 1];
                const rightObstacle = obstacles[idx + 1];
                
                obstacles.splice(idx, 1);
                fenwickMaximize(rightObstacle, rightObstacle - leftObstacle);
            }
        } else {
            const x = queries[i][1];
            const sz = queries[i][2];
            
            let idx = lowerBound(obstacles, x);
            if (idx >= obstacles.length || obstacles[idx] > x) idx--;
            const leftObstacle = obstacles[idx];
            
            ans.push(fenwickGet(leftObstacle) >= sz || x - leftObstacle >= sz);
        }
    }
    
    return ans.reverse();
};