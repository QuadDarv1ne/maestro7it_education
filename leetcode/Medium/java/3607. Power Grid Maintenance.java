/*
https://leetcode.com/problems/power-grid-maintenance/description/?envType=daily-question&envId=2025-11-06
Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X  
GitHub: https://github.com/QuadDarv1ne/  
*/

class Solution {
    private int[] parent;
    private int[] rank;
    
    public int minCost(int n, int[][] edges, int threshold) {
        // Инициализация Union-Find
        parent = new int[n];
        rank = new int[n];
        
        for (int i = 0; i < n; i++) {
            parent[i] = i;
        }
        
        // Сортируем рёбра по весу (стоимости)
        Arrays.sort(edges, (a, b) -> Integer.compare(a[2], b[2]));
        
        int totalCost = 0;
        int edgesUsed = 0;
        
        // Алгоритм Крускала: добавляем рёбра с минимальным весом
        for (int[] edge : edges) {
            int u = edge[0], v = edge[1], cost = edge[2];
            
            // Если стоимость превышает threshold, прерываем
            if (cost > threshold) break;
            
            // Если ребро соединяет разные компоненты
            if (union(u, v)) {
                totalCost += cost;
                edgesUsed++;
                
                // MST для n узлов содержит n-1 ребро
                if (edgesUsed == n - 1) break;
            }
        }
        
        // Проверяем, что граф связный
        int components = 0;
        for (int i = 0; i < n; i++) {
            if (find(i) == i) components++;
        }
        
        return (components > 1) ? -1 : totalCost;
    }
    
    private int find(int x) {
        if (parent[x] != x) {
            parent[x] = find(parent[x]); // Path compression
        }
        return parent[x];
    }
    
    private boolean union(int x, int y) {
        int px = find(x), py = find(y);
        if (px == py) return false;
        
        // Union by rank
        if (rank[px] < rank[py]) {
            parent[px] = py;
        } else if (rank[px] > rank[py]) {
            parent[py] = px;
        } else {
            parent[py] = px;
            rank[px]++;
        }
        return true;
    }
}

/* 
Теория графов:
MST (Minimum Spanning Tree) - остовное дерево минимального веса
- Содержит все вершины графа
- Не содержит циклов
- Имеет n-1 рёбер для n вершин
- Минимизирует суммарный вес рёбер

Алгоритмы построения MST:
1. Крускала - сортируем рёбра, добавляем жадно (используется здесь)
2. Прима - растим дерево от начальной вершины
3. Борувки - параллельно растим несколько деревьев

Сложность алгоритма Крускала:
- Сортировка: O(E log E)
- Union-Find операции: O(E * α(N)) ≈ O(E)
- Итоговая: O(E log E)
*/

/* Полезные ссылки: */
// 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
// 2. Telegram №1 @quadd4rv1n7
// 3. Telegram №2 @dupley_maxim_1999
// 4. Rutube канал: https://rutube.ru/channel/4218729/
// 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
// 6. YouTube канал: https://www.youtube.com/@it-coders
// 7. ВК группа: https://vk.com/science_geeks