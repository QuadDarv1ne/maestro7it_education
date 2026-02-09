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
"""

class Solution:
    def maximalSquare(self, matrix):
        """
        Находит максимальную площадь квадрата, состоящего только из '1'
        в бинарной матрице.
        
        Алгоритм: Динамическое программирование
        - dp[i][j] = сторона максимального квадрата с правым нижним углом в (i,j)
        - Если matrix[i][j] == '1', то dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1
        - Иначе dp[i][j] = 0
        
        Сложность:
        Время: O(m × n)
        Пространство: O(m × n), можно оптимизировать до O(n)
        
        Параметры:
        ----------
        matrix : List[List[str]]
            Двоичная матрица m x n из символов '0' и '1'
            
        Возвращает:
        -----------
        int
            Площадь максимального квадрата из '1'
        """
        if not matrix or not matrix[0]:
            return 0
        
        m, n = len(matrix), len(matrix[0])
        dp = [[0] * n for _ in range(m)]
        max_side = 0
        
        for i in range(m):
            for j in range(n):
                if matrix[i][j] == '1':
                    if i == 0 or j == 0:
                        dp[i][j] = 1
                    else:
                        dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1
                    max_side = max(max_side, dp[i][j])
        
        return max_side * max_side