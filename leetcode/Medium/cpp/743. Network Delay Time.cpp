/**
 * https://leetcode.com/problems/network-delay-time/description/
 */

#include <vector>
#include <queue>
#include <climits>
#include <algorithm>

using namespace std;

class Solution {
public:
    /**
     * Определяет минимальное время, необходимое для доставки сигнала от узла k ко всем остальным узлам сети.
     * Используется алгоритм Дейкстры для поиска кратчайших путей.
     *
     * @param times Список рёбер сети, где каждый элемент [u, v, w] означает, что сигнал от узла u до узла v передаётся за w единиц времени.
     * @param n Количество узлов в сети.
     * @param k Индекс начального узла (1-based).
     * @return Минимальное время доставки сигнала ко всем узлам сети или -1, если это невозможно.
     */
    int networkDelayTime(vector<vector<int>>& times, int n, int k) {
        vector<vector<pair<int, int>>> graph(n + 1);
        for (const auto& time : times) {
            graph[time[0]].emplace_back(time[1], time[2]);
        }

        vector<int> dist(n + 1, INT_MAX);
        dist[k] = 0;

        priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> pq;
        pq.push({0, k});

        while (!pq.empty()) {
            auto [d, node] = pq.top();
            pq.pop();

            if (d > dist[node]) continue;

            for (const auto& [neighbor, time] : graph[node]) {
                int newDist = d + time;
                if (newDist < dist[neighbor]) {
                    dist[neighbor] = newDist;
                    pq.push({newDist, neighbor});
                }
            }
        }

        int maxDist = *max_element(dist.begin() + 1, dist.end());
        return maxDist == INT_MAX ? -1 : maxDist;
    }
};

/*
''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
*/