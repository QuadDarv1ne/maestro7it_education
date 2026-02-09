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

# from typing import List

class Solution:
    def searchMatrix(self, matrix, target):
        """
        Проверяет, содержится ли целевое значение в отсортированной матрице.
        
        Алгоритм (поиск из правого верхнего угла):
        1. Начинаем с правого верхнего угла матрицы (row=0, col=n-1).
        2. Сравниваем текущий элемент с целевым значением:
           - Если matrix[row][col] == target: возвращаем True
           - Если matrix[row][col] > target: двигаемся влево (col -= 1)
           - Если matrix[row][col] < target: двигаемся вниз (row += 1)
        3. Повторяем, пока не выйдем за границы матрицы.
        
        Сложность:
        Время: O(m + n), где m - количество строк, n - количество столбцов
        Пространство: O(1)
        
        Параметры:
        ----------
        matrix : List[List[int]]
            Двумерная матрица, отсортированная по строкам и столбцам
        target : int
            Искомое значение
            
        Возвращает:
        -----------
        bool
            True, если target найден в матрице, иначе False
            
        Примеры:
        --------
        Матрица:
        [
          [1,   4,  7, 11, 15],
          [2,   5,  8, 12, 19],
          [3,   6,  9, 16, 22],
          [10, 13, 14, 17, 24],
          [18, 21, 23, 26, 30]
        ]
        
        searchMatrix(matrix, 5) → True
        searchMatrix(matrix, 20) → False
        """
        if not matrix or not matrix[0]:
            return False
        
        m, n = len(matrix), len(matrix[0])
        # Начинаем с правого верхнего угла
        row, col = 0, n - 1
        
        while row < m and col >= 0:
            current = matrix[row][col]
            if current == target:
                return True
            elif current > target:
                # Текущий элемент слишком большой, двигаемся влево
                col -= 1
            else:
                # Текущий элемент слишком маленький, двигаемся вниз
                row += 1
        
        return False
    
    def searchMatrix_from_left_bottom(self, matrix, target):
        """
        Альтернативная реализация: поиск из левого нижнего угла.
        
        Алгоритм:
        1. Начинаем с левого нижнего угла (row=m-1, col=0).
        2. Сравниваем текущий элемент с целевым значением:
           - Если matrix[row][col] == target: возвращаем True
           - Если matrix[row][col] > target: двигаемся вверх (row -= 1)
           - Если matrix[row][col] < target: двигаемся вправо (col += 1)
        3. Повторяем, пока не выйдем за границы матрицы.
        """
        if not matrix or not matrix[0]:
            return False
        
        m, n = len(matrix), len(matrix[0])
        # Начинаем с левого нижнего угла
        row, col = m - 1, 0
        
        while row >= 0 and col < n:
            current = matrix[row][col]
            if current == target:
                return True
            elif current > target:
                # Текущий элемент слишком большой, двигаемся вверх
                row -= 1
            else:
                # Текущий элемент слишком маленький, двигаемся вправо
                col += 1
        
        return False