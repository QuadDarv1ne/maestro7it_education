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
    def diffWaysToCompute(self, expression):
        """
        Вычисляет все возможные результаты расстановки скобок в арифметическом выражении.
        
        Алгоритм (разделяй и властвуй):
        1. Для каждого оператора в выражении:
           - Разделяем выражение на левую и правую части
           - Рекурсивно вычисляем результаты для левой части
           - Рекурсивно вычисляем результаты для правой части
           - Комбинируем результаты, применяя оператор
        2. Если в выражении нет операторов (только число), возвращаем это число
        
        Сложность:
        Время: O(C_n), где C_n - n-е каталонское число (количество способов расставить скобки)
        Пространство: O(C_n) для хранения результатов
        
        Параметры:
        ----------
        expression : str
            Строка с арифметическим выражением (например, "2-1-1")
            
        Возвращает:
        -----------
        List[int]
            Все возможные результаты вычисления выражения
            
        Примеры:
        --------
        diffWaysToCompute("2-1-1") → [0, 2]
        diffWaysToCompute("2*3-4*5") → [-34, -14, -10, -10, 10]
        """
        memo = {}  # Мемоизация для оптимизации
        
        def compute(expr):
            # Проверяем, есть ли результат в кэше
            if expr in memo:
                return memo[expr]
            
            # Если выражение - просто число
            if expr.isdigit():
                result = [int(expr)]
                memo[expr] = result
                return result
            
            results = []
            
            for i, char in enumerate(expr):
                # Если текущий символ - оператор
                if char in '+-*':
                    # Разделяем выражение на левую и правую части
                    left_results = compute(expr[:i])
                    right_results = compute(expr[i+1:])
                    
                    # Комбинируем результаты
                    for left in left_results:
                        for right in right_results:
                            if char == '+':
                                results.append(left + right)
                            elif char == '-':
                                results.append(left - right)
                            elif char == '*':
                                results.append(left * right)
            
            memo[expr] = results
            return results
        
        return compute(expression)
    
    def diffWaysToCompute_iterative(self, expression):
        """
        Итеративное решение с использованием динамического программирования.
        
        Алгоритм:
        1. Разбиваем выражение на числа и операторы
        2. Используем DP: dp[i][j] содержит все возможные результаты для подвыражения от i до j
        3. Заполняем диагонали таблицы DP
        
        Сложность:
        Время: O(n^3) в худшем случае
        Пространство: O(n^2) для таблицы DP
        """
        if not expression:
            return []
        
        # Разделяем выражение на числа и операторы
        nums = []
        ops = []
        num = 0
        
        for char in expression:
            if char.isdigit():
                num = num * 10 + int(char)
            else:
                nums.append(num)
                ops.append(char)
                num = 0
        nums.append(num)
        
        n = len(nums)
        
        # Инициализируем таблицу DP
        # dp[i][j] содержит все возможные результаты для подвыражения от i до j
        dp = [[[] for _ in range(n)] for _ in range(n)]
        
        # Заполняем диагональ (выражения из одного числа)
        for i in range(n):
            dp[i][i].append(nums[i])
        
        # Заполняем таблицу для подвыражений разной длины
        for length in range(2, n + 1):  # Длина подвыражения
            for i in range(n - length + 1):  # Начальный индекс
                j = i + length - 1  # Конечный индекс
                
                # Перебираем все возможные позиции операторов
                for k in range(i, j):
                    # Получаем результаты для левой и правой частей
                    left_results = dp[i][k]
                    right_results = dp[k+1][j]
                    op = ops[k]
                    
                    # Комбинируем результаты
                    for left in left_results:
                        for right in right_results:
                            if op == '+':
                                dp[i][j].append(left + right)
                            elif op == '-':
                                dp[i][j].append(left - right)
                            elif op == '*':
                                dp[i][j].append(left * right)
        
        return dp[0][n-1]