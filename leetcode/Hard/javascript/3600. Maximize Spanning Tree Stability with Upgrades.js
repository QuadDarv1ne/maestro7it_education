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
 * @param {number} n
 * @param {number[][]} edges
 * @param {number} k
 * @return {number}
 */
var maxStability = function(n, edges, k) {
    // Собираем все возможные значения стабильности
    const strengthSet = new Set();
    for (const edge of edges) {
        strengthSet.add(edge[2]);
        if (edge[3] === 0) {
            strengthSet.add(edge[2] * 2);
        }
    }
    const strengths = Array.from(strengthSet).sort((a, b) => a - b);
    
    let left = 0, right = strengths.length - 1;
    let ans = -1;
    
    while (left <= right) {
        const mid = left + Math.floor((right - left) / 2);
        const target = strengths[mid];
        
        if (canAchieve(n, edges, k, target)) {
            ans = target;
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }
    
    return ans;
};

class DSU {
    constructor(n) {
        this.parent = Array(n).fill(0).map((_, i) => i);
        this.rank = Array(n).fill(0);
    }
    
    find(x) {
        if (this.parent[x] !== x) {
            this.parent[x] = this.find(this.parent[x]);
        }
        return this.parent[x];
    }
    
    unite(x, y) {
        x = this.find(x);
        y = this.find(y);
        if (x === y) return false;
        
        if (this.rank[x] < this.rank[y]) {
            this.parent[x] = y;
        } else if (this.rank[x] > this.rank[y]) {
            this.parent[y] = x;
        } else {
            this.parent[y] = x;
            this.rank[x]++;
        }
        return true;
    }
    
    isConnected() {
        const root = this.find(0);
        for (let i = 1; i < this.parent.length; i++) {
            if (this.find(i) !== root) return false;
        }
        return true;
    }
}

function canAchieve(n, edges, k, target) {
    const dsu = new DSU(n);
    const optional = [];
    let mandatoryUsed = 0;
    
    // Обрабатываем обязательные рёбра
    for (const edge of edges) {
        const [u, v, s, must] = edge;
        if (must === 1) {
            if (s < target) return false;
            if (dsu.unite(u, v)) {
                mandatoryUsed++;
            }
        } else {
            optional.push([u, v, s]);
        }
    }
    
    // Проверяем, не создали ли обязательные рёбра циклы
    const mandatoryCount = edges.filter(e => e[3] === 1).length;
    if (mandatoryUsed < mandatoryCount) return false;
    
    // Сортируем опциональные рёбра: сначала те, что не требуют улучшения
    optional.sort((a, b) => {
        const aGood = a[2] >= target;
        const bGood = b[2] >= target;
        
        if (aGood && !bGood) return -1;
        if (!aGood && bGood) return 1;
        
        // Если оба в одной категории, сортируем по убыванию прочности
        if (aGood) {
            return b[2] - a[2];
        } else {
            // Для требующих улучшения - по убыванию улучшенной прочности
            const valA = a[2] * 2;
            const valB = b[2] * 2;
            if (valA !== valB) return valB - valA;
            return b[2] - a[2];
        }
    });
    
    let upgradesUsed = 0;
    let totalUsed = mandatoryUsed;
    
    // Добавляем опциональные рёбра
    for (const [u, v, s] of optional) {
        if (totalUsed === n - 1) break;
        
        if (s >= target) {
            if (dsu.unite(u, v)) {
                totalUsed++;
            }
        } else if (upgradesUsed < k && s * 2 >= target) {
            if (dsu.unite(u, v)) {
                upgradesUsed++;
                totalUsed++;
            }
        }
    }
    
    return totalUsed === n - 1 && dsu.isConnected();
}