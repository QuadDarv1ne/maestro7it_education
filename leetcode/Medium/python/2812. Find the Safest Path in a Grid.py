from collections import deque
from typing import List

class Solution:
    def maximumSafenessFactor(self, grid):
        """
        Находит максимальный коэффициент безопасности пути в сетке с ворами.

        Коэффициент безопасности пути определяется как минимальное манхэттенское 
        расстояние от любой клетки на пути до ближайшего вора. 
        Задача: найти путь из (0,0) в (n-1,n-1) с максимально возможным 
        минимальным расстоянием до воров.

        Алгоритм:
        1. Многопроходный BFS (поиск в ширину) от всех воров одновременно, 
           чтобы вычислить для каждой клетки расстояние до ближайшего вора.
        2. Бинарный поиск по возможному значению коэффициента безопасности.
        3. Для проверки конкретного значения `limit` используем BFS/DFS, 
           разрешая проход только по клеткам, расстояние до которых >= `limit`.

        Args:
            grid: Квадратная матрица n x n, где 1 - вор, 0 - пустая клетка.

        Returns:
            Максимальный возможный коэффициент безопасности пути.
        """
        n = len(grid)
        # Шаг 1: Вычисление расстояний до ближайшего вора с помощью многопроходного BFS
        dist = [[-1] * n for _ in range(n)]  # -1 означает не посещено
        q = deque()

        # Инициализация очереди всеми ворами
        for r in range(n):
            for c in range(n):
                if grid[r][c] == 1:
                    dist[r][c] = 0
                    q.append((r, c))

        # Всегда есть хотя бы один вор по условию
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        while q:
            r, c = q.popleft()
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n and dist[nr][nc] == -1:
                    dist[nr][nc] = dist[r][c] + 1
                    q.append((nr, nc))

        # Шаг 2: Бинарный поиск по коэффициенту безопасности
        # Левая граница - минимальное расстояние (0), правая - максимальное возможное (n*2)
        left, right = 0, 2 * n
        answer = 0

        def can_reach(limit):
            """
            Проверяет, можно ли добраться до (n-1,n-1), используя только клетки 
            с расстоянием до вора >= limit.

            Args:
                limit: Минимально допустимое расстояние до вора.

            Returns:
                True, если путь существует, иначе False.
            """
            # Если стартовая или конечная клетка не проходят по условию
            if dist[0][0] < limit or dist[n-1][n-1] < limit:
                return False
                
            visited = [[False] * n for _ in range(n)]
            dq = deque([(0, 0)])
            visited[0][0] = True

            while dq:
                r, c = dq.popleft()
                if r == n - 1 and c == n - 1:
                    return True
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < n and 0 <= nc < n and not visited[nr][nc] and dist[nr][nc] >= limit:
                        visited[nr][nc] = True
                        dq.append((nr, nc))
            return False

        # Бинарный поиск максимального допустимого limit
        while left <= right:
            mid = (left + right) // 2
            if can_reach(mid):
                answer = mid
                left = mid + 1
            else:
                right = mid - 1

        return answer