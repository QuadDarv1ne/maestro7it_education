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

// C++
class Solution {
public:
    /*
     * Обрабатывает запросы обслуживания энергосети.
     * Использует Union-Find для группировки станций и min-heap для поиска минимальной онлайн станции.
     * 
     * Подход: 
     * 1. Строим DSU из connections
     * 2. Для каждой компоненты создаем min-heap онлайн станций
     * 3. Используем lazy deletion при поиске минимальной станции
     * 
     * Сложность по времени: O((c + n + q) * α(c)), где α - обратная функция Аккермана
     * Сложность по памяти: O(c)
     */
    vector<int> processQueries(int c, vector<vector<int>>& connections, vector<vector<int>>& queries) {
        vector<int> parent(c + 1);
        for (int i = 0; i <= c; i++) parent[i] = i;
        
        // Функция поиска корня с path compression
        auto find = [&](int x) -> int {
            function<int(int)> findImpl = [&](int node) -> int {
                return parent[node] == node ? node : parent[node] = findImpl(parent[node]);
            };
            return findImpl(x);
        };
        
        // Объединение двух компонент
        auto unite = [&](int x, int y) {
            parent[find(x)] = find(y);
        };
        
        // Строим граф связей
        for (auto& conn : connections) {
            unite(conn[0], conn[1]);
        }
        
        // Создаем min-heap для каждой компоненты
        unordered_map<int, priority_queue<int, vector<int>, greater<int>>> comp;
        for (int i = 1; i <= c; i++) {
            comp[find(i)].push(i);
        }
        
        vector<bool> offline(c + 1, false);
        vector<int> result;
        
        // Обрабатываем запросы
        for (auto& q : queries) {
            if (q[0] == 2) {
                // Запрос типа 2: станция переходит в оффлайн
                offline[q[1]] = true;
            } else {
                // Запрос типа 1: поиск онлайн станции для обслуживания
                int x = q[1];
                if (!offline[x]) {
                    result.push_back(x);
                } else {
                    int root = find(x);
                    auto& pq = comp[root];
                    
                    // Lazy deletion: удаляем оффлайн станции из heap
                    while (!pq.empty() && offline[pq.top()]) {
                        pq.pop();
                    }
                    
                    result.push_back(pq.empty() ? -1 : pq.top());
                }
            }
        }
        
        return result;
    }
};
