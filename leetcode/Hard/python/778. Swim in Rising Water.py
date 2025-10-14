'''
https://leetcode.com/problems/swim-in-rising-water/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
'''

import heapq

class Solution(object):
    def swimInWater(self, grid):
        """
        Решение задачи Swim in Rising Water (LeetCode 778).

        Использует подход с приоритетной очередью:
        - Поддерживаем минимальное “время” (макс высоту) для попадания в каждую клетку.
        - Расширяемся от (0,0), всегда вытаскивая клетку с минимальным требованием.
        - Ответ — как только достигаем (n-1, n-1).
        Сложность: O(n^2 log n^2) = O(n^2 log n).
        """
        n = len(grid)
        # направления
        dirs = [(1,0),(-1,0),(0,1),(0,-1)]
        seen = [[False]*n for _ in range(n)]
        # heap хранит кортежи (время, x, y)
        heap = [(grid[0][0], 0, 0)]
        seen[0][0] = True
        res = 0

        while heap:
            time, x, y = heapq.heappop(heap)
            # обновляем минимальное время, необходимое до этой точки
            if time > res:
                res = time
            # если дошли до конца — это ответ
            if x == n-1 and y == n-1:
                return res
            # расширяемся к соседям
            for dx, dy in dirs:
                nx, ny = x + dx, y + dy
                if 0 <= nx < n and 0 <= ny < n and not seen[nx][ny]:
                    seen[nx][ny] = True
                    # время для соседа — max(время текущей клетки, высота соседа)
                    heapq.heappush(heap, (max(time, grid[nx][ny]), nx, ny))
        return -1

''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks