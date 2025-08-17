/**
 * https://leetcode.com/problems/network-delay-time/description/
 */

/**
 * Определяет минимальное время, необходимое для доставки сигнала от узла k ко всем остальным узлам сети.
 * Используется алгоритм Дейкстры для поиска кратчайших путей.
 *
 * @param {number[][]} times Список рёбер сети, где каждый элемент [u, v, w] означает, что сигнал от узла u до узла v передаётся за w единиц времени.
 * @param {number} n Количество узлов в сети.
 * @param {number} k Индекс начального узла (1-based).
 * @return {number} Минимальное время доставки сигнала ко всем узлам сети или -1, если это невозможно.
 */
var networkDelayTime = function(times, n, k) {
    const graph = Array.from({ length: n + 1 }, () => []);
    for (const [u, v, w] of times) {
        graph[u].push([v, w]);
    }

    const dist = Array(n + 1).fill(Infinity);
    dist[k] = 0;

    const pq = [[0, k]]; // [время, узел]

    while (pq.length) {
        pq.sort((a, b) => a[0] - b[0]);
        const [d, node] = pq.shift();

        if (d > dist[node]) continue;

        for (const [neighbor, time] of graph[node]) {
            const newDist = d + time;
            if (newDist < dist[neighbor]) {
                dist[neighbor] = newDist;
                pq.push([newDist, neighbor]);
            }
        }
    }

    const maxTime = Math.max(...dist.slice(1));
    return maxTime === Infinity ? -1 : maxTime;
};

/*
''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
*/