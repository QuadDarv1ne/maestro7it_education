'''
https://leetcode.com/problems/minimum-score-triangulation-of-polygon/description/?envType=daily-question&envId=2025-09-29
'''

class Solution:
    def minScoreTriangulation(self, values):
        """
        Решает задачу Minimum Score Triangulation of Polygon.

        Аргументы:
        - values: List[int], массив значений вершин многоугольника (в порядке обхода).

        Возвращает:
        - Минимально возможную сумму стоимостей треугольников при триангуляции.

        Подход:
        - Используем интервалный динамический программирования dp[i][j]:
            dp[i][j] = минимальная стоимость триангуляции многоугольника, образованного вершинами
                       от i до j включительно (по окружности, но мы работаем на прямом массиве).
        - Базовые случаи: dp[i][i+1] = 0 (интервал из двух вершин не образует треугольник).
        - Переход: для каждого k в (i, j): пытаемся сформировать треугольник (i, k, j) и объединить
          с dp[i][k] и dp[k][j].
        - Возвращаем dp[0][n-1].
        """
        n = len(values)
        # dp[i][j], размер n×n, инициализируем большими числами
        dp = [[0] * n for _ in range(n)]
        # рассматриваем интервалы длины ≥ 2 (т.е. j - i ≥ 2)
        for length in range(2, n):  # length = j - i
            for i in range(0, n - length):
                j = i + length
                best = float('inf')
                # выбираем точку k между i и j
                for k in range(i + 1, j):
                    cost = dp[i][k] + dp[k][j] + values[i] * values[k] * values[j]
                    if cost < best:
                        best = cost
                dp[i][j] = best
        return dp[0][n - 1]

''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks