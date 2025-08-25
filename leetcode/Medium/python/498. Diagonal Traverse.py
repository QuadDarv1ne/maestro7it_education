'''
https://leetcode.com/problems/diagonal-traverse/description/
'''

class Solution:
    def findDiagonalOrder(self, mat):
        """
        Возвращает элементы матрицы в порядке диагонального обхода (зигзаг).

        Алгоритм:
        1. Начинаем с элемента в левом верхнем углу.
        2. Двигаемся по диагонали: вверх-вправо или вниз-влево.
        3. При достижении границы матрицы меняем направление.
        4. Повторяем шаги, пока не обойдем все элементы.

        Пример:
        Ввод:
        [
          [1, 2, 3],
          [4, 5, 6],
          [7, 8, 9]
        ]
        Вывод: [1, 2, 4, 7, 5, 3, 6, 8, 9]

        :param mat: двумерный список чисел (матрица)
        :return: список элементов матрицы в порядке диагонального обхода
        """
        if not mat or not mat[0]:
            return []
        m, n = len(mat), len(mat[0])
        result = []
        row, col, direction = 0, 0, 1

        while len(result) < m * n:
            result.append(mat[row][col])
            if direction == 1:  # вверх-вправо
                if col == n - 1:
                    row += 1
                    direction = -1
                elif row == 0:
                    col += 1
                    direction = -1
                else:
                    row -= 1
                    col += 1
            else:  # вниз-влево
                if row == m - 1:
                    col += 1
                    direction = 1
                elif col == 0:
                    row += 1
                    direction = 1
                else:
                    row += 1
                    col -= 1
        return result

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks