/**
 * https://leetcode.com/problems/network-delay-time/description/
 */

using System;
using System.Collections.Generic;

public class Solution {
    /**
     * Определяет минимальное время, необходимое для доставки сигнала от узла k ко всем остальным узлам сети.
     * Используется алгоритм Дейкстры для поиска кратчайших путей.
     *
     * @param times Список рёбер сети, где каждый элемент [u, v, w] означает, что сигнал от узла u до узла v передаётся за w единиц времени.
     * @param n Количество узлов в сети.
     * @param k Индекс начального узла (1-based).
     * @return Минимальное время доставки сигнала ко всем узлам сети или -1, если это невозможно.
     */
    public int NetworkDelayTime(int[][] times, int n, int k) {
        // Построение графа
        var graph = new Dictionary<int, List<Tuple<int, int>>>();
        foreach (var time in times) {
            if (!graph.ContainsKey(time[0])) {
                graph[time[0]] = new List<Tuple<int, int>>();
            }
            graph[time[0]].Add(new Tuple<int, int>(time[1], time[2]));
        }

        // Инициализация расстояний
        var dist = new int[n + 1];
        Array.Fill(dist, int.MaxValue);
        dist[k] = 0;

        // Очередь с приоритетом (SortedSet имитирует min-heap)
        var pq = new SortedSet<Tuple<int, int>>(Comparer<Tuple<int, int>>.Create((a, b) => {
            int cmp = a.Item1.CompareTo(b.Item1);
            return cmp != 0 ? cmp : a.Item2.CompareTo(b.Item2);
        }));
        pq.Add(new Tuple<int, int>(0, k));

        while (pq.Count > 0) {
            var curr = pq.Min;
            pq.Remove(curr);

            int d = curr.Item1;
            int node = curr.Item2;

            if (d > dist[node]) continue;

            if (graph.ContainsKey(node)) {
                foreach (var neighbor in graph[node]) {
                    int nextNode = neighbor.Item1;
                    int time = neighbor.Item2;
                    int newDist = d + time;
                    if (newDist < dist[nextNode]) {
                        dist[nextNode] = newDist;
                        pq.Add(new Tuple<int, int>(newDist, nextNode));
                    }
                }
            }
        }

        int maxDist = int.MinValue;
        for (int i = 1; i <= n; i++) {
            if (dist[i] == int.MaxValue) return -1;
            maxDist = Math.Max(maxDist, dist[i]);
        }

        return maxDist;
    }
}

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