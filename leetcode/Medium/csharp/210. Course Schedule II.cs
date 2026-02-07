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

public class Solution {
    public int[] FindOrder(int numCourses, int[][] prerequisites) {
        // Алгоритм Кана (топологическая сортировка через BFS)
        List<int>[] graph = new List<int>[numCourses];
        int[] inDegree = new int[numCourses];
        
        // Инициализация графа
        for (int i = 0; i < numCourses; i++) {
            graph[i] = new List<int>();
        }
        
        // Строим граф и считаем входящие степени
        foreach (var prereq in prerequisites) {
            int course = prereq[0];
            int pre = prereq[1];
            graph[pre].Add(course);
            inDegree[course]++;
        }
        
        // Очередь для вершин с нулевой входящей степенью
        Queue<int> queue = new Queue<int>();
        for (int i = 0; i < numCourses; i++) {
            if (inDegree[i] == 0) {
                queue.Enqueue(i);
            }
        }
        
        List<int> order = new List<int>();
        
        // Обработка вершин
        while (queue.Count > 0) {
            int node = queue.Dequeue();
            order.Add(node);
            
            foreach (int neighbor in graph[node]) {
                inDegree[neighbor]--;
                if (inDegree[neighbor] == 0) {
                    queue.Enqueue(neighbor);
                }
            }
        }
        
        // Проверяем, прошли ли все курсы
        if (order.Count == numCourses) {
            return order.ToArray();
        }
        return new int[0];
    }
}