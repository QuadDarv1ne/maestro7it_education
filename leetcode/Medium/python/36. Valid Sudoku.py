'''
https://leetcode.com/problems/valid-sudoku/description/?envType=daily-question&envId=2025-08-30
'''

class Solution:
    def isValidSudoku(self, board):
        """
        Проверяет, является ли переданная Sudoku-доска (9x9) корректной.

        Условия корректности:
        1. В каждой строке цифры 1–9 не должны повторяться.
        2. В каждом столбце цифры 1–9 не должны повторяться.
        3. В каждом подблоке 3x3 цифры 1–9 не должны повторяться.
        Символ '.' обозначает пустую клетку и игнорируется.

        :param board: Список списков символов (строки Sudoku).
        :return: True, если доска корректна, иначе False.
        """
        rows = [[False]*9 for _ in range(9)]
        cols = [[False]*9 for _ in range(9)]
        boxes = [[False]*9 for _ in range(9)]
        
        for i in range(9):
            for j in range(9):
                c = board[i][j]
                if c == '.':
                    continue
                num = int(c) - 1
                box_idx = (i // 3) * 3 + (j // 3)
                if rows[i][num] or cols[j][num] or boxes[box_idx][num]:
                    return False
                rows[i][num] = cols[j][num] = boxes[box_idx][num] = True
        return True

''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks