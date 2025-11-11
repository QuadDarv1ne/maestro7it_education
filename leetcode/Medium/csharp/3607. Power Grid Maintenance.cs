/*
https://leetcode.com/problems/power-grid-maintenance/description/?envType=daily-question&envId=2025-11-06
Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X  
GitHub: https://github.com/QuadDarv1ne/  
*/

public class Solution {
    private int[] parent;
    private int[] rank;
    
    public int MinCost(int n, int[][] edges, int threshold) {
        // Инициализация Union-Find
        parent = new int[n];
        rank = new int[n];
        
        for (int i = 0; i < n; i++) {
            parent[i] = i;
        }
        
        // Сортируем рёбра по весу
        Array.Sort(edges, (a, b) => a[2].CompareTo(b[2]));
        
        int totalCost = 0;
        int edgesUsed = 0;
        
        // Алгоритм Крускала
        foreach (var edge in edges) {
            int u = edge[0], v = edge[1], cost = edge[2];
            
            if (cost > threshold) break;
            
            if (Union(u, v)) {
                totalCost += cost;
                edgesUsed++;
                
                if (edgesUsed == n - 1) break;
            }
        }
        
        // Проверяем связность
        int components = 0;
        for (int i = 0; i < n; i++) {
            if (Find(i) == i) components++;
        }
        
        return (components > 1) ? -1 : totalCost;
    }
    
    private int Find(int x) {
        if (parent[x] != x) {
            parent[x] = Find(parent[x]); // Path compression
        }
        return parent[x];
    }
    
    private bool Union(int x, int y) {
        int px = Find(x), py = Find(y);
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
Особенности реализации на C#:
- Используем Array.Sort с лямбда-компаратором
- Метод CompareTo для сравнения целых чисел
- Приватные методы для Find и Union операций

Пример работы:
n = 4, edges = [[0,1,1],[1,2,2],[2,3,3],[0,3,4]], threshold = 5
1. Сортируем: [0,1,1], [1,2,2], [2,3,3], [0,3,4]
2. Добавляем [0,1,1]: cost = 1
3. Добавляем [1,2,2]: cost = 3
4. Добавляем [2,3,3]: cost = 6
5. Результат: 6
*/

/* Полезные ссылки: */
// 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
// 2. Telegram №1 @quadd4rv1n7
// 3. Telegram №2 @dupley_maxim_1999
// 4. Rutube канал: https://rutube.ru/channel/4218729/
// 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
// 6. YouTube канал: https://www.youtube.com/@it-coders
// 7. ВК группа: https://vk.com/science_geeks