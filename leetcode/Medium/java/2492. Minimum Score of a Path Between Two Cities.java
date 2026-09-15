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
     * Находит минимальный вес ребра, которое можно посетить на пути
     * между городами 1 и n.
     * 
     * Поскольку разрешено многократно посещать города и дороги,
     * задача сводится к нахождению минимального ребра во всей
     * компоненте связности, содержащей города 1 и n.
     * 
     * Алгоритм:
     * 1. Строим список смежности графа
     * 2. Запускаем BFS от города 1
     * 3. При обходе отслеживаем минимальный вес ребра
     * 
     * @param n Количество городов (от 1 до n)
     * @param roads Массив дорог [a, b, distance]
     * @return Минимальный вес ребра в компоненте связности
     * 
     * Временная сложность: O(V + E)
     * Пространственная сложность: O(V + E)
     */
    public int minScore(int n, int[][] roads) {
        // Построение графа
        List<List<int[]>> graph = new ArrayList<>();
        for (int i = 0; i <= n; i++) {
            graph.add(new ArrayList<>());
        }
        
        for (int[] road : roads) {
            int a = road[0], b = road[1], dist = road[2];
            graph.get(a).add(new int[]{b, dist});
            graph.get(b).add(new int[]{a, dist});
        }
        
        // BFS
        boolean[] visited = new boolean[n + 1];
        Queue<Integer> queue = new LinkedList<>();
        queue.offer(1);
        visited[1] = true;
        
        int minScore = Integer.MAX_VALUE;
        
        while (!queue.isEmpty()) {
            int city = queue.poll();
            
            for (int[] edge : graph.get(city)) {
                int neighbor = edge[0];
                int dist = edge[1];
                
                minScore = Math.min(minScore, dist);
                
                if (!visited[neighbor]) {
                    visited[neighbor] = true;
                    queue.offer(neighbor);
                }
            }
        }
        
        return minScore;
    }
}