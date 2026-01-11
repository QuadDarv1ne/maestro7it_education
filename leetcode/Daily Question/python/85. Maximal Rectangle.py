"""
Находит площадь максимального прямоугольника, состоящего из единиц

@param matrix: Бинарная матрица (из символов '0' и '1')
@return: Площадь максимального прямоугольника из единиц

Сложность: Время O(rows * cols), Память O(cols)

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
    def maximalRectangle(self, matrix):
        if not matrix or not matrix[0]:
            return 0
        
        rows = len(matrix)
        cols = len(matrix[0])
        max_area = 0
        
        # Массив высот для каждого столбца
        heights = [0] * cols
        
        for i in range(rows):
            # Обновляем высоты для текущей строки
            for j in range(cols):
                if matrix[i][j] == '1':
                    heights[j] += 1
                else:
                    heights[j] = 0
            
            # Находим максимальную площадь в гистограмме
            max_area = max(max_area, self._largest_rectangle_area(heights))
        
        return max_area
    
    def _largest_rectangle_area(self, heights):
        """Находит максимальную площадь прямоугольника в гистограмме"""
        n = len(heights)
        stack = []
        max_area = 0
        
        for i in range(n + 1):
            # Барьерное значение 0 в конце для обработки оставшихся элементов
            h = 0 if i == n else heights[i]
            
            # Пока стек не пуст и текущая высота меньше высоты в стеке
            while stack and h < heights[stack[-1]]:
                height = heights[stack.pop()]
                width = i if not stack else i - stack[-1] - 1
                max_area = max(max_area, height * width)
            
            stack.append(i)
        
        return max_area