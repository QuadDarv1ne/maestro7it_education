"""
https://leetcode.com/problems/longest-valid-parentheses/description/
Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
"""

class Solution:
    def longestValidParentheses(self, s):
        """
        Находит длину самой длинной валидной скобочной последовательности.
        
        Args:
            s: строка, содержащая только символы '(' и ')'
            
        Returns:
            Длина самой длинной правильной скобочной подстроки
        """
        if not s:
            return 0
        
        stack = [-1]  # Инициализируем стек с -1 как базовым индексом
        max_length = 0
        
        for i, char in enumerate(s):
            if char == '(':
                stack.append(i)
            else:
                # Удаляем последний элемент стека (это может быть индекс открывающей скобки)
                stack.pop()
                
                if not stack:
                    # Если стек пуст, добавляем текущий индекс как новую базовую точку
                    stack.append(i)
                else:
                    # Вычисляем длину валидной последовательности
                    current_length = i - stack[-1]
                    max_length = max(max_length, current_length)
        
        return max_length

    def longestValidParentheses_dp(self, s):
        """
        Решение с использованием динамического программирования.
        Более эффективно по памяти в некоторых случаях.
        """
        if not s:
            return 0
        
        n = len(s)
        dp = [0] * n  # dp[i] хранит длину валидной последовательности, заканчивающейся в i
        max_length = 0
        
        for i in range(1, n):
            if s[i] == ')':
                if s[i-1] == '(':
                    # Случай: ...()
                    dp[i] = (dp[i-2] if i >= 2 else 0) + 2
                elif i - dp[i-1] > 0 and s[i - dp[i-1] - 1] == '(':
                    # Случай: ...((...))
                    prev_length = dp[i - dp[i-1] - 2] if i - dp[i-1] >= 2 else 0
                    dp[i] = dp[i-1] + prev_length + 2
                
                max_length = max(max_length, dp[i])
        
        return max_length

    def longestValidParentheses_two_pass(self, s):
        """
        Решение с двумя проходами (слева направо и справа налево).
        Не требует дополнительной памяти кроме счетчиков.
        """
        max_length = 0
        
        # Проход слева направо
        left = right = 0
        for char in s:
            if char == '(':
                left += 1
            else:
                right += 1
            
            if left == right:
                max_length = max(max_length, 2 * right)
            elif right > left:
                left = right = 0
        
        # Проход справа налево
        left = right = 0
        for char in reversed(s):
            if char == '(':
                left += 1
            else:
                right += 1
            
            if left == right:
                max_length = max(max_length, 2 * left)
            elif left > right:
                left = right = 0
        
        return max_length
    
''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
