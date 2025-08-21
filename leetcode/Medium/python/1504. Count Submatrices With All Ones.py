'''
https://leetcode.com/problems/count-submatrices-with-all-ones/description/?envType=daily-question&envId=2025-08-21
'''

class Solution:
    def numSubmat(self, mat):
        """
        Подсчёт количества подматриц, состоящих только из единиц.
        :param mat: бинарная матрица (list[list[int]])
        :return: количество подматриц (int)
        
        Алгоритм:
        1. Для каждой клетки (i, j) считаем, сколько подряд идущих единиц
           слева до неё (включая её).
        2. Считаем количество подматриц, в которых (i, j) — правый нижний угол.
        3. Для этого поднимаемся вверх по строкам, уменьшая минимальную ширину
           и добавляем её к ответу.
        """
        m, n = len(mat), len(mat[0])
        continuous = [[0] * n for _ in range(m)]

        # Подсчёт подряд идущих единиц в строках
        for i in range(m):
            for j in range(n):
                if mat[i][j] == 1:
                    continuous[i][j] = (continuous[i][j - 1] if j > 0 else 0) + 1

        ans = 0
        # Подсчёт количества подматриц
        for i in range(m):
            for j in range(n):
                min_width = float("inf")
                for k in range(i, -1, -1):
                    min_width = min(min_width, continuous[k][j])
                    ans += min_width
        return ans

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks