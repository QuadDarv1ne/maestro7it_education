"""
LeetCode 3047: Find the Largest Area of Square Inside Two Rectangles

Задача: Найти максимальную площадь квадрата, который можно поместить 
в пересечение двух прямоугольников.

Алгоритм:
1. Перебираем все пары прямоугольников O(n²)
2. Для каждой пары находим пересечение прямоугольников
3. В пересечении определяем максимальный квадрат (min из ширины и высоты)
4. Сохраняем максимальную площадь среди всех пар

Временная сложность: O(n²), где n - количество прямоугольников
Пространственная сложность: O(1)

Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Полезные ссылки:
- LeetCode задача: https://leetcode.com/problems/find-the-largest-area-of-square-inside-two-rectangles/
- Telegram канал: https://t.me/hut_programmer_07
- Rutube: https://rutube.ru/channel/4218729/
- YouTube: https://www.youtube.com/@it-coders
- ВКонтакте: https://vk.com/science_geeks
"""

# from typing import List


class Solution:
    def largestSquareArea(self, bottomLeft, topRight):
        """
        Находит максимальную площадь квадрата, который можно поместить 
        в пересечение двух прямоугольников.
        
        Args:
            bottomLeft: Массив координат левых нижних углов прямоугольников
            topRight: Массив координат правых верхних углов прямоугольников
            
        Returns:
            int: Максимальная площадь квадрата
            
        Examples:
            >>> solution = Solution()
            >>> solution.largestSquareArea([[1,1],[2,2],[3,1]], [[3,3],[4,4],[6,6]])
            1
            >>> solution.largestSquareArea([[1,1],[2,2],[1,2]], [[3,3],[4,4],[3,4]])
            1
            >>> solution.largestSquareArea([[1,1],[3,3],[3,1]], [[2,2],[4,4],[4,2]])
            0
        """
        n = len(bottomLeft)
        max_area = 0
        
        # Перебираем все пары прямоугольников
        for i in range(n - 1):
            for j in range(i + 1, n):
                # Находим пересечение по оси X
                x1 = max(bottomLeft[i][0], bottomLeft[j][0])
                x2 = min(topRight[i][0], topRight[j][0])
                
                # Находим пересечение по оси Y
                y1 = max(bottomLeft[i][1], bottomLeft[j][1])
                y2 = min(topRight[i][1], topRight[j][1])
                
                # Вычисляем ширину и высоту пересечения
                width = x2 - x1
                height = y2 - y1
                
                # Проверяем существование пересечения и обновляем максимум
                if width > 0 and height > 0:
                    side = min(width, height)
                    max_area = max(max_area, side * side)
        
        return max_area


# Альтернативное решение с использованием comprehension (более Pythonic)
class SolutionCompact:
    def largestSquareArea(self, bottomLeft, topRight):
        """
        Компактная версия решения с использованием list comprehension.
        
        Args:
            bottomLeft: Массив координат левых нижних углов прямоугольников
            topRight: Массив координат правых верхних углов прямоугольников
            
        Returns:
            int: Максимальная площадь квадрата
        """
        n = len(bottomLeft)
        
        def intersection_square_area(i, j):
            """Вычисляет площадь квадрата в пересечении двух прямоугольников."""
            width = min(topRight[i][0], topRight[j][0]) - max(bottomLeft[i][0], bottomLeft[j][0])
            height = min(topRight[i][1], topRight[j][1]) - max(bottomLeft[i][1], bottomLeft[j][1])
            
            if width > 0 and height > 0:
                side = min(width, height)
                return side * side
            return 0
        
        return max(
            (intersection_square_area(i, j) for i in range(n - 1) for j in range(i + 1, n)),
            default=0
        )