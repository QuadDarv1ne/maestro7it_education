/**
 * https://leetcode.com/problems/maximum-number-of-k-divisible-components/description/?envType=daily-question&envId=2025-11-28
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "Maximum Number of K-Divisible Components" на JavaScript
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

var maxKDivisibleComponents = function(n, edges, values, k) {
    // Строим граф
    const graph = Array.from({length: n}, () => []);
    for (const [u, v] of edges) {
        graph[u].push(v);
        graph[v].push(u);
    }
    
    let components = 0;
    
    const dfs = (node, parent) => {
        let total = values[node];
        
        for (const neighbor of graph[node]) {
            if (neighbor !== parent) {
                total += dfs(neighbor, node);
            }
        }
        
        if (total % k === 0) {
            components++;
        }
        
        return total;
    };
    
    dfs(0, -1);
    return components;
};