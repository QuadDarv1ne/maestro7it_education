"""
LeetCode: Evaluate Reverse Polish Notation
https://leetcode.com/problems/evaluate-reverse-polish-notation/

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
    def evalRPN(self, tokens):
        """
        Итоговое оптимизированное решение.
        
        Преимущества:
        1. Минимальный код (15 строк)
        2. Ясная логика
        3. Корректная обработка деления с округлением к нулю
        4. O(n) время, O(n) память
        """
        stack = []
        
        for token in tokens:
            if token == '+':
                stack.append(stack.pop() + stack.pop())
            elif token == '-':
                b, a = stack.pop(), stack.pop()
                stack.append(a - b)
            elif token == '*':
                stack.append(stack.pop() * stack.pop())
            elif token == '/':
                b, a = stack.pop(), stack.pop()
                stack.append(int(a / b))  # Ключевая оптимизация!
            else:
                stack.append(int(token))
        
        return stack[0]