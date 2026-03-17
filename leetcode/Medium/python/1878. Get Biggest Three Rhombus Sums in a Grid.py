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
    def getBiggestThree(self, grid):
        m, n = len(grid), len(grid[0])
        # Используем список для хранения топ-3 уникальных сумм
        top_sums = []

        # Перебираем все возможные центры ромбов
        for i in range(m):
            for j in range(n):
                # Добавляем сумму для ромба размера 1 (одна ячейка)
                val = grid[i][j]
                if val not in top_sums:
                    top_sums.append(val)
                    top_sums.sort(reverse=True)
                    if len(top_sums) > 3:
                        top_sums.pop()

                # Перебираем возможные размеры ромба k (начиная с 2)
                # Размер k определяет, что сторона содержит k ячеек, а всего ячеек по диагонали 2k-1
                max_k = min(i, m - 1 - i, j, n - 1 - j) + 1 # Максимальная "полудиагональ"
                for k in range(2, max_k + 1):
                    # Вычисляем координаты четырех вершин
                    # Верхняя вершина
                    r1, c1 = i - (k - 1), j
                    # Правая вершина
                    r2, c2 = i, j + (k - 1)
                    # Нижняя вершина
                    r3, c3 = i + (k - 1), j
                    # Левая вершина
                    r4, c4 = i, j - (k - 1)

                    # Проверка границ (хотя max_k уже гарантирует)
                    if not (0 <= r1 < m and 0 <= c1 < n and
                            0 <= r2 < m and 0 <= c2 < n and
                            0 <= r3 < m and 0 <= c3 < n and
                            0 <= r4 < m and 0 <= c4 < n):
                        continue

                    # Вычисляем сумму границы
                    total = 0
                    # Идем от верхней вершины к правой (вниз-вправо)
                    for step in range(k - 1):
                        total += grid[r1 + step][c1 + step]
                    # От правой к нижней (вниз-влево)
                    for step in range(k - 1):
                        total += grid[r2 + step][c2 - step]
                    # От нижней к левой (вверх-влево)
                    for step in range(k - 1):
                        total += grid[r3 - step][c3 - step]
                    # От левой к верхней (вверх-вправо)
                    for step in range(k - 1):
                        total += grid[r4 - step][c4 + step]

                    # Добавляем сумму в топ-3, если она уникальна
                    if total not in top_sums:
                        top_sums.append(total)
                        top_sums.sort(reverse=True)
                        if len(top_sums) > 3:
                            top_sums.pop()

        return top_sums