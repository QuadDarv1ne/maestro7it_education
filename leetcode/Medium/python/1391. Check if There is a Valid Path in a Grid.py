'''
https://leetcode.com/problems/balance-a-binary-search-tree/description/
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

from collections import deque
# from typing import List

class Solution:
    def hasValidPath(self, grid):
        m, n = len(grid), len(grid[0])
        # delta для направлений 0: вверх, 1: вправо, 2: вниз, 3: влево
        dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        
        # Предрасчёт допустимых направлений для каждого типа труб (1-6)
        pipes = [
            [],          # индекс 0 не используется
            [1, 3],      # тип 1
            [0, 2],      # тип 2
            [2, 3],      # тип 3
            [1, 2],      # тип 4
            [0, 3],      # тип 5
            [0, 1]       # тип 6
        ]
        
        visited = [[False] * n for _ in range(m)]
        q = deque()
        q.append((0, 0))
        visited[0][0] = True
        
        while q:
            x, y = q.popleft()
            if x == m-1 and y == n-1:
                return True
            
            cell_type = grid[x][y]
            for d in pipes[cell_type]:
                dx, dy = dirs[d]
                nx, ny = x + dx, y + dy
                
                if not (0 <= nx < m and 0 <= ny < n) or visited[nx][ny]:
                    continue
                
                next_type = grid[nx][ny]
                # Проверка возможности обратного движения
                possible_back = any(rd == (d ^ 2) for rd in pipes[next_type])
                if possible_back:
                    visited[nx][ny] = True
                    q.append((nx, ny))
        
        return False