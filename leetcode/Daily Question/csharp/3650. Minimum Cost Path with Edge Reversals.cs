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

using System;
using System.Collections.Generic;

public class Solution {
    /// <summary>
    /// Находит минимальную стоимость пути от узла 0 до узла n-1 
    /// с возможностью разворота рёбер.
    /// </summary>
    /// <param name="n">Количество узлов в графе</param>
    /// <param name="edges">Массив рёбер [u, v, w], где u->v с весом w</param>
    /// <returns>Минимальная стоимость пути или -1, если путь невозможен</returns>
    public int MinCost(int n, int[][] edges) {
        // Создаём граф смежности: {узел, вес}
        List<(int node, int weight)>[] graph = new List<(int, int)>[n];
        for (int i = 0; i < n; i++) {
            graph[i] = new List<(int, int)>();
        }
        
        // Для каждого направленного ребра u -> v с весом w:
        // 1. Добавляем обычное ребро u -> v с весом w
        // 2. Добавляем развёрнутое ребро v -> u с весом 2*w (стоимость разворота)
        foreach (var e in edges) {
            int u = e[0], v = e[1], w = e[2];
            graph[u].Add((v, w));        // Обычное направление
            graph[v].Add((u, w * 2));    // Развёрнутое ребро
        }
        
        // Алгоритм Дейкстры
        const int INF = int.MaxValue / 2;
        int[] dist = new int[n];
        Array.Fill(dist, INF);
        dist[0] = 0;
        
        // Очередь с приоритетом: (расстояние, узел)
        PriorityQueue<(int dist, int node), int> pq = new PriorityQueue<(int, int), int>();
        pq.Enqueue((0, 0), 0);
        
        while (pq.Count > 0) {
            var (d, u) = pq.Dequeue();
            
            // Пропускаем устаревшие записи
            if (d > dist[u]) continue;
            
            // Если достигли конечного узла, возвращаем расстояние
            if (u == n - 1) return d;
            
            // Релаксация рёбер
            foreach (var (v, w) in graph[u]) {
                int newDist = d + w;
                if (newDist < dist[v]) {
                    dist[v] = newDist;
                    pq.Enqueue((newDist, v), newDist);
                }
            }
        }
        
        // Если узел n-1 недостижим
        return -1;
    }
}