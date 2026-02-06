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
 
// C#
public class Solution {
    /*
     * Обрабатывает запросы обслуживания энергосети.
     * Использует Union-Find для группировки станций и min-heap для поиска минимальной онлайн станции.
     * 
     * Сложность по времени: O((c + n + q) * α(c))
     * Сложность по памяти: O(c)
     */
    public int[] ProcessQueries(int c, int[][] connections, int[][] queries) {
        int[] parent = new int[c + 1];
        for (int i = 0; i <= c; i++) parent[i] = i;
        
        // Функция поиска корня с path compression
        int Find(int x) {
            return parent[x] == x ? x : parent[x] = Find(parent[x]);
        }
        
        // Объединение двух компонент
        void Unite(int x, int y) {
            parent[Find(x)] = Find(y);
        }
        
        // Строим граф связей
        foreach (var conn in connections) {
            Unite(conn[0], conn[1]);
        }
        
        // Создаем min-heap для каждой компоненты
        var comp = new Dictionary<int, PriorityQueue<int, int>>();
        for (int i = 1; i <= c; i++) {
            int root = Find(i);
            if (!comp.ContainsKey(root)) {
                comp[root] = new PriorityQueue<int, int>();
            }
            comp[root].Enqueue(i, i);
        }
        
        bool[] offline = new bool[c + 1];
        var result = new List<int>();
        
        // Обрабатываем запросы
        foreach (var q in queries) {
            if (q[0] == 2) {
                // Запрос типа 2: станция переходит в оффлайн
                offline[q[1]] = true;
            } else {
                // Запрос типа 1: поиск онлайн станции для обслуживания
                int x = q[1];
                if (!offline[x]) {
                    result.Add(x);
                } else {
                    int root = Find(x);
                    var pq = comp[root];
                    
                    // Lazy deletion: удаляем оффлайн станции из heap
                    while (pq.Count > 0 && offline[pq.Peek()]) {
                        pq.Dequeue();
                    }
                    
                    result.Add(pq.Count == 0 ? -1 : pq.Peek());
                }
            }
        }
        
        return result.ToArray();
    }
}
