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

import threading

class FooBar:
    def __init__(self, n):
        self.n = n
        self.lock = threading.Condition()
        self.foo_turn = True

    def foo(self, printFoo):
        for i in range(self.n):
            with self.lock:
                while not self.foo_turn:
                    self.lock.wait()
                printFoo()
                self.foo_turn = False
                self.lock.notify()

    def bar(self, printBar):
        for i in range(self.n):
            with self.lock:
                while self.foo_turn:
                    self.lock.wait()
                printBar()
                self.foo_turn = True
                self.lock.notify()