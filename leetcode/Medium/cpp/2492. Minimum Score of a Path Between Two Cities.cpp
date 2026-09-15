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

#include <vector>
#include <queue>
#include <algorithm>
#include <climits>

using namespace std;

class Solution {
public:
    /*
     * Находит минимальный вес ребра на пути между городами 1 и n.
     * 
     * Алгоритм использует BFS для обхода всей компоненты связности,
     * содержащей город 1. Поскольку город n гарантированно достижим,
     * минимальное ребро во всей компоненте будет ответом.
     * 
     * @param n Количество городов
     * @param roads Вектор дорог, где roads[i] = [a, b, distance]
     * @return Минимальный вес ребра в компоненте связности
     * 
     * Временная сложность: O(V + E)
     * Пространственная сложность: O(V + E)
     */
    int minScore(int n, vector<vector<int>>& roads) {
        // Построение списка смежности
        vector<vector<pair<int, int>>> graph(n + 1);
        for (const auto& road : roads) {
            int a = road[0], b = road[1], dist = road[2];
            graph[a].emplace_back(b, dist);
            graph[b].emplace_back(a, dist);
        }
        
        // BFS для обхода компоненты связности
        vector<bool> visited(n + 1, false);
        queue<int> q;
        q.push(1);
        visited[1] = true;
        
        int min_score = INT_MAX;
        
        while (!q.empty()) {
            int city = q.front();
            q.pop();
            
            for (const auto& [neighbor, dist] : graph[city]) {
                min_score = min(min_score, dist);
                if (!visited[neighbor]) {
                    visited[neighbor] = true;
                    q.push(neighbor);
                }
            }
        }
        
        return min_score;
    }
};