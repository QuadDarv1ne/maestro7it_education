'''
https://leetcode.com/problems/number-of-islands/description/
'''

class Solution:
    def numIslands(self, grid):
        """
        Считает количество островов на карте.

        Алгоритм:
        1. Пробегаем по всем клеткам grid.
        2. Если встречаем '1' (земля), увеличиваем счетчик островов.
        3. Запускаем DFS, чтобы пометить все смежные клетки как посещённые ('0').
        4. DFS рекурсивно проходит вверх, вниз, влево и вправо.

        :param grid: двумерный массив символов '1' и '0'
        :return: количество островов
        """
        if not grid or not grid[0]:
            return 0
        
        rows, cols = len(grid), len(grid[0])
        count = 0
        
        def dfs(i, j):
            if i < 0 or i >= rows or j < 0 or j >= cols or grid[i][j] == '0':
                return
            grid[i][j] = '0'  # помечаем клетку как посещённую
            dfs(i+1, j)
            dfs(i-1, j)
            dfs(i, j+1)
            dfs(i, j-1)
        
        for i in range(rows):
            for j in range(cols):
                if grid[i][j] == '1':
                    count += 1
                    dfs(i, j)
        
        return count

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks