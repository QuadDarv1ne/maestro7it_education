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
 */
class Solution {
    private static final int MOD = 1_000_000_007;

    public int assignEdgeWeights(int[][] edges) {
        int n = edges.length + 1;

        // Строим список смежности
        List<List<Integer>> graph = new ArrayList<>();
        for (int i = 0; i <= n; i++) {
            graph.add(new ArrayList<>());
        }
        for (int[] edge : edges) {
            graph.get(edge[0]).add(edge[1]);
            graph.get(edge[1]).add(edge[0]);
        }

        // BFS для нахождения максимальной глубины
        Queue<Integer> queue = new ArrayDeque<>();
        queue.offer(1);
        boolean[] visited = new boolean[n + 1];
        visited[1] = true;
        int depth = 0;

        while (!queue.isEmpty()) {
            int levelSize = queue.size();
            for (int i = 0; i < levelSize; i++) {
                int u = queue.poll();
                for (int v : graph.get(u)) {
                    if (!visited[v]) {
                        visited[v] = true;
                        queue.offer(v);
                    }
                }
            }
            depth++;
        }

        // Количество способов = 2^(depth - 2) mod MOD
        // depth — число уровней BFS, число рёбер на максимальном пути = depth - 1
        if (depth < 2) return 0;
        return (int) modPow(2, depth - 2, MOD);
    }

    /**
     * Быстрое возведение в степень по модулю
     *
     * @param base основание
     * @param exp  показатель степени
     * @param mod  модуль
     * @return (base^exp) mod mod
     */
    private long modPow(long base, long exp, long mod) {
        long result = 1;
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
}