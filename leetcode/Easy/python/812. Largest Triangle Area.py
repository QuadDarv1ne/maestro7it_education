'''
https://leetcode.com/problems/largest-triangle-area/description/?envType=daily-question&envId=2025-09-27
'''

class Solution:
    def largestTriangleArea(self, points):
        """
        Возвращает максимальную площадь треугольника, который можно составить из трёх точек.
        Использует формулу через векторное произведение (cross product) и полный перебор.
        """
        n = len(points)
        ans = 0.0
        for i in range(n):
            x1, y1 = points[i]
            for j in range(i + 1, n):
                x2, y2 = points[j]
                for k in range(j + 1, n):
                    x3, y3 = points[k]
                    # вектор из A в B: (x2-x1, y2-y1)
                    # вектор из A в C: (x3-x1, y3-y1)
                    cross = (x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1)
                    area = abs(cross) / 2.0
                    if area > ans:
                        ans = area
        return ans

''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks