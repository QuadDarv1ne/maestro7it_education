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

Определяет, можно ли разделить матрицу одним горизонтальным или вертикальным
разрезом на две непустые части с равной суммой элементов.

Параметры:
    grid (List[List[int]]): матрица положительных целых чисел размером m x n

Возвращает:
    bool: True, если существует разрез с равными суммами, иначе False

Примечания:
    - Разрез может быть горизонтальным (между строками) или вертикальным (между столбцами)
    - Обе части после разреза должны быть непустыми
    - Используется префиксная сумма для строк и столбцов
    - Сложность: O(m*n) по времени и O(1) дополнительной памяти

Пример:
    >>> grid = [[1,4],[2,3]]
    >>> equalSumGridPartition(grid)
    True
"""

class Solution(object):
    def canPartitionGrid(self, grid):
        total = 0
        m = len(grid)
        n = len(grid[0])
        
        # Вычисляем общую сумму всех элементов
        for i in range(m):
            for j in range(n):
                total += grid[i][j]
        
        # Если общая сумма нечётная, разделение невозможно
        if total % 2 != 0:
            return False
        
        target = total // 2
        
        # Проверяем горизонтальные разрезы
        row_sum = 0
        for i in range(m - 1):
            for j in range(n):
                row_sum += grid[i][j]
            if row_sum == target:
                return True
        
        # Проверяем вертикальные разрезы
        col_sum = 0
        for j in range(n - 1):
            for i in range(m):
                col_sum += grid[i][j]
            if col_sum == target:
                return True
        
        return False