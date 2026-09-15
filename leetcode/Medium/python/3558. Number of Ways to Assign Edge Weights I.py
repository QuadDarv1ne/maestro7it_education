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