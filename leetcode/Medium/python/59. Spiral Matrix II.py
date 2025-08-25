'''
https://leetcode.com/problems/spiral-matrix-ii/description/
'''

class Solution(object):
    def generateMatrix(self, n):
        """
        Генерация матрицы n x n, заполненной числами от 1 до n^2
        по спирали (по часовой стрелке, начиная сверху слева).

        :type n: int
        :rtype: List[List[int]]
        """
        # Создаем пустую матрицу n x n
        matrix = [[0] * n for _ in range(n)]
        
        left, right = 0, n - 1   # границы по столбцам
        top, bottom = 0, n - 1   # границы по строкам
        num = 1                  # число, которое будем записывать

        while left <= right and top <= bottom:
            # Заполняем верхнюю строку слева направо
            for j in range(left, right + 1):
                matrix[top][j] = num
                num += 1
            top += 1

            # Заполняем правый столбец сверху вниз
            for i in range(top, bottom + 1):
                matrix[i][right] = num
                num += 1
            right -= 1

            # Заполняем нижнюю строку справа налево (если осталась)
            if top <= bottom:
                for j in range(right, left - 1, -1):
                    matrix[bottom][j] = num
                    num += 1
                bottom -= 1

            # Заполняем левый столбец снизу вверх (если остался)
            if left <= right:
                for i in range(bottom, top - 1, -1):
                    matrix[i][left] = num
                    num += 1
                left += 1

        return matrix

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks