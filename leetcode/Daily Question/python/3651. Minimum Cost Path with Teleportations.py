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

from collections import defaultdict

class Solution:
    def minCost(self, grid, k):
        """
        Находит минимальную стоимость пути от (0,0) до (m-1,n-1) с возможностью телепортации.
        
        Args:
            grid: Сетка m×n с целыми числами
            k: Максимальное количество телепортаций
            
        Returns:
            Минимальная стоимость пути
        """
        m, n = len(grid), len(grid[0])
        INF = float('inf')
        
        # f[t][i][j] = минимальная стоимость достижения (i,j) используя ровно t телепортаций
        f = [[[INF] * n for _ in range(m)] for _ in range(k + 1)]
        
        # Базовый случай: телепортации не используются
        f[0][0][0] = 0
        
        # Заполняем таблицу DP для 0 телепортаций (только обычные ходы)
        for i in range(m):
            for j in range(n):
                if i > 0:
                    f[0][i][j] = min(f[0][i][j], f[0][i-1][j] + grid[i][j])
                if j > 0:
                    f[0][i][j] = min(f[0][i][j], f[0][i][j-1] + grid[i][j])
        
        # Группируем клетки по их значениям для эффективной телепортации
        value_to_cells = defaultdict(list)
        for i in range(m):
            for j in range(n):
                value_to_cells[grid[i][j]].append((i, j))
        
        # Сортируем значения по убыванию
        sorted_values = sorted(value_to_cells.keys(), reverse=True)
        
        # Для каждого количества телепортаций
        for t in range(1, k + 1):
            min_cost = INF
            
            # Обрабатываем клетки в порядке убывания значений
            # Это гарантирует, что когда мы телепортируемся В клетку со значением v,
            # мы уже вычислили стоимости для всех клеток со значением >= v
            for val in sorted_values:
                cells = value_to_cells[val]
                
                # Обновляем min_cost клетками с текущим значением
                # Это потенциальные источники для телепортации
                for i, j in cells:
                    min_cost = min(min_cost, f[t-1][i][j])
                
                # Все клетки с этим значением можно достичь телепортацией
                # из любой клетки со значением >= этого значения используя t телепортаций
                for i, j in cells:
                    f[t][i][j] = min_cost
            
            # После телепортации можем делать обычные ходы
            for i in range(m):
                for j in range(n):
                    if i > 0:
                        f[t][i][j] = min(f[t][i][j], f[t][i-1][j] + grid[i][j])
                    if j > 0:
                        f[t][i][j] = min(f[t][i][j], f[t][i][j-1] + grid[i][j])
        
        # Возвращаем минимальную стоимость используя любое количество телепортаций (от 0 до k)
        return min(f[t][m-1][n-1] for t in range(k + 1))