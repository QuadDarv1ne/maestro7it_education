'''
https://leetcode.com/problems/count-covered-buildings/?envType=daily-question&envId=2025-12-11

Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Решение задачи "Count Covered Buildings"

Подход:
1. Для строк и столбцов находим min/max координаты
2. Для каждого здания проверяем, есть ли здания
   по всем четырём направлениям
'''

class Solution:
    def countCoveredBuildings(self, n: int, buildings: List[List[int]]) -> int:
        row_min = {}
        row_max = {}
        col_min = {}
        col_max = {}

        # Собираем границы
        for x, y in buildings:
            if x not in row_min:
                row_min[x] = y
                row_max[x] = y
            else:
                row_min[x] = min(row_min[x], y)
                row_max[x] = max(row_max[x], y)

            if y not in col_min:
                col_min[y] = x
                col_max[y] = x
            else:
                col_min[y] = min(col_min[y], x)
                col_max[y] = max(col_max[y], x)

        ans = 0
        for x, y in buildings:
            if row_min[x] < y < row_max[x] and col_min[y] < x < col_max[y]:
                ans += 1

        return ans
