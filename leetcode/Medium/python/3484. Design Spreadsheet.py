'''
https://leetcode.com/problems/design-spreadsheet/description/?envType=daily-question&envId=2025-09-19
'''

class Spreadsheet:
    """
    Класс Spreadsheet — простая реализация электронной таблицы.

    Атрибуты:
        rows: количество строк
        grid: данные таблицы (rows x 26)

    Методы:
        setCell(cell, value):
            Устанавливает значение в ячейку (например, "A1" = 5).
        resetCell(cell):
            Сбрасывает значение ячейки (устанавливает 0).
        getValue(formula):
            Вычисляет выражение вида "=X+Y", где X и Y — ссылки на ячейки или числа.
    """

    def __init__(self, rows):
        self.rows = rows
        self.grid = [[0] * 26 for _ in range(rows)]

    def _parse_cell(self, cell):
        col = ord(cell[0]) - ord('A')
        row = int(cell[1:]) - 1
        return row, col

    def _value_from_token(self, tok):
        if tok and tok[0].isupper():
            r, c = self._parse_cell(tok)
            return self.grid[r][c]
        else:
            return int(tok)

    def setCell(self, cell, value):
        """Установить значение в указанную ячейку"""
        r, c = self._parse_cell(cell)
        self.grid[r][c] = value

    def resetCell(self, cell):
        """Сбросить значение ячейки (установить 0)"""
        r, c = self._parse_cell(cell)
        self.grid[r][c] = 0

    def getValue(self, formula):
        """Вычислить значение формулы вида "=X+Y" """
        expr = formula[1:]
        a, b = expr.split('+')
        return self._value_from_token(a) + self._value_from_token(b)

''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
