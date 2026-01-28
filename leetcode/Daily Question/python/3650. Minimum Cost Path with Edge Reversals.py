"""
Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
 
Полезные ссылки:
1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
2. Telegram №1 @quadd4rv1n7
3. Telegram №2 @dupley_maxim_1999
4. Rutube канал: https://rutube.ru/channel/4218729/
5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
6. YouTube канал: https://www.youtube.com/@it-coders
7. ВК группа: https://vk.com/science_geeks
"""

from collections import defaultdict
import heapq

class Solution:
    def minCost(self, n, edges):
        """
        Находит минимальную стоимость пути от узла 0 до узла n-1 
        с возможностью разворота рёбер.
        
        Args:
            n: Количество узлов в графе
            edges: Массив рёбер [u, v, w], где u->v с весом w
            
        Returns:
            Минимальная стоимость пути или -1, если путь невозможен
        """
        # Создаём граф смежности: {узел: [(сосед, вес)]}
        graph = defaultdict(list)
        
        # Для каждого направленного ребра u -> v с весом w:
        # 1. Добавляем обычное ребро u -> v с весом w
        # 2. Добавляем развёрнутое ребро v -> u с весом 2*w (стоимость разворота)
        for u, v, w in edges:
            graph[u].append((v, w))        # Обычное направление
            graph[v].append((u, w * 2))    # Развёрнутое ребро
        
        # Алгоритм Дейкстры
        INF = float('inf')
        dist = [INF] * n
        dist[0] = 0
        
        # Очередь с приоритетом: (расстояние, узел)
        pq = [(0, 0)]
        
        while pq:
            d, u = heapq.heappop(pq)
            
            # Пропускаем устаревшие записи
            if d > dist[u]:
                continue
            
            # Если достигли конечного узла, возвращаем расстояние
            if u == n - 1:
                return d
            
            # Релаксация рёбер
            for v, w in graph[u]:
                new_dist = d + w
                if new_dist < dist[v]:
                    dist[v] = new_dist
                    heapq.heappush(pq, (new_dist, v))
        
        # Если узел n-1 недостижим
        return -1