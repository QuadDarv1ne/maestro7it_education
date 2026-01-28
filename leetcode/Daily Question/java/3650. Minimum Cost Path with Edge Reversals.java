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

import java.util.*;

class Solution {
    /**
     * Находит минимальную стоимость пути от узла 0 до узла n-1 
     * с возможностью разворота рёбер.
     * 
     * @param n Количество узлов в графе
     * @param edges Массив рёбер [u, v, w], где u->v с весом w
     * @return Минимальная стоимость пути или -1, если путь невозможен
     */
    public int minCost(int n, int[][] edges) {
        // Создаём граф смежности: список пар {узел, вес}
        List<int[]>[] graph = new ArrayList[n];
        for (int i = 0; i < n; i++) {
            graph[i] = new ArrayList<>();
        }
        
        // Для каждого направленного ребра u -> v с весом w:
        // 1. Добавляем обычное ребро u -> v с весом w
        // 2. Добавляем развёрнутое ребро v -> u с весом 2*w (стоимость разворота)
        for (int[] e : edges) {
            int u = e[0], v = e[1], w = e[2];
            graph[u].add(new int[]{v, w});        // Обычное направление
            graph[v].add(new int[]{u, w * 2});    // Развёрнутое ребро
        }
        
        // Алгоритм Дейкстры
        final int INF = Integer.MAX_VALUE / 2;
        int[] dist = new int[n];
        Arrays.fill(dist, INF);
        dist[0] = 0;
        
        // Очередь с приоритетом: {расстояние, узел}
        PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> Integer.compare(a[0], b[0]));
        pq.offer(new int[]{0, 0});
        
        while (!pq.isEmpty()) {
            int[] curr = pq.poll();
            int d = curr[0], u = curr[1];
            
            // Пропускаем устаревшие записи
            if (d > dist[u]) continue;
            
            // Если достигли конечного узла, возвращаем расстояние
            if (u == n - 1) return d;
            
            // Релаксация рёбер
            for (int[] edge : graph[u]) {
                int v = edge[0], w = edge[1];
                int newDist = d + w;
                if (newDist < dist[v]) {
                    dist[v] = newDist;
                    pq.offer(new int[]{newDist, v});
                }
            }
        }
        
        // Если узел n-1 недостижим
        return -1;
    }
}