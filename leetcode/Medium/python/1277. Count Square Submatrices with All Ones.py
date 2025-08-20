'''
https://leetcode.com/problems/count-square-submatrices-with-all-ones/description/?envType=daily-question&envId=2025-08-20
'''

# from typing import List

class Solution:
    # def countSquares(self, matrix: List[List[int]]) -> int:
    def countSquares(self, matrix):
        """
        Задача: посчитать количество квадратных подматриц,
        состоящих только из единиц.

        Метод:
        Используется динамическое программирование.
        dp[i][j] хранит размер наибольшего квадрата с правым нижним углом в (i, j).
        Если matrix[i][j] == 1, то:
            dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1
        Ответ — сумма всех dp[i][j].

        Временная сложность: O(m * n)
        Пространственная сложность: O(m * n) (можно оптимизировать до O(n))
        """
        m, n = len(matrix), len(matrix[0])
        ans = 0
        for i in range(m):
            for j in range(n):
                if matrix[i][j] == 1 and i > 0 and j > 0:
                    matrix[i][j] = min(matrix[i-1][j], matrix[i][j-1], matrix[i-1][j-1]) + 1
                ans += matrix[i][j]
        return ans

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks