"""
Python (Binary Search + BFS)

Последний день, когда можно перейти от верхней строки к нижней

@param row: Количество строк в сетке
@param col: Количество столбцов в сетке  
@param cells: Массив ячеек, которые становятся водой каждый день
@return: Последний день (0-индексированный), когда можно перейти сверху вниз

Сложность: Время O((row*col) * log(row*col)), Память O(row*col)

Автор: Дуплей Максим Игоревич
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
    def latestDayToCross(self, row: int, col: int, cells: List[List[int]]) -> int:
        def can_cross(day: int) -> bool:
            grid = [[0] * col for _ in range(row)]
            
            for i in range(day):
                r, c = cells[i]
                grid[r-1][c-1] = 1
            
            queue = deque()
            for c in range(col):
                if grid[0][c] == 0:
                    queue.append((0, c))
                    grid[0][c] = 1
            
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            
            while queue:
                r, c = queue.popleft()
                
                if r == row - 1:
                    return True
                
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    
                    if 0 <= nr < row and 0 <= nc < col and grid[nr][nc] == 0:
                        grid[nr][nc] = 1
                        queue.append((nr, nc))
            
            return False
        
        left, right = 0, len(cells)
        
        while left < right:
            mid = left + (right - left + 1) // 2
            if can_cross(mid):
                left = mid
            else:
                right = mid - 1
        
        return left