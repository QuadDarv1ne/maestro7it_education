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
    def calculate(self, s):
        """
        Вычисляет значение арифметического выражения без скобок.
        
        Алгоритм:
        1. Используем стек для хранения промежуточных результатов.
        2. Проходим по строке, собирая числа и обрабатывая операторы.
        3. Операторы * и / обрабатываются немедленно.
        4. Операторы + и - откладываются на потом (числа помещаются в стек с соответствующим знаком).
        5. В конце суммируем все элементы стека.
        
        Сложность:
        Время: O(n), где n - длина строки
        Пространство: O(n) для стека в худшем случае
        
        Параметры:
        ----------
        s : str
            Строка с арифметическим выражением
            
        Возвращает:
        -----------
        int
            Результат вычисления выражения
            
        Примеры:
        --------
        calculate("3+2*2") → 7
        calculate(" 3/2 ") → 1
        calculate(" 3+5 / 2 ") → 5
        """
        if not s:
            return 0
        
        stack = []
        num = 0
        sign = '+'  # Текущий оператор перед числом
        n = len(s)
        
        for i in range(n):
            ch = s[i]
            
            # Если символ - цифра, собираем число
            if ch.isdigit():
                num = num * 10 + int(ch)
            
            # Если символ - оператор или последний символ
            if (not ch.isdigit() and ch != ' ') or i == n - 1:
                if sign == '+':
                    stack.append(num)
                elif sign == '-':
                    stack.append(-num)
                elif sign == '*':
                    stack.append(stack.pop() * num)
                elif sign == '/':
                    # Целочисленное деление с округлением к нулю
                    top = stack.pop()
                    # Для Python: // округляет вниз, но нам нужно к нулю
                    if top < 0:
                        stack.append(-(abs(top) // num))
                    else:
                        stack.append(top // num)
                
                # Сбрасываем число и обновляем оператор
                num = 0
                sign = ch
        
        # Суммируем все элементы в стеке
        return sum(stack)