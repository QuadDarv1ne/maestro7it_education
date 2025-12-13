'''
https://leetcode.com/problems/maximal-rectangle/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
'''

class Solution(object):
    def maximalRectangle(self, matrix):
        """
        Решение задачи "Maximal Rectangle" (LeetCode 85).

        Задача:
        - Дан бинарный матриц matrix размером m×n.
        - Найти максимальную прямоугольную область,
          заполненную только '1'.

        Идея:
        - Представляем каждую строку как основание
          гистограммы высот.
        - Для каждой строки считаем максимальную площадь
          прямоугольника (как в LeetCode 84).
        - Поддерживаем массив высот heights,
          обновляем его для каждой строки:
            heights[j] = heights[j] + 1 если '1', иначе 0.

        Сложность:
        - Время: O(m·n)
        - Память: O(n)
        """
        if not matrix:
            return 0
        
        max_area = 0
        n = len(matrix[0])
        heights = [0] * n
        
        for row in matrix:
            for i in range(n):
                heights[i] = heights[i] + 1 if row[i] == '1' else 0
            
            # Наибольшая площадь для текущих высот
            max_area = max(max_area, self.largestRectangleArea(heights))
        
        return max_area

    def largestRectangleArea(self, heights):
        stack = []
        max_area = 0
        heights.append(0)
        
        for i, h in enumerate(heights):
            while stack and heights[stack[-1]] > h:
                height = heights[stack.pop()]
                width = i if not stack else i - stack[-1] - 1
                max_area = max(max_area, height * width)
            stack.append(i)
        
        heights.pop()
        return max_area
