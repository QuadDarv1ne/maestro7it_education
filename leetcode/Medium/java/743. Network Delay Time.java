/**
 * https://leetcode.com/problems/network-delay-time/description/
 */

import java.util.*;

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
    public int networkDelayTime(int[][] times, int n, int k) {
        Map<Integer, List<int[]>> graph = new HashMap<>();
        for (int[] time : times) {
            graph.computeIfAbsent(time[0], x -> new ArrayList<>()).add(new int[]{time[1], time[2]});
        }

        int[] dist = new int[n + 1];
        Arrays.fill(dist, Integer.MAX_VALUE);
        dist[k] = 0;

        PriorityQueue<int[]> pq = new PriorityQueue<>(Comparator.comparingInt(a -> a[0]));
        pq.offer(new int[]{0, k});

        while (!pq.isEmpty()) {
            int[] curr = pq.poll();
            int d = curr[0], node = curr[1];

            if (d > dist[node]) continue;

            if (graph.containsKey(node)) {
                for (int[] neighbor : graph.get(node)) {
                    int nextNode = neighbor[0], time = neighbor[1];
                    int newDist = d + time;
                    if (newDist < dist[nextNode]) {
                        dist[nextNode] = newDist;
                        pq.offer(new int[]{newDist, nextNode});
                    }
                }
            }
        }

        int maxDist = Arrays.stream(dist, 1, dist.length).max().getAsInt();
        return maxDist == Integer.MAX_VALUE ? -1 : maxDist;
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