'''
https://leetcode.com/problems/largest-rectangle-in-histogram/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
'''

class Solution(object):
    def largestRectangleArea(self, heights):
        """
        Решение задачи "Largest Rectangle in Histogram" (LeetCode 84).

        Задача:
        - Дан массив высот гистограммы.
        - Найти наибольшую площадь прямоугольника, который можно
          вписать в гистограмму.

        Идея:
        - Используем стек, который хранит индексы с возрастающими
          высотами.
        - Когда встречается меньшая высота, обрабатываем предыдущие
          "горизонтальные" прямоугольники.
        - Добавляем фиктивный 0 в конец для окончательной очистки стека.

        Сложность:
        - Время: O(n)
        - Память: O(n)
        """
        stack = []
        max_area = 0
        # Добавляем 0 в конец, чтобы "вычистить" стек до конца
        heights.append(0)

        for i, h in enumerate(heights):
            while stack and heights[stack[-1]] > h:
                height = heights[stack.pop()]
                width = i if not stack else i - stack[-1] - 1
                max_area = max(max_area, height * width)
            stack.append(i)

        return max_area
