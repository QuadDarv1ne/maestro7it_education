'''
https://leetcode.com/problems/min-stack/description/
'''

class MinStack:
    def __init__(self):
        """
        Реализация стека с поддержкой получения минимума за O(1).
        stack — основной стек.
        min_stack — стек минимумов.
        """
        self.stack = []
        self.min_stack = []

    def push(self, val):
        """
        Добавить элемент в стек.
        В стек минимумов кладём минимальное из val и текущего минимума.
        """
        self.stack.append(val)
        if not self.min_stack or val <= self.min_stack[-1]:
            self.min_stack.append(val)
        else:
            self.min_stack.append(self.min_stack[-1])

    def pop(self):
        """
        Удалить верхний элемент из обоих стеков.
        """
        self.stack.pop()
        self.min_stack.pop()

    def top(self):
        """
        Получить верхний элемент основного стека.
        """
        return self.stack[-1]

    def getMin(self):
        """
        Получить текущий минимум.
        """
        return self.min_stack[-1]

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks