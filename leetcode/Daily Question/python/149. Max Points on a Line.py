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

from fractions import Fraction
from collections import defaultdict

class Solution:
    """
    @brief Решение с использованием Fraction для точного представления наклона
    
    Преимущества:
    1. Автоматическая нормализация дробей
    2. Встроенная обработка бесконечного наклона (вертикальных линий)
    3. Более читаемый код
    
    Недостатки:
    1. Может быть медленнее из-за создания объектов Fraction
    2. Требует дополнительной памяти
    """
    def maxPoints(self, points):
        n = len(points)
        if n <= 2:
            return n
        
        max_points = 0
        
        for i in range(n):
            slope_count = defaultdict(int)
            same_point = 0
            current_max = 0
            
            for j in range(i + 1, n):
                x1, y1 = points[i]
                x2, y2 = points[j]
                
                if x1 == x2 and y1 == y2:
                    same_point += 1
                    continue
                
                if x1 == x2:
                    # Вертикальная линия
                    slope = float('inf')
                else:
                    # Вычисляем наклон как Fraction
                    slope = Fraction(y2 - y1, x2 - x1)
                
                slope_count[slope] += 1
                current_max = max(current_max, slope_count[slope])
            
            max_points = max(max_points, 1 + same_point + current_max)
        
        return max_points