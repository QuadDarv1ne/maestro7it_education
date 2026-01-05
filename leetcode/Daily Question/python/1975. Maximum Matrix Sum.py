'''
https://leetcode.com/problems/maximum-matrix-sum/
Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Решение задачи "Maximum Matrix Sum"

Полезные ссылки:
1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
2. Telegram №1 @quadd4rv1n7
3. Telegram №2 @dupley_maxim_1999
4. Rutube канал: https://rutube.ru/channel/4218729/
5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
6. YouTube канал: https://www.youtube.com/@it-coders
7. ВК группа: https://vk.com/science_geeks
'''

# from typing import List

class Solution:
    def maxMatrixSum(self, matrix):
        """
        Находит максимальную сумму матрицы после применения операций умножения -1
        на две соседние ячейки (по горизонтали или вертикали).
        
        Args:
            matrix: квадратная матрица целых чисел
            
        Returns:
            Максимально возможная сумма всех элементов матрицы
            
        Алгоритм:
        1. Суммируем абсолютные значения всех элементов
        2. Находим минимальное абсолютное значение
        3. Считаем количество отрицательных элементов
        4. Проверяем наличие нуля
        5. Если есть ноль или четное количество отрицательных элементов, 
           можно сделать все элементы положительными
        6. Иначе нужно вычесть дважды минимальное абсолютное значение
        """
        n = len(matrix)
        
        # Если матрица 1x1, просто возвращаем значение
        if n == 1:
            return matrix[0][0]
        
        total_abs_sum = 0      # Сумма абсолютных значений
        min_abs = float('inf') # Минимальное абсолютное значение
        negative_count = 0     # Количество отрицательных элементов
        has_zero = False       # Наличие нуля
        
        # Проходим по всем элементам матрицы
        for i in range(n):
            for j in range(n):
                value = matrix[i][j]
                abs_value = abs(value)
                
                total_abs_sum += abs_value
                
                # Обновляем минимальное абсолютное значение
                if abs_value < min_abs:
                    min_abs = abs_value
                
                # Считаем отрицательные элементы
                if value < 0:
                    negative_count += 1
                
                # Проверяем наличие нуля
                if value == 0:
                    has_zero = True
        
        # Если есть ноль или четное количество отрицательных элементов,
        # можно сделать все элементы положительными
        if has_zero or negative_count % 2 == 0:
            return total_abs_sum
        
        # Иначе нужно сделать один элемент отрицательным
        # Выбираем элемент с минимальным абсолютным значением
        return total_abs_sum - 2 * min_abs