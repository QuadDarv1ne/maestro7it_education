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

class Solution {
public:
    /**
     * @brief Вычисляет количество способов назначения весов рёбрам для каждого запроса
     * 
     * @details Задача: дано дерево с n вершинами, пронумерованными от 1 до n.
     * Каждому ребру можно назначить вес 1 или 2. Для каждого запроса [u, v]
     * требуется найти количество способов назначения весов ВСЕМ рёбрам дерева,
     * при которых сумма весов на пути между u и v является чётной.
     * 
     * Математическое обоснование:
     * - Пусть длина пути между u и v равна L (количество рёбер на пути)
     * - Для чётной суммы на пути нужно, чтобы количество рёбер с нечётным весом (1)
     *   на этом пути было чётным
     * - Из L рёбер пути можно выбрать 0, 2, 4, ... рёбер с весом 1
     * - Количество способов = C(L,0) + C(L,2) + C(L,4) + ... = 2^(L-1) при L > 0
     * - Рёбра вне пути могут иметь любой вес (1 или 2), но они не влияют на ответ,
     *   так как для каждого запроса считаются все возможные назначения всех рёбер
     * - При L = 0 (u = v) нет рёбер для назначения, ответ = 0
     * 
     * Алгоритм:
     * 1. Находим количество вершин n (максимальный индекс + 1)
     * 2. Строим список смежности дерева
     * 3. Предвычисляем массив степеней двойки: pow2[i] = 2^i mod (10^9 + 7)
     * 4. Запускаем DFS для нахождения глубин вершин и построения LCA
     * 5. Для каждого запроса находим LCA и вычисляем длину пути
     * 6. Ответ = pow2[pathLen - 1] для pathLen > 0, иначе 0
     * 
     * @param edges Список рёбер дерева, где edges[i] = [ui, vi]
     * @param queries Список запросов, где queries[i] = [ui, vi]
     * @return vector<int> Массив ответов для каждого запроса по модулю 10^9 + 7
     * 
     * @note Временная сложность: O((n + q) * log n), где n - число вершин, q - число запросов
     * @note Пространственная сложность: O(n * log n) для хранения таблицы LCA
     * 
     * @example
     * edges = [[1,2],[1,3],[3,4],[3,5]]
     * queries = [[1,4],[3,4],[2,5]]
     * Результат: [2, 1, 4]
     * Пояснение:
     * - [1,4]: путь длины 2, ответ = 2^(2-1) = 2
     * - [3,4]: путь длины 1, ответ = 2^(1-1) = 1
     * - [2,5]: путь длины 3, ответ = 2^(3-1) = 4
     */
    vector<int> assignEdgeWeights(vector<vector<int>>& edges, vector<vector<int>>& queries) {
        const int MOD = 1e9 + 7;
        
        // Определяем количество вершин как максимальный индекс + 1
        // Индексы могут начинаться с 1 и идти не последовательно
        int n = 0;
        for (const auto& edge : edges) {
            n = max({n, edge[0] + 1, edge[1] + 1});
        }
        for (const auto& query : queries) {
            n = max({n, query[0] + 1, query[1] + 1});
        }
        
        // Если нет вершин, возвращаем нули для всех запросов
        if (n == 0) {
            return vector<int>(queries.size(), 0);
        }
        
        // Построение списка смежности для представления дерева
        vector<vector<int>> graph(n);
        for (const auto& edge : edges) {
            int u = edge[0], v = edge[1];
            graph[u].push_back(v);
            graph[v].push_back(u);
        }
        
        // Предвычисление степеней двойки по модулю MOD
        // pow2[i] = 2^i mod MOD
        vector<int> pow2(n + 1);
        pow2[0] = 1;
        for (int i = 1; i <= n; i++) {
            pow2[i] = (pow2[i-1] * 2LL) % MOD;
        }
        
        // Подготовка данных для LCA (Lowest Common Ancestor)
        // LOG - максимальная степень двойки, необходимая для двоичного подъёма
        int LOG = ceil(log2(n)) + 1;
        
        // up[node][i] - вершина, в которую придём из node, поднявшись на 2^i рёбер вверх
        vector<vector<int>> up(n, vector<int>(LOG));
        
        // depth[node] - глубина вершины (расстояние от корня)
        vector<int> depth(n, 0);
        
        // visited[node] - флаг посещения вершины (для обработки несвязных графов)
        vector<bool> visited(n, false);
        
        /**
         * @brief Рекурсивный обход дерева для вычисления глубин и таблицы LCA
         * 
         * @param node Текущая вершина
         * @param parent Родительская вершина
         */
        function<void(int, int)> dfs = [&](int node, int parent) {
            visited[node] = true;
            up[node][0] = parent;  // На 2^0 = 1 ребро вверх - это родитель
            
            // Заполняем таблицу двоичных подъёмов
            for (int i = 1; i < LOG; i++) {
                up[node][i] = up[up[node][i-1]][i-1];
            }
            
            // Рекурсивно обходим всех непосещённых соседей
            for (int neighbor : graph[node]) {
                if (!visited[neighbor]) {
                    depth[neighbor] = depth[node] + 1;
                    dfs(neighbor, node);
                }
            }
        };
        
        // Запускаем DFS для всех компонент связности
        for (int i = 0; i < n; i++) {
            if (!visited[i]) {
                dfs(i, i);  // Корень компоненты указывает сам на себя
            }
        }
        
        /**
         * @brief Нахождение наименьшего общего предка (LCA) двух вершин
         * 
         * Алгоритм:
         * 1. Выравниваем глубины вершин
         * 2. Поднимаем обе вершины одновременно до LCA
         * 
         * @param u Первая вершина
         * @param v Вторая вершина
         * @return int Наименьший общий предок вершин u и v
         */
        auto lca = [&](int u, int v) {
            // Выравниваем глубины: u должна быть не выше v
            if (depth[u] < depth[v]) swap(u, v);
            
            // Поднимаем u на разницу глубин
            int diff = depth[u] - depth[v];
            for (int i = 0; i < LOG; i++) {
                if (diff & (1 << i)) {
                    u = up[u][i];
                }
            }
            
            // Если вершины совпали, LCA найден
            if (u == v) return u;
            
            // Поднимаем обе вершины одновременно
            for (int i = LOG - 1; i >= 0; i--) {
                if (up[u][i] != up[v][i]) {
                    u = up[u][i];
                    v = up[v][i];
                }
            }
            
            // Родитель u (или v) является LCA
            return up[u][0];
        };
        
        // Обработка запросов
        vector<int> results;
        for (const auto& query : queries) {
            int u = query[0], v = query[1];
            int l = lca(u, v);
            
            // Длина пути = расстояние от u до LCA + расстояние от v до LCA
            int pathLen = depth[u] + depth[v] - 2 * depth[l];
            
            if (pathLen == 0) {
                // Путь нулевой длины - нет рёбер для назначения весов
                results.push_back(0);
            } else {
                // Количество способов = 2^(pathLen-1)
                results.push_back(pow2[pathLen - 1]);
            }
        }
        
        return results;
    }
};