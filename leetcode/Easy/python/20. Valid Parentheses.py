'''
https://leetcode.com/problems/valid-parentheses/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
'''

class Solution:
    def isValid(self, s):
        """
        Проверка корректности скобочной последовательности.
        
        Алгоритм:
        1. Используем стек для хранения открывающих скобок.
        2. При встрече закрывающей скобки проверяем,
           соответствует ли она верхнему элементу стека.
        3. В конце стек должен быть пуст — значит все скобки корректно закрыты.
        
        :param s: Строка, содержащая только '()[]{}'
        :return: True — если последовательность корректна, иначе False
        """
        stack = []
        mapping = {')': '(', ']': '[', '}': '{'}
        
        for char in s:
            if char in mapping.values():  # открывающая скобка
                stack.append(char)
            else:  # закрывающая скобка
                if not stack or stack.pop() != mapping[char]:
                    return False
        
        return not stack

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks