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

// Java
class Solution {
    /*
     * Обрабатывает запросы обслуживания энергосети.
     * Используется Union-Find для группировки станций и min-heap для поиска минимальной онлайн станции.
     * 
     * Сложность по времени: O((c + n + q) * α(c))
     * Сложность по памяти: O(c)
     */
    int[] parent;
    
    // Функция поиска корня с path compression
    int find(int x) {
        return parent[x] == x ? x : (parent[x] = find(parent[x]));
    }
    
    // Объединение двух компонент
    void unite(int x, int y) {
        parent[find(x)] = find(y);
    }
    
    public int[] processQueries(int c, int[][] connections, int[][] queries) {
        parent = new int[c + 1];
        for (int i = 0; i <= c; i++) parent[i] = i;
        
        // Строим граф связей
        for (int[] conn : connections) {
            unite(conn[0], conn[1]);
        }
        
        // Создаем min-heap для каждой компоненты
        Map<Integer, PriorityQueue<Integer>> comp = new HashMap<>();
        for (int i = 1; i <= c; i++) {
            int root = find(i);
            comp.putIfAbsent(root, new PriorityQueue<>());
            comp.get(root).offer(i);
        }
        
        boolean[] offline = new boolean[c + 1];
        List<Integer> result = new ArrayList<>();
        
        // Обрабатываем запросы
        for (int[] q : queries) {
            if (q[0] == 2) {
                // Запрос типа 2: станция переходит в оффлайн
                offline[q[1]] = true;
            } else {
                // Запрос типа 1: поиск онлайн станции для обслуживания
                int x = q[1];
                if (!offline[x]) {
                    result.add(x);
                } else {
                    int root = find(x);
                    PriorityQueue<Integer> pq = comp.get(root);
                    
                    // Lazy deletion: удаляем оффлайн станции из heap
                    while (!pq.isEmpty() && offline[pq.peek()]) {
                        pq.poll();
                    }
                    
                    result.add(pq.isEmpty() ? -1 : pq.peek());
                }
            }
        }
        
        return result.stream().mapToInt(i -> i).toArray();
    }
}
