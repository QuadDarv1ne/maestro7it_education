'''
https://leetcode.com/problems/network-delay-time/description/
'''

# import heapq
# from collections import defaultdict

class Solution:
    # def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
    def networkDelayTime(self, times, n, k):
        """
        Определяет минимальное время, необходимое для доставки сигнала от узла k ко всем остальным узлам сети.
        Используется алгоритм Дейкстры для поиска кратчайших путей.

        :param times: Список рёбер сети, где каждый элемент [u, v, w] означает, что сигнал от узла u до узла v передаётся за w единиц времени.
        :param n: Количество узлов в сети.
        :param k: Индекс начального узла (1-based).
        :return: Минимальное время доставки сигнала ко всем узлам сети или -1, если это невозможно.
        """
        graph = defaultdict(list)
        for u, v, w in times:
            graph[u].append((v, w))

        # Инициализация расстояний от начального узла
        dist = {i: float('inf') for i in range(1, n + 1)}
        dist[k] = 0

        # Очередь с приоритетом (min-heap)
        pq = [(0, k)]  # (время, узел)

        while pq:
            d, node = heapq.heappop(pq)

            if d > dist[node]:
                continue

            for neighbor, time in graph[node]:
                new_dist = d + time
                if new_dist < dist[neighbor]:
                    dist[neighbor] = new_dist
                    heapq.heappush(pq, (new_dist, neighbor))

        max_time = max(dist.values())
        return max_time if max_time < float('inf') else -1

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks