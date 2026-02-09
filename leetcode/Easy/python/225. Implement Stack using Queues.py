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

from collections import deque

class MyStack:
    """
    Реализация стека с использованием двух очередей.
    
    Алгоритм (подход 2 - дорогой push):
    - Используем две очереди: main_queue и temp_queue
    - Операция push:
        1. Добавляем новый элемент в temp_queue
        2. Перемещаем все элементы из main_queue в temp_queue
        3. Меняем очереди местами
    - Операции pop и top: работают с main_queue
    
    Сложность операций:
    - push: O(n)
    - pop: O(1)
    - top: O(1)
    - empty: O(1)
    
    Пример:
    ------
    stack = MyStack()
    stack.push(1)  # main_queue: [1]
    stack.push(2)  # temp_queue: [2], затем [2, 1], меняем местами
    stack.top()    # возвращает 2
    stack.pop()    # возвращает 2, main_queue: [1]
    """
    
    def __init__(self):
        """Инициализирует стек с двумя пустыми очередями."""
        self.main_queue = deque()
        self.temp_queue = deque()

    def push(self, x):
        """
        Помещает элемент x на вершину стека.
        
        Параметры:
        ----------
        x : int
            Элемент для добавления в стек
        """
        # Добавляем новый элемент во временную очередь
        self.temp_queue.append(x)
        
        # Перемещаем все элементы из основной очереди во временную
        while self.main_queue:
            self.temp_queue.append(self.main_queue.popleft())
        
        # Меняем очереди местами
        self.main_queue, self.temp_queue = self.temp_queue, self.main_queue

    def pop(self):
        """
        Удаляет элемент с вершины стека и возвращает его.
        
        Возвращает:
        -----------
        int
            Элемент с вершины стека
            
        Исключения:
        -----------
        ValueError
            Если стек пуст
        """
        if self.empty():
            raise ValueError("Stack is empty")
        return self.main_queue.popleft()

    def top(self):
        """
        Возвращает элемент на вершине стека без удаления.
        
        Возвращает:
        -----------
        int
            Элемент на вершине стека
            
        Исключения:
        -----------
        ValueError
            Если стек пуст
        """
        if self.empty():
            raise ValueError("Stack is empty")
        return self.main_queue[0]

    def empty(self):
        """
        Проверяет, пуст ли стек.
        
        Возвращает:
        -----------
        bool
            True, если стек пуст, иначе False
        """
        return len(self.main_queue) == 0


# Альтернативная реализация (дорогой pop)
class MyStackAlternative:
    """
    Альтернативная реализация стека с дорогой операцией pop.
    
    Алгоритм:
    - push: O(1) - просто добавляем в queue1
    - pop: O(n) - перемещаем n-1 элементов из queue1 в queue2,
                 извлекаем последний элемент из queue1,
                 меняем очереди местами
    """
    
    def __init__(self):
        self.queue1 = deque()
        self.queue2 = deque()

    def push(self, x):
        """Добавляет элемент в стек."""
        self.queue1.append(x)

    def pop(self):
        """Удаляет и возвращает элемент с вершины стека."""
        if self.empty():
            raise ValueError("Stack is empty")
        
        # Перемещаем все элементы, кроме последнего, во вторую очередь
        while len(self.queue1) > 1:
            self.queue2.append(self.queue1.popleft())
        
        # Получаем последний элемент
        result = self.queue1.popleft()
        
        # Меняем очереди местами
        self.queue1, self.queue2 = self.queue2, self.queue1
        
        return result

    def top(self):
        """Возвращает элемент с вершины стека без удаления."""
        if self.empty():
            raise ValueError("Stack is empty")
        
        # Копируем элементы для поиска последнего
        result = None
        while self.queue1:
            result = self.queue1.popleft()
            self.queue2.append(result)
        
        # Меняем очереди местами
        self.queue1, self.queue2 = self.queue2, self.queue1
        
        return result

    def empty(self):
        """Проверяет, пуст ли стек."""
        return len(self.queue1) == 0