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
    /// <summary>
    /// Константа модуля для вычислений (10^9 + 7)
    /// </summary>
    private const int MOD = 1_000_000_007;
    
    public int[] AssignEdgeWeights(int[][] edges, int[][] queries) {
        // Шаг 1: Определяем количество вершин как максимальный индекс + 1
        // Индексы могут начинаться с 1 и идти не последовательно
        int n = 0;
        foreach (var edge in edges) {
            n = Math.Max(n, Math.Max(edge[0] + 1, edge[1] + 1));
        }
        foreach (var query in queries) {
            n = Math.Max(n, Math.Max(query[0] + 1, query[1] + 1));
        }
        
        // Если нет вершин, возвращаем массив нулей
        if (n == 0) {
            return new int[queries.Length];
        }
        
        // Шаг 2: Построение списка смежности для представления дерева
        var graph = new List<int>[n];
        for (int i = 0; i < n; i++) {
            graph[i] = new List<int>();
        }
        
        foreach (var edge in edges) {
            int u = edge[0], v = edge[1];
            graph[u].Add(v);
            graph[v].Add(u);
        }
        
        // Шаг 3: Предвычисление степеней двойки по модулю MOD
        // pow2[i] = 2^i mod MOD
        int[] pow2 = new int[n + 1];
        pow2[0] = 1;
        for (int i = 1; i <= n; i++) {
            pow2[i] = (int)((pow2[i-1] * 2L) % MOD);
        }
        
        // Шаг 4: Подготовка данных для LCA (Lowest Common Ancestor)
        // LOG - максимальная степень двойки для двоичного подъёма
        int LOG = (int)Math.Ceiling(Math.Log2(n)) + 1;
        
        // up[node,i] - вершина на 2^i рёбер выше node
        var up = new int[n, LOG];
        
        // depth[node] - глубина вершины (расстояние от корня)
        var depth = new int[n];
        
        // visited[node] - флаг посещения (для обработки несвязных графов)
        var visited = new bool[n];
        
        // Шаг 5: Запускаем DFS для всех компонент связности
        for (int i = 0; i < n; i++) {
            if (!visited[i]) {
                DFS(i, i, graph, up, depth, visited, LOG);
            }
        }
        
        // Шаг 6: Обработка запросов
        int[] results = new int[queries.Length];
        for (int i = 0; i < queries.Length; i++) {
            int u = queries[i][0], v = queries[i][1];
            
            // Находим наименьшего общего предка
            int l = LCA(u, v, up, depth, LOG);
            
            // Вычисляем длину пути между вершинами
            int pathLen = depth[u] + depth[v] - 2 * depth[l];
            
            if (pathLen == 0) {
                // Путь нулевой длины - нет рёбер для назначения весов
                results[i] = 0;
            } else {
                // Количество способов = 2^(pathLen-1)
                results[i] = pow2[pathLen - 1];
            }
        }
        
        return results;
    }
    
    /// <summary>
    /// Рекурсивный обход дерева для вычисления глубин и построения таблицы LCA
    /// </summary>
    /// <param name="node">Текущая вершина</param>
    /// <param name="parent">Родительская вершина</param>
    /// <param name="graph">Список смежности дерева</param>
    /// <param name="up">Таблица двоичных подъёмов для LCA</param>
    /// <param name="depth">Массив глубин вершин</param>
    /// <param name="visited">Массив флагов посещения</param>
    /// <param name="LOG">Максимальная степень двойки</param>
    /// <remarks>
    /// Алгоритм DFS:
    /// <list type="number">
    /// <item>Помечаем вершину как посещённую</item>
    /// <item>Устанавливаем родителя (up[node,0])</item>
    /// <item>Заполняем таблицу двоичных подъёмов:
    ///   up[node,i] = up[up[node,i-1], i-1]</item>
    /// <item>Рекурсивно обходим всех непосещённых соседей</item>
    /// </list>
    /// </remarks>
    private void DFS(int node, int parent, List<int>[] graph, int[,] up, 
                     int[] depth, bool[] visited, int LOG) {
        visited[node] = true;
        
        // На 2^0 = 1 ребро вверх находится родитель
        up[node, 0] = parent;
        
        // Заполняем таблицу двоичных подъёмов
        // up[node,i] = вершина, в которую придём, поднявшись на 2^i рёбер
        for (int i = 1; i < LOG; i++) {
            up[node, i] = up[up[node, i-1], i-1];
        }
        
        // Рекурсивно обходим всех непосещённых соседей
        foreach (int neighbor in graph[node]) {
            if (!visited[neighbor]) {
                depth[neighbor] = depth[node] + 1;
                DFS(neighbor, node, graph, up, depth, visited, LOG);
            }
        }
    }
    
    /// <summary>
    /// Нахождение наименьшего общего предка (LCA) двух вершин
    /// с использованием метода двоичного подъёма
    /// </summary>
    /// <param name="u">Первая вершина</param>
    /// <param name="v">Вторая вершина</param>
    /// <param name="up">Таблица двоичных подъёмов</param>
    /// <param name="depth">Массив глубин вершин</param>
    /// <param name="LOG">Максимальная степень двойки</param>
    /// <returns>Наименьший общий предок вершин u и v</returns>
    /// <remarks>
    /// Алгоритм LCA:
    /// <list type="number">
    /// <item><b>Выравнивание глубин:</b> Поднимаем более глубокую вершину 
    /// на разницу глубин, используя двоичное представление разницы</item>
    /// <item><b>Проверка совпадения:</b> Если вершины совпали после выравнивания,
    /// это и есть LCA</item>
    /// <item><b>Двоичный подъём:</b> Поднимаем обе вершины одновременно,
    /// начиная с наибольшей степени двойки. Если предки различаются - поднимаемся</item>
    /// <item><b>Результат:</b> Родитель любой из вершин является LCA</item>
    /// </list>
    /// </remarks>
    private int LCA(int u, int v, int[,] up, int[] depth, int LOG) {
        // Шаг 1: Выравниваем глубины - u должна быть не выше v
        if (depth[u] < depth[v]) {
            int temp = u;
            u = v;
            v = temp;
        }
        
        // Поднимаем u на разницу глубин
        int diff = depth[u] - depth[v];
        for (int i = 0; i < LOG; i++) {
            if ((diff & (1 << i)) != 0) {
                u = up[u, i];
            }
        }
        
        // Шаг 2: Если вершины совпали, LCA найден
        if (u == v) {
            return u;
        }
        
        // Шаг 3: Поднимаем обе вершины одновременно
        // Идём от больших степеней к меньшим
        for (int i = LOG - 1; i >= 0; i--) {
            if (up[u, i] != up[v, i]) {
                u = up[u, i];
                v = up[v, i];
            }
        }
        
        // Шаг 4: Родитель u является LCA
        return up[u, 0];
    }
}