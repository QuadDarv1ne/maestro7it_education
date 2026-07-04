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
 * Находит минимальный вес ребра на пути между городами 1 и n.
 * 
 * Поскольку граф неориентированный и можно проходить по любому пути
 * (включая циклы и повторное посещение вершин), минимальный вес ребра
 * во всей компоненте связности, содержащей города 1 и n, будет ответом.
 * 
 * Используется BFS для обхода всех достижимых вершин из города 1.
 * 
 * @param {number} n - Количество городов (нумерация с 1)
 * @param {number[][]} roads - Массив дорог [a, b, distance]
 * @return {number} Минимальный вес ребра в компоненте связности
 * 
 * @example
 * minScore(4, [[1,2,9],[2,3,6],[2,4,5],[1,4,7]])
 * // Returns: 5
 * 
 * Временная сложность: O(V + E)
 * Пространственная сложность: O(V + E)
 */
var minScore = function(n, roads) {
    // Построение списка смежности
    const graph = Array.from({ length: n + 1 }, () => []);
    
    for (const [a, b, dist] of roads) {
        graph[a].push([b, dist]);
        graph[b].push([a, dist]);
    }
    
    // BFS обход
    const visited = new Array(n + 1).fill(false);
    const queue = [1];
    visited[1] = true;
    
    let minScore = Infinity;
    
    while (queue.length > 0) {
        const city = queue.shift();
        
        for (const [neighbor, dist] of graph[city]) {
            minScore = Math.min(minScore, dist);
            
            if (!visited[neighbor]) {
                visited[neighbor] = true;
                queue.push(neighbor);
            }
        }
    }
    
    return minScore;
};