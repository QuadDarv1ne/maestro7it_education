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

# Below is the interface for Iterator, which is already defined for you.
#
# class Iterator:
#     def __init__(self, nums):
#         """
#         Initializes an iterator object to the beginning of a list.
#         :type nums: List[int]
#         """
#
#     def hasNext(self):
#         """
#         Returns true if the iteration has more elements.
#         :rtype: bool
#         """
#
#     def next(self):
#         """
#         Returns the next element in the iteration.
#         :rtype: int
#         """

class PeekingIterator:
    """
    Класс PeekingIterator, который расширяет стандартный итератор методом peek().
    
    Позволяет просматривать следующий элемент итерации без продвижения итератора.
    
    Атрибуты:
        iterator: Исходный итератор
        next_element: Сохраненный следующий элемент
        has_next_element: Флаг наличия следующего элемента
    
    Методы:
        __init__(iterator): Инициализирует PeekingIterator с заданным итератором
        peek(): Возвращает следующий элемент без продвижения итератора
        next(): Возвращает следующий элемент и продвигает итератор
        hasNext(): Проверяет наличие следующего элемента
    
    Исключения:
        StopIteration: Вызывается при попытке peek() или next(), когда элементов нет
    
    Пример использования:
        >>> nums = [1, 2, 3]
        >>> iter = PeekingIterator(Iterator(nums))
        >>> iter.peek()    # 1
        >>> iter.next()    # 1
        >>> iter.hasNext() # True
    """
    
    def __init__(self, iterator):
        """
        Инициализирует PeekingIterator с заданным итератором.
        :type iterator: Iterator
        """
        self.iterator = iterator
        self.next_element = None
        self.has_next_element = False
        
        # Предзагружаем первый элемент при инициализации
        if self.iterator.hasNext():
            self.next_element = self.iterator.next()
            self.has_next_element = True

    def peek(self):
        """
        Возвращает следующий элемент без продвижения итератора.
        :rtype: int
        """
        if not self.has_next_element:
            raise StopIteration
        return self.next_element

    def next(self):
        """
        Возвращает следующий элемент и продвигает итератор.
        :rtype: int
        """
        if not self.has_next_element:
            raise StopIteration
        
        current = self.next_element
        # Загружаем следующий элемент из итератора
        if self.iterator.hasNext():
            self.next_element = self.iterator.next()
            self.has_next_element = True
        else:
            self.next_element = None
            self.has_next_element = False
        
        return current

    def hasNext(self):
        """
        Проверяет наличие следующего элемента.
        :rtype: bool
        """
        return self.has_next_element