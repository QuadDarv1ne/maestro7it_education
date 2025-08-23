'''
https://leetcode.com/problems/find-the-minimum-area-to-cover-all-ones-ii/description/?envType=daily-question&envId=2025-08-23
'''

# from typing import List

class Solution:
    """
    Находит минимальную суммарную площадь трёх непересекающихся прямоугольников,
    покрывающих все единицы в бинарной матрице.
    Реализует все необходимые конфигурации разрезов (гориз./верт., и смешанные случаи).
    """
    # def minimumSum(self, grid: List[List[int]]) -> int:
    def minimumSum(self, grid):
        m = len(grid); n = len(grid[0])
        INF = m * n + 5
        ans = INF

        def area(r1, r2, c1, c2):
            rmin = 10**9; rmax = -10**9; cmin = 10**9; cmax = -10**9
            for r in range(r1, r2+1):
                for c in range(c1, c2+1):
                    if grid[r][c] == 1:
                        if r < rmin: rmin = r
                        if r > rmax: rmax = r
                        if c < cmin: cmin = c
                        if c > cmax: cmax = c
            if rmin == 10**9:
                return 0
            return (rmax - rmin + 1) * (cmax - cmin + 1)

        # три горизонтальных полосы
        for i in range(1, m):
            for j in range(i+1, m):
                a = area(0, i-1, 0, n-1)
                b = area(i, j-1, 0, n-1)
                c = area(j, m-1, 0, n-1)
                ans = min(ans, a + b + c)

        # три вертикальных полосы
        for i in range(1, n):
            for j in range(i+1, n):
                a = area(0, m-1, 0, i-1)
                b = area(0, m-1, i, j-1)
                c = area(0, m-1, j, n-1)
                ans = min(ans, a + b + c)

        # горизонтальный + вертикальное разбиение в верхней/нижней части
        for i in range(0, m-1):
            for j in range(0, n-1):
                topLeft = area(0, i, 0, j)
                topRight = area(0, i, j+1, n-1)
                bottom = area(i+1, m-1, 0, n-1)
                ans = min(ans, topLeft + topRight + bottom)

                top = area(0, i, 0, n-1)
                bottomLeft = area(i+1, m-1, 0, j)
                bottomRight = area(i+1, m-1, j+1, n-1)
                ans = min(ans, top + bottomLeft + bottomRight)

        # вертикальный + горизонтальное разбиение в левой/правой части
        for i in range(0, n-1):
            for j in range(0, m-1):
                leftTop = area(0, j, 0, i)
                leftBottom = area(j+1, m-1, 0, i)
                right = area(0, m-1, i+1, n-1)
                ans = min(ans, leftTop + leftBottom + right)

                left = area(0, m-1, 0, i)
                rightTop = area(0, j, i+1, n-1)
                rightBottom = area(j+1, m-1, i+1, n-1)
                ans = min(ans, left + rightTop + rightBottom)

        return ans if ans != INF else 0

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks