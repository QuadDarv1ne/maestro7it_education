'''
https://leetcode.com/problems/implement-queue-using-stacks/description/
'''

class MyQueue:
    def __init__(self):
        """
        Инициализация: два стека —
        in_stack для добавления,
        out_stack для удаления/просмотра.
        """
        self.in_stack = []
        self.out_stack = []

    def push(self, x):
        """
        Записываем элемент в in_stack.
        """
        self.in_stack.append(x)

    def pop(self):
        """
        Если out_stack пуст, переносим в него все из in_stack.
        Затем возвращаем верх из out_stack.
        """
        if not self.out_stack:
            while self.in_stack:
                self.out_stack.append(self.in_stack.pop())
        return self.out_stack.pop()

    def peek(self):
        """
        То же, что и pop, но без удаления — возвращаем верх из out_stack.
        """
        if not self.out_stack:
            while self.in_stack:
                self.out_stack.append(self.in_stack.pop())
        return self.out_stack[-1]

    def empty(self):
        """
        Проверяем, пусты ли оба стека.
        """
        return not self.in_stack and not self.out_stack

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks