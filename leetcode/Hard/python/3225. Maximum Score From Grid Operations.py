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
    def maximumScore(self, grid):
        """
        Вычисляет максимальный счет после выполнения операций закрашивания столбцов.
        Операция: можно выбрать клетку (i, j) и закрасить все клетки в столбце j
        от верхней строки до i-й строки. Счет: сумма значений белых клеток,
        у которых есть горизонтальный сосед, закрашенный черным.
        Используется динамическое программирование с префиксными суммами столбцов.
        """
        n = len(grid)
        # prefix[j][i] — сумма первых i элементов (строк 0..i-1) в столбце j
        prefix = [[0] * (n + 1) for _ in range(n)]
        for j in range(n):
            for i in range(n):
                prefix[j][i + 1] = prefix[j][i] + grid[i][j]

        # prevPick[i] — макс. счет для предыдущего столбца, где высота черного столбца = i
        # prevSkip[i] — макс. счет для столбца перед предыдущим, где высота = i
        prevPick = [0] * (n + 1)
        prevSkip = [0] * (n + 1)

        # Обрабатываем столбцы начиная со второго, т.к. первый столбец не имеет соседа слева
        for j in range(1, n):
            currPick = [0] * (n + 1)
            currSkip = [0] * (n + 1)
            for curr in range(n + 1):      # высота текущего столбца j
                for prev in range(n + 1):  # высота предыдущего столбца j-1
                    if curr > prev:
                        # Случай: текущая высота больше предыдущей.
                        # Добавляем счет из предыдущего столбца (j-1) в диапазоне [prev, curr)
                        score = prefix[j - 1][curr] - prefix[j - 1][prev]
                        currPick[curr] = max(currPick[curr], prevSkip[prev] + score)
                        currSkip[curr] = max(currSkip[curr], prevSkip[prev] + score)
                    else:
                        # Случай: предыдущая высота больше или равна текущей.
                        # Добавляем счет из текущего столбца (j) в диапазоне [curr, prev)
                        score = prefix[j][prev] - prefix[j][curr]
                        currPick[curr] = max(currPick[curr], prevPick[prev] + score)
                        currSkip[curr] = max(currSkip[curr], prevPick[prev])
            prevPick = currPick
            prevSkip = currSkip

        # Ответ — максимальное значение среди всех возможных высот последнего столбца
        return max(prevPick)