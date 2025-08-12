'''
https://leetcode.com/contest/weekly-contest-462/problems/flip-square-submatrix-vertically/submissions/
'''

class Solution:
    def reverseSubmatrix(self, grid, x, y, k):
        """
        Переворачивает (по вертикали) квадратную подматрицу k×k в матрице grid.

        :param grid: Матрица (m×n) целых чисел.
        :param x: Индекс строки верхнего левого угла подматрицы.
        :param y: Индекс столбца верхнего левого угла подматрицы.
        :param k: Размер стороны подматрицы.
        :return: Матрица после вертикального переворота подматрицы.

        Алгоритм:
        1. Идём сверху вниз до середины подматрицы.
        2. Для каждой пары строк внутри подматрицы меняем элементы местами.
        3. Остальная матрица остаётся неизменной.

        Сложность:
        - Время: O(k²)
        - Память: O(1)
        """
        for i in range(k // 2):
            top_row = x + i
            bottom_row = x + k - 1 - i
            for j in range(k):
                col = y + j
                grid[top_row][col], grid[bottom_row][col] = grid[bottom_row][col], grid[top_row][col]
        return grid

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks