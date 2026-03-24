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

Находит максимальное неотрицательное произведение на пути из (0,0) в (m-1,n-1).

Параметры:
    grid (List[List[int]]): Матрица целых чисел размером m x n.

Возвращает:
    int: Максимальное неотрицательное произведение по модулю 10^9+7,
         или -1, если такого произведения нет.

Примечания:
    - Движение возможно только вправо или вниз.
    - Отрицательные числа могут менять знак произведения.
    - Используется динамическое программирование с отслеживанием максимального
      и минимального произведения в каждой ячейке.
    - Сложность: O(m*n) по времени и O(m*n) по памяти.

Пример:
    >>> grid = [[1,-2,1],[1,-2,1],[3,-4,1]]
    >>> maxProductPath(grid)
    8
"""

class Solution(object):
    def maxProductPath(self, grid):
        MOD = 10**9 + 7
        m = len(grid)
        n = len(grid[0])
        
        # Создаем таблицы для хранения максимального и минимального произведения
        max_dp = [[0] * n for _ in range(m)]
        min_dp = [[0] * n for _ in range(m)]
        
        # Инициализация начальной ячейки
        max_dp[0][0] = min_dp[0][0] = grid[0][0]
        
        # Заполняем первую строку
        for j in range(1, n):
            max_dp[0][j] = min_dp[0][j] = max_dp[0][j-1] * grid[0][j]
        
        # Заполняем первый столбец
        for i in range(1, m):
            max_dp[i][0] = min_dp[i][0] = max_dp[i-1][0] * grid[i][0]
        
        # Основной DP
        for i in range(1, m):
            for j in range(1, n):
                curr = grid[i][j]
                # Возможные значения сверху и слева
                candidates = [
                    max_dp[i-1][j] * curr,
                    min_dp[i-1][j] * curr,
                    max_dp[i][j-1] * curr,
                    min_dp[i][j-1] * curr
                ]
                max_dp[i][j] = max(candidates)
                min_dp[i][j] = min(candidates)
        
        # Проверяем результат
        result = max_dp[m-1][n-1]
        if result < 0:
            return -1
        return result % MOD