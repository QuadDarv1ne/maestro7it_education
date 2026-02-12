'''
https://leetcode.com/problems/print-in-order/description/
Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Решение задачи "1114. Print in Order"

Полезные ссылки:
1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
2. Telegram №1 @quadd4rv1n7
3. Telegram №2 @dupley_maxim_1999
4. Rutube канал: https://rutube.ru/channel/4218729/
5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
6. YouTube канал: https://www.youtube.com/@it-coders
7. ВК группа: https://vk.com/science_geeks
'''

from threading import Event

class Foo:
    """
    Класс для управления порядком выполнения трёх методов в разных потоках.

    Атрибуты:
        event1 (Event): Сигнал о завершении метода first().
        event2 (Event): Сигнал о завершении метода second().
    """

    def __init__(self):
        """Инициализирует два события в несигнальном состоянии."""
        self.event1 = Event()
        self.event2 = Event()

    def first(self, printFirst):
        """
        Выполняет первую функцию и подаёт сигнал о завершении.
        Блокировок не содержит — всегда выполняется немедленно.

        Аргументы:
            printFirst: функция, выводящая "first".
        """
        printFirst()
        self.event1.set()

    def second(self, printSecond):
        """
        Ожидает сигнал от first(), затем выполняет свою функцию
        и подаёт сигнал для third().

        Аргументы:
            printSecond: функция, выводящая "second".
        """
        self.event1.wait()
        printSecond()
        self.event2.set()

    def third(self, printThird):
        """
        Ожидает сигнал от second(), затем выполняет свою функцию.

        Аргументы:
            printThird: функция, выводящая "third".
        """
        self.event2.wait()
        printThird()