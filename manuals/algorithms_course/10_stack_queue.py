"""
СТЕК И ОЧЕРЕДЬ (STACK AND QUEUE)

Стек и очередь — базовые абстрактные типы данных (ADT),
определяющие порядок доступа к элементам.

СТЕК (Stack) — LIFO (Last In, First Out)
Последний вошедший элемент выходит первым.
Аналогия: стопка тарелок.

Основные операции:
- push(x): добавить элемент на вершину стека
- pop(): удалить и вернуть верхний элемент
- peek(): вернуть верхний элемент без удаления
- is_empty(): проверка на пустоту

ОЧЕРЕДЬ (Queue) — FIFO (First In, First Out)
Первый вошедший элемент выходит первым.
Аналогия: очередь в магазине.

Основные операции:
- enqueue(x): добавить элемент в конец очереди
- dequeue(): удалить и вернуть первый элемент
- front(): вернуть первый элемент без удаления
- is_empty(): проверка на пустоту

Применение стека:
- Проверка сбалансированности скобок
- Обратная польская запись
- Отмена действий (Undo)
- Рекурсия (стек вызовов)

Применение очереди:
- BFS в графах
- Буферизация данных
- Планирование задач
- Обработка запросов
"""


# ===== РЕАЛИЗАЦИЯ СТЕКА =====

class Stack:
    """
    Реализация стека на основе списка Python.
    
    Пример:
        >>> s = Stack()
        >>> s.push(1)
        >>> s.push(2)
        >>> s.pop()
        2
    """
    
    def __init__(self):
        self._items = []
    
    def push(self, item):
        """Добавить элемент на вершину стека. O(1)"""
        self._items.append(item)
    
    def pop(self):
        """Удалить и вернуть верхний элемент. O(1)"""
        if self.is_empty():
            raise IndexError("Стек пуст")
        return self._items.pop()
    
    def peek(self):
        """Вернуть верхний элемент без удаления. O(1)"""
        if self.is_empty():
            raise IndexError("Стек пуст")
        return self._items[-1]
    
    def is_empty(self):
        """Проверить, пуст ли стек. O(1)"""
        return len(self._items) == 0
    
    def size(self):
        """Вернуть размер стека. O(1)"""
        return len(self._items)
    
    def __len__(self):
        return self.size()
    
    def __repr__(self):
        return f"Stack({self._items})"


# ===== РЕАЛИЗАЦИЯ ОЧЕРЕДИ =====

from collections import deque

class Queue:
    """
    Реализация очереди на основе collections.deque.
    
    Deque обеспечивает O(1) для операций с обоих концов.
    
    Пример:
        >>> q = Queue()
        >>> q.enqueue(1)
        >>> q.enqueue(2)
        >>> q.dequeue()
        1
    """
    
    def __init__(self):
        self._items = deque()
    
    def enqueue(self, item):
        """Добавить элемент в конец очереди. O(1)"""
        self._items.append(item)
    
    def dequeue(self):
        """Удалить и вернуть первый элемент. O(1)"""
        if self.is_empty():
            raise IndexError("Очередь пуста")
        return self._items.popleft()
    
    def front(self):
        """Вернуть первый элемент без удаления. O(1)"""
        if self.is_empty():
            raise IndexError("Очередь пуста")
        return self._items[0]
    
    def is_empty(self):
        """Проверить, пуста ли очередь. O(1)"""
        return len(self._items) == 0
    
    def size(self):
        """Вернуть размер очереди. O(1)"""
        return len(self._items)
    
    def __len__(self):
        return self.size()
    
    def __repr__(self):
        return f"Queue({list(self._items)})"


# ===== ЗАДАЧИ НА СТЕК =====

def is_valid_parentheses(s):
    """
    Проверка сбалансированности скобок.
    
    Классическая задача на стек. Проверяем, что каждая открывающая
    скобка имеет соответствующую закрывающую в правильном порядке.
    
    Аргументы:
        s: строка со скобками
    
    Возвращает:
        bool: True если скобки сбалансированы
    
    Сложность: O(n) по времени, O(n) по памяти
    
    Пример:
        >>> is_valid_parentheses("()[]{}")
        True
        >>> is_valid_parentheses("([)]")
        False
    """
    stack = Stack()
    pairs = {')': '(', ']': '[', '}': '{'}
    
    for char in s:
        if char in pairs.values():  # Открывающая скобка
            stack.push(char)
        elif char in pairs:  # Закрывающая скобка
            if stack.is_empty() or stack.pop() != pairs[char]:
                return False
    
    return stack.is_empty()


def evaluate_rpn(tokens):
    """
    Вычисление обратной польской записи (RPN).
    
    RPN (Reverse Polish Notation) — форма записи выражений,
    где операторы следуют за операндами. Вычисляется с помощью стека.
    
    Аргументы:
        tokens: список токенов (числа и операторы)
    
    Возвращает:
        int: результат вычисления
    
    Сложность: O(n)
    
    Пример:
        >>> evaluate_rpn(["2", "1", "+", "3", "*"])
        9
        >>> evaluate_rpn(["4", "13", "5", "/", "+"])
        6
    """
    stack = Stack()
    operators = {
        '+': lambda a, b: a + b,
        '-': lambda a, b: a - b,
        '*': lambda a, b: a * b,
        '/': lambda a, b: int(a / b),
    }
    
    for token in tokens:
        if token in operators:
            b = stack.pop()
            a = stack.pop()
            stack.push(operators[token](a, b))
        else:
            stack.push(int(token))
    
    return stack.pop()


def next_greater_element(nums):
    """
    Найти следующий больший элемент для каждого элемента массива.
    
    Классическая задача на монотонный стек.
    Для каждого элемента находим первый элемент справа, который больше него.
    
    Аргументы:
        nums: список чисел
    
    Возвращает:
        list: для каждого элемента — следующий больший или -1
    
    Сложность: O(n)
    
    Пример:
        >>> next_greater_element([4, 5, 2, 25])
        [5, 25, 25, -1]
    """
    n = len(nums)
    result = [-1] * n
    stack = Stack()  # Хранит индексы
    
    for i in range(n):
        while not stack.is_empty() and nums[stack.peek()] < nums[i]:
            result[stack.pop()] = nums[i]
        stack.push(i)
    
    return result


def daily_temperatures(temperatures):
    """
    Количество дней до более тёплого дня.
    
    Для каждого дня определяем, через сколько дней будет теплее.
    
    Аргументы:
        temperatures: список температур
    
    Возвращает:
        list: количество дней до потепления (0 если не будет)
    
    Сложность: O(n)
    
    Пример:
        >>> daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73])
        [1, 1, 4, 2, 1, 1, 0, 0]
    """
    n = len(temperatures)
    result = [0] * n
    stack = Stack()  # Индексы дней с невозрастающими температурами
    
    for i in range(n):
        while not stack.is_empty() and temperatures[stack.peek()] < temperatures[i]:
            prev_idx = stack.pop()
            result[prev_idx] = i - prev_idx
        stack.push(i)
    
    return result


def largest_rectangle_histogram(heights):
    """
    Максимальная площадь прямоугольника в гистограмме.
    
    Задача на монотонный стек. Находим наибольший прямоугольник,
    который можно построить на основе гистограммы.
    
    Аргументы:
        heights: список высот столбцов
    
    Возвращает:
        int: максимальная площадь
    
    Сложность: O(n)
    
    Пример:
        >>> largest_rectangle_histogram([2, 1, 5, 6, 2, 3])
        10
    """
    stack = Stack()  # Индексы с возрастающими высотами
    max_area = 0
    
    for i, h in enumerate(heights + [0]):  # Добавляем 0 для очистки стека
        while not stack.is_empty() and heights[stack.peek()] > h:
            height = heights[stack.pop()]
            width = i if stack.is_empty() else i - stack.peek() - 1
            max_area = max(max_area, height * width)
        stack.push(i)
    
    return max_area


# ===== ЗАДАЧИ НА ОЧЕРЕДЬ =====

class RecentCounter:
    """
    Счётчик недавних запросов.
    
    Поддерживает количество запросов за последние 3000 мс.
    """
    
    def __init__(self):
        self.queue = Queue()
    
    def ping(self, t):
        """
        Зарегистрировать запрос в момент времени t.
        
        Возвращает количество запросов в интервале [t-3000, t].
        """
        self.queue.enqueue(t)
        while self.queue.front() < t - 3000:
            self.queue.dequeue()
        return self.queue.size()


def moving_average_stream(nums, k):
    """
    Скользящее среднее для потока данных.
    
    Вычисляет среднее значение для каждого окна размера k.
    
    Аргументы:
        nums: поток чисел
        k: размер окна
    
    Возвращает:
        list: скользящие средние значения
    
    Пример:
        >>> moving_average_stream([1, 10, 3, 5], 3)
        [1.0, 5.5, 4.67, 6.0]
    """
    queue = Queue()
    result = []
    window_sum = 0
    
    for num in nums:
        queue.enqueue(num)
        window_sum += num
        
        if queue.size() > k:
            window_sum -= queue.dequeue()
        
        if queue.size() == k:
            result.append(window_sum / k)
    
    return result


# ===== ДЕК (DEQUE) =====

class Deque:
    """
    Двусторонняя очередь (Double-ended queue).
    
    Позволяет добавлять и удалять элементы с обоих концов.
    """
    
    def __init__(self):
        self._items = deque()
    
    def add_front(self, item):
        """Добавить в начало. O(1)"""
        self._items.appendleft(item)
    
    def add_rear(self, item):
        """Добавить в конец. O(1)"""
        self._items.append(item)
    
    def remove_front(self):
        """Удалить и вернуть первый элемент. O(1)"""
        if self.is_empty():
            raise IndexError("Deque пуст")
        return self._items.popleft()
    
    def remove_rear(self):
        """Удалить и вернуть последний элемент. O(1)"""
        if self.is_empty():
            raise IndexError("Deque пуст")
        return self._items.pop()
    
    def is_empty(self):
        return len(self._items) == 0
    
    def size(self):
        return len(self._items)


def is_palindrome_deque(s):
    """
    Проверка палиндрома с использованием deque.
    
    Аргументы:
        s: строка для проверки
    
    Возвращает:
        bool: True если строка — палиндром
    
    Пример:
        >>> is_palindrome_deque("racecar")
        True
    """
    d = Deque()
    for char in s.lower():
        if char.isalnum():
            d.add_rear(char)
    
    while d.size() > 1:
        if d.remove_front() != d.remove_rear():
            return False
    
    return True


if __name__ == "__main__":
    print(__doc__)
    print("\n" + "="*60)
    
    # Тест стека
    print("Тестирование стека:")
    s = Stack()
    s.push(1)
    s.push(2)
    s.push(3)
    print(f"  Стек: {s}")
    print(f"  pop: {s.pop()}, peek: {s.peek()}")
    
    # Тест очереди
    print("\nТестирование очереди:")
    q = Queue()
    q.enqueue(1)
    q.enqueue(2)
    q.enqueue(3)
    print(f"  Очередь: {q}")
    print(f"  dequeue: {q.dequeue()}, front: {q.front()}")
    
    # Скобки
    print("\nПроверка скобок:")
    test_cases = ["()", "()[]{}", "(]", "([)]", "{[]}", ""]
    for case in test_cases:
        print(f"  '{case}': {is_valid_parentheses(case)}")
    
    # RPN
    print("\nОбратная польская запись:")
    expr = ["2", "1", "+", "3", "*"]
    print(f"  {expr} = {evaluate_rpn(expr)}")
    
    # Следующий больший элемент
    print("\nСледующий больший элемент:")
    nums = [4, 5, 2, 25]
    print(f"  {nums} -> {next_greater_element(nums)}")
    
    # Гистограмма
    print("\nМаксимальный прямоугольник в гистограмме:")
    heights = [2, 1, 5, 6, 2, 3]
    print(f"  {heights} -> {largest_rectangle_histogram(heights)}")
