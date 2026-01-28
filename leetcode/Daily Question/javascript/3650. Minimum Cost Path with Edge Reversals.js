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
 * Находит минимальную стоимость пути от узла 0 до узла n-1 
 * с возможностью разворота рёбер.
 * 
 * @param {number} n - Количество узлов в графе
 * @param {number[][]} edges - Массив рёбер [u, v, w], где u->v с весом w
 * @return {number} Минимальная стоимость пути или -1, если путь невозможен
 */
var minCost = function(n, edges) {
    // Создаём граф смежности: массив списков {узел, вес}
    const graph = Array.from({ length: n }, () => []);
    
    // Для каждого направленного ребра u -> v с весом w:
    // 1. Добавляем обычное ребро u -> v с весом w
    // 2. Добавляем развёрнутое ребро v -> u с весом 2*w (стоимость разворота)
    for (const [u, v, w] of edges) {
        graph[u].push([v, w]);        // Обычное направление
        graph[v].push([u, w * 2]);    // Развёрнутое ребро
    }
    
    // Алгоритм Дейкстры
    const INF = Number.MAX_SAFE_INTEGER;
    const dist = Array(n).fill(INF);
    dist[0] = 0;
    
    // Очередь с приоритетом (мин-куча): [расстояние, узел]
    class MinHeap {
        constructor() {
            this.heap = [];
        }
        
        push(item) {
            this.heap.push(item);
            this.bubbleUp(this.heap.length - 1);
        }
        
        pop() {
            if (this.heap.length === 1) return this.heap.pop();
            const top = this.heap[0];
            this.heap[0] = this.heap.pop();
            this.bubbleDown(0);
            return top;
        }
        
        bubbleUp(idx) {
            while (idx > 0) {
                const parent = Math.floor((idx - 1) / 2);
                if (this.heap[idx][0] >= this.heap[parent][0]) break;
                [this.heap[idx], this.heap[parent]] = [this.heap[parent], this.heap[idx]];
                idx = parent;
            }
        }
        
        bubbleDown(idx) {
            while (true) {
                let smallest = idx;
                const left = 2 * idx + 1;
                const right = 2 * idx + 2;
                
                if (left < this.heap.length && this.heap[left][0] < this.heap[smallest][0]) {
                    smallest = left;
                }
                if (right < this.heap.length && this.heap[right][0] < this.heap[smallest][0]) {
                    smallest = right;
                }
                if (smallest === idx) break;
                
                [this.heap[idx], this.heap[smallest]] = [this.heap[smallest], this.heap[idx]];
                idx = smallest;
            }
        }
        
        isEmpty() {
            return this.heap.length === 0;
        }
    }
    
    const pq = new MinHeap();
    pq.push([0, 0]);
    
    while (!pq.isEmpty()) {
        const [d, u] = pq.pop();
        
        // Пропускаем устаревшие записи
        if (d > dist[u]) continue;
        
        // Если достигли конечного узла, возвращаем расстояние
        if (u === n - 1) return d;
        
        // Релаксация рёбер
        for (const [v, w] of graph[u]) {
            const newDist = d + w;
            if (newDist < dist[v]) {
                dist[v] = newDist;
                pq.push([newDist, v]);
            }
        }
    }
    
    // Если узел n-1 недостижим
    return -1;
};