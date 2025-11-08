/*
https://leetcode.com/problems/power-grid-maintenance/description/?envType=daily-question&envId=2025-11-06
Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X  
GitHub: https://github.com/QuadDarv1ne/  
*/

/**
 * @param {number} n
 * @param {number[][]} edges
 * @param {number} threshold
 * @return {number}
 */
var minCost = function(n, edges, threshold) {
    // Инициализация Union-Find
    const parent = Array.from({length: n}, (_, i) => i);
    const rank = Array(n).fill(0);
    
    // Поиск корня с path compression
    const find = (x) => {
        if (parent[x] !== x) {
            parent[x] = find(parent[x]);
        }
        return parent[x];
    };
    
    // Объединение двух компонент с union by rank
    const union = (x, y) => {
        const px = find(x), py = find(y);
        if (px === py) return false;
        
        if (rank[px] < rank[py]) {
            parent[px] = py;
        } else if (rank[px] > rank[py]) {
            parent[py] = px;
        } else {
            parent[py] = px;
            rank[px]++;
        }
        return true;
    };
    
    // Сортируем рёбра по весу (алгоритм Крускала)
    edges.sort((a, b) => a[2] - b[2]);
    
    let totalCost = 0;
    let edgesUsed = 0;
    
    // Добавляем рёбра с минимальным весом
    for (const [u, v, cost] of edges) {
        if (cost > threshold) break;
        
        if (union(u, v)) {
            totalCost += cost;
            edgesUsed++;
            
            // MST содержит n-1 ребро
            if (edgesUsed === n - 1) break;
        }
    }
    
    // Проверяем связность графа
    const components = new Set();
    for (let i = 0; i < n; i++) {
        components.add(find(i));
    }
    
    return (components.size > 1) ? -1 : totalCost;
};

/* 
Пошаговый пример для n=5, threshold=10:
edges = [[0,1,2],[1,2,3],[2,3,4],[3,4,5],[0,4,15]]

1. Сортируем: [0,1,2], [1,2,3], [2,3,4], [3,4,5], [0,4,15]
2. Добавляем [0,1,2]: компоненты {0,1}, cost = 2
3. Добавляем [1,2,3]: компоненты {0,1,2}, cost = 5
4. Добавляем [2,3,4]: компоненты {0,1,2,3}, cost = 9
5. Добавляем [3,4,5]: компоненты {0,1,2,3,4}, cost = 14
6. Все узлы связаны, возвращаем 14

Оптимизации Union-Find:
1. Path compression - сжатие пути при поиске корня
2. Union by rank - присоединяем меньшее дерево к большему
3. Итоговая сложность операций: почти O(1) амортизированно
*/

/* Полезные ссылки: */
// 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
// 2. Telegram №1 @quadd4rv1n7
// 3. Telegram №2 @dupley_maxim_1999
// 4. Rutube канал: https://rutube.ru/channel/4218729/
// 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
// 6. YouTube канал: https://www.youtube.com/@it-coders
// 7. ВК группа: https://vk.com/science_geeks