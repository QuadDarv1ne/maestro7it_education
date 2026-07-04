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
    /*
     * Находит минимальный вес ребра, доступного на пути между городами 1 и n.
     * 
     * Так как можно посещать города и дороги многократно, задача сводится
     * к поиску минимального ребра в компоненте связности, содержащей оба города.
     * Используется BFS для обхода графа.
     * 
     * @param n Количество городов (нумерация с 1)
     * @param roads Массив дорог [city1, city2, distance]
     * @return Минимальный вес ребра в компоненте связности
     * 
     * Пример:
     * n = 4, roads = [[1,2,9],[2,3,6],[2,4,5],[1,4,7]]
     * Результат: 5 (ребро 2-4)
     */
    public int MinScore(int n, int[][] roads) {
        // Построение графа
        var graph = new List<(int to, int distance)>[n + 1];
        for (int i = 1; i <= n; i++) {
            graph[i] = new List<(int, int)>();
        }
        
        foreach (var road in roads) {
            int a = road[0], b = road[1], dist = road[2];
            graph[a].Add((b, dist));
            graph[b].Add((a, dist));
        }
        
        // BFS обход
        var visited = new bool[n + 1];
        var queue = new Queue<int>();
        queue.Enqueue(1);
        visited[1] = true;
        
        int minScore = int.MaxValue;
        
        while (queue.Count > 0) {
            int city = queue.Dequeue();
            
            foreach (var (neighbor, dist) in graph[city]) {
                minScore = Math.Min(minScore, dist);
                if (!visited[neighbor]) {
                    visited[neighbor] = true;
                    queue.Enqueue(neighbor);
                }
            }
        }
        
        return minScore;
    }
}