'''
https://leetcode.com/problems/sudoku-solver/description/?envType=daily-question&envId=2025-08-31
'''

class Solution(object):
    def solveSudoku(self, board):
        """
        Решает головоломку "Судоку" (9x9) с помощью оптимизированного бэктрекинга.
        Пустые клетки обозначены как ".".
        Решение выполняется на месте (in-place).

        :param board: List[List[str]] - игровое поле 9x9
        :rtype: None
        """

        # Таблицы для проверки: строки, столбцы, блоки
        rows = [[False] * 10 for _ in range(9)]
        cols = [[False] * 10 for _ in range(9)]
        boxes = [[False] * 10 for _ in range(9)]

        empties = []

        # Заполнение таблиц начальными числами
        for i in range(9):
            for j in range(9):
                if board[i][j] == ".":
                    empties.append((i, j))
                else:
                    d = int(board[i][j])
                    rows[i][d] = cols[j][d] = boxes[(i // 3) * 3 + (j // 3)][d] = True

        def backtrack(idx):
            if idx == len(empties):
                return True  # все заполнено

            i, j = empties[idx]
            box_id = (i // 3) * 3 + (j // 3)

            for d in range(1, 10):
                if not rows[i][d] and not cols[j][d] and not boxes[box_id][d]:
                    # ставим число
                    board[i][j] = str(d)
                    rows[i][d] = cols[j][d] = boxes[box_id][d] = True

                    if backtrack(idx + 1):
                        return True

                    # откат
                    board[i][j] = "."
                    rows[i][d] = cols[j][d] = boxes[box_id][d] = False

            return False

        backtrack(0)

''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks