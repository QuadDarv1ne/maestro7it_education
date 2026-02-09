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
    def computeArea(self, ax1, ay1, ax2, ay2, 
                    bx1, by1, bx2, by2):
        """
        Вычисляет общую площадь, покрываемую двумя прямоугольниками.
        
        Алгоритм:
        1. Вычисляет площади каждого прямоугольника.
        2. Находит площадь пересечения прямоугольников (если оно есть).
        3. Возвращает сумму площадей минус площадь пересечения.
        
        Формула:
        Общая площадь = Площадь1 + Площадь2 - ПлощадьПересечения
        
        Сложность:
        Время: O(1)
        Пространство: O(1)
        
        Параметры:
        ----------
        ax1, ay1, ax2, ay2 : int
            Координаты первого прямоугольника:
            (ax1, ay1) - левый нижний угол
            (ax2, ay2) - правый верхний угол
        bx1, by1, bx2, by2 : int
            Координаты второго прямоугольника:
            (bx1, by1) - левый нижний угол
            (bx2, by2) - правый верхний угол
            
        Возвращает:
        -----------
        int
            Общая площадь, покрываемая двумя прямоугольниками
            
        Пример:
        -------
        Вход: ax1=-3, ay1=0, ax2=3, ay2=4, bx1=0, by1=-1, bx2=9, by2=2
        Площадь1 = 24, Площадь2 = 27, Пересечение = 6
        Выход: 24 + 27 - 6 = 45
        """
        # Вычисляем площади каждого прямоугольника
        area_a = (ax2 - ax1) * (ay2 - ay1)
        area_b = (bx2 - bx1) * (by2 - by1)
        
        # Находим координаты пересечения
        overlap_width = max(0, min(ax2, bx2) - max(ax1, bx1))
        overlap_height = max(0, min(ay2, by2) - max(ay1, by1))
        
        # Вычисляем площадь пересечения
        overlap_area = overlap_width * overlap_height
        
        # Общая площадь
        return area_a + area_b - overlap_area