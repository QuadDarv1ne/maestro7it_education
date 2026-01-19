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

class Node:
    """Узел двусвязного списка"""
    def __init__(self, key=0, value=0):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    """
    @brief Класс LRU (Least Recently Used) кэша
    
    Реализация с использованием:
    1. Двусвязного списка для отслеживания порядка использования
    2. Словаря (hash map) для быстрого доступа по ключу
    
    Сложность операций: O(1) для get и put
    """
    
    def __init__(self, capacity):
        """
        @brief Конструктор LRU кэша
        @param capacity: Максимальная емкость кэша
        """
        self.capacity = capacity
        self.cache = {}  # ключ -> узел
        
        # Инициализация фиктивных узлов
        self.head = Node()  # самый недавно использованный
        self.tail = Node()  # самый старый
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def _remove_node(self, node):
        """
        @brief Удаляет узел из списка
        @param node: Узел для удаления
        """
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node
    
    def _add_to_front(self, node):
        """
        @brief Добавляет узел в начало списка
        @param node: Узел для добавления
        """
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node
    
    def _move_to_front(self, node):
        """
        @brief Перемещает узел в начало списка
        @param node: Узел для перемещения
        """
        self._remove_node(node)
        self._add_to_front(node)
    
    def _remove_lru(self):
        """
        @brief Удаляет самый старый узел (Least Recently Used)
        """
        lru_node = self.tail.prev
        self._remove_node(lru_node)
        del self.cache[lru_node.key]
    
    def get(self, key):
        """
        @brief Получает значение по ключу
        @param key: Ключ для поиска
        @return: Значение или -1, если ключ не найден
        """
        if key not in self.cache:
            return -1
        
        node = self.cache[key]
        self._move_to_front(node)  # Обновляем как недавно использованный
        return node.value
    
    def put(self, key, value):
        """
        @brief Добавляет или обновляет пару ключ-значение
        @param key: Ключ
        @param value: Значение
        """
        if key in self.cache:
            # Ключ уже существует, обновляем значение
            node = self.cache[key]
            node.value = value
            self._move_to_front(node)
        else:
            # Новый ключ
            if len(self.cache) >= self.capacity:
                # Удаляем самый старый элемент
                self._remove_lru()
            
            # Создаем новый узел
            new_node = Node(key, value)
            self._add_to_front(new_node)
            self.cache[key] = new_node

# Альтернативная реализация с использованием OrderedDict
from collections import OrderedDict

class LRUCacheOrderedDict:
    """
    @brief Упрощенная реализация LRU кэша с использованием OrderedDict
    
    OrderedDict в Python сохраняет порядок вставки.
    При доступе к элементу перемещаем его в конец.
    При переполнении удаляем первый элемент.
    """
    
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = OrderedDict()
    
    def get(self, key):
        if key not in self.cache:
            return -1
        
        # Перемещаем в конец (как самый недавно использованный)
        self.cache.move_to_end(key)
        return self.cache[key]
    
    def put(self, key, value):
        if key in self.cache:
            # Обновляем и перемещаем в конец
            self.cache.move_to_end(key)
        elif len(self.cache) >= self.capacity:
            # Удаляем самый старый элемент (первый в OrderedDict)
            self.cache.popitem(last=False)
        
        self.cache[key] = value