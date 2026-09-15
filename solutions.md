# LeetCode 3558 — Number of Ways to Assign Edge Weights I

## Описание задачи

Дано неориентированное дерево из `n` узлов, пронумерованных от 1 до `n`, с корнем в узле 1.
Дерево задано массивом рёбер `edges`, где `edges[i] = [u_i, v_i]`.
Каждому ребру нужно присвоить вес **1** или **2**.
Выберите любой узел `x` на максимальной глубине. Верните количество способов назначить веса рёбер на пути от узла 1 до `x` так, чтобы суммарная стоимость пути была **нечётной**. Результат верните по модулю `10^9 + 7`.

## Идея решения

1. **BFS от корня** для нахождения максимальной глубины дерева `d`.
2. Путь от корня до узла на глубине `d` содержит ровно `d` рёбер.
3. Каждое ребро можно назначить весом 1 или 2 → всего `2^d` комбинаций.
4. Ровно половина комбинаций даёт нечётную сумму → ответ: `2^(d-1) mod (10^9+7)`.

**Почему ровно половина?** Зафиксируем веса первых `d-1` рёбер. Тогда вес последнего ребра однозначно определяет чётность суммы: если сумма первых `d-1` чётная — нужен вес 1; если нечётная — нужен вес 2. Ровно один выбор из двух для последнего ребра делает сумму нечётной.

---

## C++

```cpp
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
```

---

## C#

```csharp
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
```

---

## Java

```java
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
```

---

## JavaScript

```javascript
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
 *
 * @param {number[][]} edges - массив рёбер дерева
 * @return {number} количество способов по модулю 10^9 + 7
 */
var assignEdgeWeights = function(edges) {
    const MOD = 1_000_000_007;
    const n = edges.length + 1;

    // Строим список смежности
    const graph = Array.from({ length: n + 1 }, () => []);
    for (const [u, v] of edges) {
        graph[u].push(v);
        graph[v].push(u);
    }

    // BFS для нахождения максимальной глубины
    const queue = [1];
    const visited = new Array(n + 1).fill(false);
    visited[1] = true;
    let depth = 0;

    while (queue.length > 0) {
        const levelSize = queue.length;
        for (let i = 0; i < levelSize; i++) {
            const u = queue.shift();
            for (const v of graph[u]) {
                if (!visited[v]) {
                    visited[v] = true;
                    queue.push(v);
                }
            }
        }
        depth++;
    }

    // Количество способов = 2^(depth - 2) mod MOD
    // depth — число уровней BFS, число рёбер = depth - 1
    if (depth < 2) return 0;
    return Number(modPow(2n, BigInt(depth - 2), BigInt(MOD)));
};

/**
 * Быстрое возведение в степень по модулю (BigInt)
 *
 * @param {bigint} base - основание
 * @param {bigint} exp - показатель степени
 * @param {bigint} mod - модуль
 * @returns {bigint} (base^exp) mod mod
 */
function modPow(base, exp, mod) {
    let result = 1n;
    base = base % mod;
    while (exp > 0n) {
        if (exp % 2n === 1n) {
            result = result * base % mod;
        }
        exp = exp / 2n;
        base = base * base % mod;
    }
    return result;
}
```

---

## Python

```python
from collections import deque
from typing import List


class Solution:
    """
    Решение задачи LeetCode 3558: Number of Ways to Assign Edge Weights I

    Дано неориентированное дерево из n узлов с корнем в узле 1.
    Каждому ребру назначается вес 1 или 2. Нужно найти количество способов
    назначить веса на пути от корня до узла максимальной глубины так,
    чтобы сумма весов была нечётной. Ответ вернуть по модулю 10^9 + 7.

    Идея: находим максимальную глубину d через BFS. Путь содержит d рёбер,
    и ровно 2^(d-1) комбинаций дают нечётную сумму.

    Временная сложность: O(n)
    Пространственная сложность: O(n)
    """

    MOD = 1000000007

    def assignEdgeWeights(self, edges: List[List[int]]) -> int:
        n = len(edges) + 1

        # Строим список смежности
        graph = [[] for _ in range(n + 1)]
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)

        # BFS для нахождения максимальной глубины
        queue = deque([1])
        visited = [False] * (n + 1)
        visited[1] = True
        depth = 0

        while queue:
            level_size = len(queue)
            for _ in range(level_size):
                u = queue.popleft()
                for v in graph[u]:
                    if not visited[v]:
                        visited[v] = True
                        queue.append(v)
            depth += 1

        # Количество способов = 2^(depth - 2) mod MOD
        # depth — число уровней BFS, число рёбер на максимальном пути = depth - 1
        if depth < 2:
            return 0
        return pow(2, depth - 2, self.MOD)
```
