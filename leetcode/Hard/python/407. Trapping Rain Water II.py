'''
https://leetcode.com/problems/trapping-rain-water-ii/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
'''

import heapq

class Solution(object):
    def trapRainWater(self, heightMap):
        """
        Решает задачу "Trapping Rain Water II" (LeetCode 407).

        Задача:
        Дана карта высот (матрица m x n). Нужно вычислить, сколько воды может быть
        собрано после дождя, если считать, что вода удерживается "ямами" внутри рельефа.

        Оптимизированное решение задачи:
        - Использует приоритетную очередь (min-heap).
        - Начинаем с внешних границ, постепенно "затягиваем" внутрь.
        - Если сосед ниже текущего уровня, вода добавляется.
        - Ускорение:
            • visited встроен прямо в heightMap заменой на -1 (экономия памяти).
            • меньше проверок и аллокаций.
        """
        if not heightMap or not heightMap[0]:
            return 0
        m, n = len(heightMap), len(heightMap[0])
        if m < 3 or n < 3:
            return 0

        heap = []
        # Помечаем границы как посещённые (-1)
        for i in range(m):
            heapq.heappush(heap, (heightMap[i][0], i, 0))
            heapq.heappush(heap, (heightMap[i][n-1], i, n-1))
            heightMap[i][0] = -1
            heightMap[i][n-1] = -1
        for j in range(1, n-1):
            heapq.heappush(heap, (heightMap[0][j], 0, j))
            heapq.heappush(heap, (heightMap[m-1][j], m-1, j))
            heightMap[0][j] = -1
            heightMap[m-1][j] = -1

        water, dirs = 0, ((1,0),(-1,0),(0,1),(0,-1))

        while heap:
            h, x, y = heapq.heappop(heap)
            for dx, dy in dirs:
                nx, ny = x + dx, y + dy
                if 0 <= nx < m and 0 <= ny < n and heightMap[nx][ny] != -1:
                    nh = heightMap[nx][ny]
                    if nh < h:
                        water += h - nh
                        heapq.heappush(heap, (h, nx, ny))
                    else:
                        heapq.heappush(heap, (nh, nx, ny))
                    heightMap[nx][ny] = -1
        return water

''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07 
# 2. Telegram №1 @quadd4rv1n7 
# 3. Telegram №2 @dupley_maxim_1999 
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
