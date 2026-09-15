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

# from typing import List

class Solution:
    def rotateTheBox(self, boxGrid):
        """
        Поворачивает матрицу и применяет гравитацию к камням.

        Сначала в каждой строке исходной матрицы камни ('#') сдвигаются вправо,
        упираясь в препятствия ('*') или другие камни. Затем матрица
        поворачивается на 90 градусов по часовой стрелке.

        Args:
            boxGrid: Список списков строк, представляющих исходную коробку.
                     Символы: '#' (камень), '*' (препятствие), '.' (пустота).

        Returns:
            Новая матрица после поворота и гравитации.
        """
        m = len(boxGrid)
        n = len(boxGrid[0])

        # Этап 1: Применить гравитацию в каждой строке (сдвиг камней вправо)
        for row in boxGrid:
            empty_pos = n - 1  # Позиция для следующего камня
            for col in range(n - 1, -1, -1):
                if row[col] == '*':
                    empty_pos = col - 1
                elif row[col] == '#':
                    # Меняем местами камень и пустое место
                    row[col], row[empty_pos] = row[empty_pos], row[col]
                    empty_pos -= 1

        # Этап 2: Повернуть матрицу на 90 градусов по часовой стрелке
        # Создаем матрицу размером n x m
        rotated_box = [[''] * m for _ in range(n)]
        for i in range(m):
            for j in range(n):
                rotated_box[j][m - 1 - i] = boxGrid[i][j]

        return rotated_box