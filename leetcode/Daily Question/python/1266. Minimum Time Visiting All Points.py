"""
Находит минимальное время для посещения всех точек в заданном порядке

@param points: Список точек в формате [x, y] в порядке посещения
@return: Минимальное время для посещения всех точек

Сложность: Время O(n), Память O(1)

Автор: Дуплей Максим Игоревич
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

# from typing import List

class Solution:
    def minTimeToVisitAllPoints(self, points):
        total_time = 0
        
        # Проходим по всем соседним парам точек
        for i in range(len(points) - 1):
            dx = abs(points[i + 1][0] - points[i][0])
            dy = abs(points[i + 1][1] - points[i][1])
            
            # Минимальное время между точками - максимум из разностей координат
            total_time += max(dx, dy)
        
        return total_time