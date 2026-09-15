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