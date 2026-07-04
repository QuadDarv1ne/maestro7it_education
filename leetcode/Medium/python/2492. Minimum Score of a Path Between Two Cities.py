'''
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
'''

from collections import defaultdict, deque
# from typing import List

class Solution:
    def minScore(self, n, roads):
        """
        Находит минимальный вес ребра на пути между городами 1 и n.
        
        Так как можно проходить по любому пути (включая циклы), 
        достаточно найти минимальное ребро в компоненте связности,
        содержащей оба города. Используем BFS для обхода компоненты.
        
        Args:
            n: Количество городов (от 1 до n)
            roads: Список дорог [a, b, distance], где a и b - города,
                   distance - вес ребра
            
        Returns:
            Минимальный вес ребра в компоненте связности городов 1 и n
            
        Examples:
            >>> sol = Solution()
            >>> sol.minScore(4, [[1,2,9],[2,3,6],[2,4,5],[1,4,7]])
            5
        """
        # Строим граф
        graph = defaultdict(list)
        for a, b, dist in roads:
            graph[a].append((b, dist))
            graph[b].append((a, dist))
        
        # BFS для обхода компоненты связности
        visited = [False] * (n + 1)
        queue = deque([1])
        visited[1] = True
        min_score = float('inf')
        
        while queue:
            city = queue.popleft()
            
            # Проверяем все соседние ребра
            for neighbor, dist in graph[city]:
                min_score = min(min_score, dist)
                if not visited[neighbor]:
                    visited[neighbor] = True
                    queue.append(neighbor)
        
        return min_score