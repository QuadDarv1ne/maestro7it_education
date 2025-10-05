'''
https://leetcode.com/problems/pacific-atlantic-water-flow/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
'''

class Solution(object):
    def pacificAtlantic(self, heights):
        """
        Решение задачи Pacific Atlantic Water Flow.
        Алгоритм: DFS от океанов (в обратном направлении потока воды).
        Сложность: O(m * n)
        """
        if not heights or not heights[0]:
            return []
        m, n = len(heights), len(heights[0])

        pac = [[False] * n for _ in range(m)]
        atl = [[False] * n for _ in range(m)]
        dirs = ((1,0),(-1,0),(0,1),(0,-1))

        def dfs(x, y, visited):
            visited[x][y] = True
            for dx, dy in dirs:
                nx, ny = x + dx, y + dy
                if 0 <= nx < m and 0 <= ny < n and not visited[nx][ny] and heights[nx][ny] >= heights[x][y]:
                    dfs(nx, ny, visited)

        for i in range(m):
            dfs(i, 0, pac)
            dfs(i, n - 1, atl)
        for j in range(n):
            dfs(0, j, pac)
            dfs(m - 1, j, atl)

        res = [[i, j] for i in range(m) for j in range(n) if pac[i][j] and atl[i][j]]
        return res

''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks