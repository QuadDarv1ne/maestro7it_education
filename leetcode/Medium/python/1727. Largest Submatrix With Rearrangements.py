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
    def largestSubmatrix(self, matrix):
        if not matrix:
            return 0

        m, n = len(matrix), len(matrix[0])
        max_area = 0
        # heights[j] будет хранить количество последовательных 1 в столбце j до текущей строки
        heights = [0] * n

        for i in range(m):
            # Обновляем высоты для текущей строки
            for j in range(n):
                if matrix[i][j] == 1:
                    heights[j] += 1
                else:
                    heights[j] = 0

            # Создаем копию heights для текущей строки, чтобы отсортировать
            current_heights = heights[:]
            current_heights.sort(reverse=True)

            # Вычисляем максимальную площадь для этой строки
            for j in range(n):
                # current_heights[j] - это минимальная высота в прямоугольнике,
                # а (j + 1) столбцов имеют высоту >= current_heights[j] (так как сортировка по убыванию)
                max_area = max(max_area, current_heights[j] * (j + 1))

        return max_area