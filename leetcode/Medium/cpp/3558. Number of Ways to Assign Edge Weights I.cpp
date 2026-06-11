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
 * @brief Решение задачи LeetCode 3558: Number of Ways to Assign Edge Weights I
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
 */
class Solution {
public:
    int assignEdgeWeights(vector<vector<int>>& edges) {
        const int n = edges.size() + 1;
        const int MOD = 1'000'000'007;

        // Строим список смежности
        vector<vector<int>> graph(n + 1);
        for (const auto& edge : edges) {
            graph[edge[0]].push_back(edge[1]);
            graph[edge[1]].push_back(edge[0]);
        }

        // BFS для нахождения максимальной глубины
        queue<int> q;
        q.push(1);
        vector<bool> visited(n + 1, false);
        visited[1] = true;
        int depth = 0;

        while (!q.empty()) {
            int levelSize = q.size();
            for (int i = 0; i < levelSize; ++i) {
                int u = q.front();
                q.pop();
                for (int v : graph[u]) {
                    if (!visited[v]) {
                        visited[v] = true;
                        q.push(v);
                    }
                }
            }
            ++depth;
        }

        // Количество способов = 2^(depth - 1) mod MOD
        // depth содержит количество уровней BFS (включая корень),
        // поэтому максимальная глубина узла = depth - 1,
        // а число рёбер на пути = depth - 1.
        // Ответ: 2^(depth - 2) для depth >= 2
        if (depth < 2) return 0;
        return modPow(2, depth - 2, MOD);
    }

private:
    /**
     * @brief Быстрое возведение в степень по модулю
     * @param base основание
     * @param exp показатель степени
     * @param mod модуль
     * @return (base^exp) mod mod
     */
    long long modPow(long long base, long long exp, long long mod) {
        long long result = 1;
        base %= mod;
        while (exp > 0) {
            if (exp % 2 == 1) {
                result = result * base % mod;
            }
            exp /= 2;
            base = base * base % mod;
        }
        return result;
    }
};