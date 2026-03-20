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

"""
Находит для каждой подматрицы размера k x k минимальную абсолютную разность
между любыми двумя различными значениями внутри этой подматрицы.

Параметры:
    grid (List[List[int]]): Исходная матрица размером m x n.
    k (int): Размер стороны квадратной подматрицы.

Возвращает:
    List[List[int]]: Матрица ans размером (m - k + 1) x (n - k + 1),
                     где ans[i][j] содержит минимальную абсолютную разность
                     для подматрицы с верхним левым углом (i, j).

Алгоритм:
    1. Перебираем все возможные позиции верхнего левого угла подматрицы.
    2. Для каждой позиции собираем все уникальные значения внутри подматрицы.
    3. Если все значения одинаковы (одно уникальное число) → ответ 0.
    4. Сортируем уникальные значения и находим минимальную разность между соседними.
    5. Сохраняем результат в соответствующую ячейку.

Сложность:
    Время: O(m * n * k² * log k)
    Память: O(k²)
"""

# from typing import List

class Solution:
    def minAbsDiff(self, grid, k):
        m, n = len(grid), len(grid[0])
        rows, cols = m - k + 1, n - k + 1
        result = [[0] * cols for _ in range(rows)]
        
        for i in range(rows):
            for j in range(cols):
                # Собираем все значения в текущей подматрице
                values = set()
                for x in range(i, i + k):
                    for y in range(j, j + k):
                        values.add(grid[x][y])
                
                # Если все элементы одинаковы
                if len(values) == 1:
                    result[i][j] = 0
                    continue
                
                # Сортируем уникальные значения
                sorted_vals = sorted(values)
                
                # Ищем минимальную разность между соседями
                min_diff = float('inf')
                for idx in range(1, len(sorted_vals)):
                    diff = sorted_vals[idx] - sorted_vals[idx - 1]
                    if diff < min_diff:
                        min_diff = diff
                
                result[i][j] = min_diff
        
        return result