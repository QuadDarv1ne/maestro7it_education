'''
https://leetcode.com/problems/length-of-longest-v-shaped-diagonal-segment/description/?envType=daily-question&envId=2025-08-27
'''

class Solution(object):
    def lenOfVDiagonal(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int

        Задача:
        -----------------
        В матрице grid нужно найти длину самого длинного "V-образного"
        диагонального сегмента.

        Правила сегмента:
        1. Сегмент всегда начинается с числа 1.
        2. Далее значения должны чередоваться строго по шаблону:
           2, 0, 2, 0, ...
        3. Сегмент идёт по диагонали в одном из четырёх направлений:
           ↘, ↗, ↙, ↖.
        4. Разрешается не более одного поворота на 90° по часовой стрелке
           (например, из ↘ можно повернуть в ↙).
        5. Нужно вернуть максимальную длину такого сегмента (в клетках).
        Если ни одного сегмента нет, вернуть 0.

        Пример:
        -----------------
        Вход:
        [[2,2,1,2,2],
         [2,0,2,2,0],
         [2,0,1,1,0],
         [1,0,2,2,2],
         [2,0,0,2,2]]

        Выход: 5
        (максимальный сегмент с поворотом).
        """
        n, m = len(grid), len(grid[0])
        nxt = {1: 2, 2: 0, 0: 2}

        # Направления (dx, dy): 0:↘, 1:↗, 2:↙, 3:↖
        dirs = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
        cw = {0: 2, 1: 0, 2: 3, 3: 1}  # поворот на 90° по часовой

        def ok(a, b):
            return nxt.get(a) == b

        # end[d][i][j]: длина корректной цепочки, заканчивающейся в (i,j) по d,
        # причём вся цепочка стартует с 1.
        end = [[[0] * m for _ in range(n)] for _ in range(4)]

        for d, (dx, dy) in enumerate(dirs):
            xs = range(n) if dx == 1 else range(n - 1, -1, -1)
            ys = range(m) if dy == 1 else range(m - 1, -1, -1)
            for i in xs:
                for j in ys:
                    val = grid[i][j]
                    pi, pj = i - dx, j - dy
                    if 0 <= pi < n and 0 <= pj < m and ok(grid[pi][pj], val) and end[d][pi][pj] > 0:
                        end[d][i][j] = end[d][pi][pj] + 1
                    else:
                        end[d][i][j] = 1 if val == 1 else 0

        # go[d][i][j]: длина корректной цепочки, начинающейся в (i,j) и идущей вперёд по d
        # (НЕ требуем, чтобы старт был 1).
        go = [[[1] * m for _ in range(n)] for _ in range(4)]

        for d, (dx, dy) in enumerate(dirs):
            xs = range(n - 1, -1, -1) if dx == 1 else range(n)
            ys = range(m - 1, -1, -1) if dy == 1 else range(m)
            for i in xs:
                for j in ys:
                    ni, nj = i + dx, j + dy
                    if 0 <= ni < n and 0 <= nj < m and ok(grid[i][j], grid[ni][nj]):
                        go[d][i][j] = 1 + go[d][ni][nj]
                    else:
                        go[d][i][j] = 1

        ans = 0
        # Прямые сегменты (без поворота)
        for d in range(4):
            for i in range(n):
                for j in range(m):
                    ans = max(ans, end[d][i][j])

        # V-сегменты с поворотом
        for i in range(n):
            for j in range(m):
                for a in range(4):
                    b = cw[a]
                    if end[a][i][j] > 0:  # первая ножка существует и начинается с 1
                        cur = end[a][i][j] + go[b][i][j] - 1
                        ans = max(ans, cur)

        return ans

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks