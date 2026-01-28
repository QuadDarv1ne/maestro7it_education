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
#include <iostream>
using namespace std;

class Solution {
public:
    /**
     * Находит минимальную стоимость пути от узла 0 до узла n-1 
     * с возможностью разворота рёбер.
     * 
     * @param n Количество узлов в графе
     * @param edges Массив рёбер [u, v, w], где u->v с весом w
     * @return Минимальная стоимость пути или -1, если путь невозможен
     */
    int minCost(int n, vector<vector<int>>& edges) {
        // Создаём граф смежности: {узел, вес}
        vector<vector<pair<int, int>>> graph(n);
        
        // Для каждого направленного ребра u -> v с весом w:
        // 1. Добавляем обычное ребро u -> v с весом w
        // 2. Добавляем развёрнутое ребро v -> u с весом 2*w (стоимость разворота)
        for (auto& e : edges) {
            int u = e[0], v = e[1], w = e[2];
            graph[u].push_back({v, w});      // Обычное направление
            graph[v].push_back({u, w * 2});  // Развёрнутое ребро
        }
        
        // Алгоритм Дейкстры
        const int INF = INT_MAX / 2;
        vector<int> dist(n, INF);
        dist[0] = 0;
        
        // Очередь с приоритетом: {расстояние, узел}
        priority_queue<pair<int, int>, vector<pair<int, int>>, greater<>> pq;
        pq.push({0, 0});
        
        while (!pq.empty()) {
            auto [d, u] = pq.top();
            pq.pop();
            
            // Пропускаем устаревшие записи
            if (d > dist[u]) continue;
            
            // Если достигли конечного узла, возвращаем расстояние
            if (u == n - 1) return d;
            
            // Релаксация рёбер
            for (auto& [v, w] : graph[u]) {
                int newDist = d + w;
                if (newDist < dist[v]) {
                    dist[v] = newDist;
                    pq.push({newDist, v});
                }
            }
        }
        
        // Если узел n-1 недостижим
        return -1;
    }
};