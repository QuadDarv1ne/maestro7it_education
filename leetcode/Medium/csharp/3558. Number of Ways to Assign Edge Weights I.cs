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

/**
 * <summary>
 * Решение задачи LeetCode 3558: Number of Ways to Assign Edge Weights I
 *
 * Дано неориентированное дерево из n узлов с корнем в узле 1.
 * Каждому ребру назначается вес 1 или 2. Нужно найти количество способов
 * назначить веса на пути от корня до узла максимальной глубины так,
 * чтобы сумма весов была нечётной. Ответ вернуть по модулю 10^9 + 7.
 *
 * Идея: находим максимальную глубину d через BFS. Путь содержит d рёбер,
 * и ровно 2^(d-1) комбинаций дают нечётную сумму.
 *
 * Временная сложность: O(n)
 * Пространственная сложность: O(n)
 * </summary>
 */
public class Solution {
    private const int MOD = 1_000_000_007;

    public int AssignEdgeWeights(int[][] edges) {
        int n = edges.Length + 1;

        // Строим список смежности
        var graph = new List<int>[n + 1];
        for (int i = 0; i <= n; i++) {
            graph[i] = new List<int>();
        }
        foreach (var edge in edges) {
            graph[edge[0]].Add(edge[1]);
            graph[edge[1]].Add(edge[0]);
        }

        // BFS для нахождения максимальной глубины
        var queue = new Queue<int>();
        queue.Enqueue(1);
        var visited = new bool[n + 1];
        visited[1] = true;
        int depth = 0;

        while (queue.Count > 0) {
            int levelSize = queue.Count;
            for (int i = 0; i < levelSize; i++) {
                int u = queue.Dequeue();
                foreach (int v in graph[u]) {
                    if (!visited[v]) {
                        visited[v] = true;
                        queue.Enqueue(v);
                    }
                }
            }
            depth++;
        }

        // Количество способов = 2^(depth - 2) mod MOD
        // depth — число уровней BFS, число рёбер = depth - 1
        if (depth < 2) return 0;
        return (int)ModPow(2, depth - 2, MOD);
    }

    /// <summary>
    /// Быстрое возведение в степень по модулю
    /// </summary>
    /// <param name="baseVal">Основание</param>
    /// <param name="exp">Показатель степени</param>
    /// <param name="mod">Модуль</param>
    /// <returns>(baseVal^exp) mod mod</returns>
    private long ModPow(long baseVal, long exp, long mod) {
        long result = 1;
        baseVal %= mod;
        while (exp > 0) {
            if (exp % 2 == 1) {
                result = result * baseVal % mod;
            }
            exp /= 2;
            baseVal = baseVal * baseVal % mod;
        }
        return result;
    }
}