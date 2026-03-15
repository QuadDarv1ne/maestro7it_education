"""
АЛГОРИТМЫ НА СВЯЗНЫХ СПИСКАХ (LINKED LIST ALGORITHMS)

Связный список — это линейная структура данных, где каждый элемент (узел)
содержит значение и ссылку на следующий элемент.

Типы связных списков:
1. Односвязный (singly linked): только ссылка на следующий
2. Двусвязный (doubly linked): ссылки на предыдущий и следующий
3. Циклический (circular): последний элемент ссылается на первый

Преимущества перед массивами:
- O(1) вставка и удаление в любой позиции (если есть ссылка)
- Динамический размер

Недостатки:
- O(n) доступ по индексу
- Дополнительная память на ссылки

Основные операции:
- Обход, поиск, вставка, удаление
- Разворот, обнаружение цикла
- Слияние, сортировка
- Нахождение середины, k-го элемента с конца
"""

from typing import Optional, List


# ===== ОПРЕДЕЛЕНИЕ УЗЛА =====

class ListNode:
    """
    Узел односвязного списка.
    
    Атрибуты:
        val: значение узла
        next: ссылка на следующий узел
    """
    
    def __init__(self, val: int = 0, next: 'ListNode' = None):
        self.val = val
        self.next = next
    
    def __repr__(self):
        return f"ListNode({self.val})"
    
    def to_list(self) -> List[int]:
        """Преобразование списка в Python list."""
        result = []
        current = self
        while current:
            result.append(current.val)
            current = current.next
        return result
    
    @staticmethod
    def from_list(values: List[int]) -> Optional['ListNode']:
        """Создание списка из Python list."""
        if not values:
            return None
        
        head = ListNode(values[0])
        current = head
        
        for val in values[1:]:
            current.next = ListNode(val)
            current = current.next
        
        return head


class DoublyListNode:
    """
    Узел двусвязного списка.
    
    Атрибуты:
        val: значение
        prev: ссылка на предыдущий узел
        next: ссылка на следующий узел
    """
    
    def __init__(self, val: int = 0):
        self.val = val
        self.prev = None
        self.next = None
    
    def __repr__(self):
        return f"DoublyListNode({self.val})"


# ===== БАЗОВЫЕ ОПЕРАЦИИ =====

def traverse(head: Optional[ListNode]) -> List[int]:
    """
    Обход связного списка.
    
    Аргументы:
        head: голова списка
    
    Возвращает:
        list: все значения в порядке следования
    
    Сложность: O(n) по времени, O(1) по памяти
    """
    result = []
    current = head
    
    while current:
        result.append(current.val)
        current = current.next
    
    return result


def get_length(head: Optional[ListNode]) -> int:
    """
    Вычисление длины списка.
    
    Сложность: O(n)
    """
    length = 0
    current = head
    
    while current:
        length += 1
        current = current.next
    
    return length


def get_node(head: Optional[ListNode], index: int) -> Optional[ListNode]:
    """
    Получение узла по индексу.
    
    Аргументы:
        head: голова списка
        index: индекс (0-based)
    
    Возвращает:
        ListNode: узел или None если индекс вне диапазона
    
    Сложность: O(n)
    """
    current = head
    count = 0
    
    while current:
        if count == index:
            return current
        count += 1
        current = current.next
    
    return None


def search(head: Optional[ListNode], val: int) -> Optional[ListNode]:
    """
    Поиск узла по значению.
    
    Возвращает первый узел с заданным значением.
    
    Сложность: O(n)
    """
    current = head
    
    while current:
        if current.val == val:
            return current
        current = current.next
    
    return None


def insert_at_beginning(head: Optional[ListNode], val: int) -> ListNode:
    """
    Вставка узла в начало списка.
    
    Аргументы:
        head: голова списка (может быть None)
        val: значение нового узла
    
    Возвращает:
        ListNode: новая голова списка
    
    Сложность: O(1)
    """
    new_node = ListNode(val)
    new_node.next = head
    return new_node


def insert_at_end(head: Optional[ListNode], val: int) -> ListNode:
    """
    Вставка узла в конец списка.
    
    Сложность: O(n)
    """
    new_node = ListNode(val)
    
    if not head:
        return new_node
    
    current = head
    while current.next:
        current = current.next
    
    current.next = new_node
    return head


def insert_after(node: ListNode, val: int) -> None:
    """
    Вставка узла после заданного.
    
    Сложность: O(1)
    """
    new_node = ListNode(val)
    new_node.next = node.next
    node.next = new_node


def delete_node(head: Optional[ListNode], val: int) -> Optional[ListNode]:
    """
    Удаление первого узла с заданным значением.
    
    Аргументы:
        head: голова списка
        val: значение для удаления
    
    Возвращает:
        ListNode: новая голова списка
    
    Сложность: O(n)
    """
    # Удаление головы
    if head and head.val == val:
        return head.next
    
    current = head
    
    while current and current.next:
        if current.next.val == val:
            current.next = current.next.next
            return head
        current = current.next
    
    return head


def delete_at_index(head: Optional[ListNode], index: int) -> Optional[ListNode]:
    """
    Удаление узла по индексу.
    
    Сложность: O(n)
    """
    if index < 0:
        return head
    
    # Удаление головы
    if index == 0:
        return head.next if head else None
    
    current = head
    count = 0
    
    while current and count < index - 1:
        current = current.next
        count += 1
    
    # Проверяем существование следующего узла
    if current and current.next:
        current.next = current.next.next
    
    return head


# ===== РАЗВОРОТ СПИСКА =====

def reverse_list(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    Разворот связного списка итеративно.
    
    Аргументы:
        head: голова списка
    
    Возвращает:
        ListNode: новая голова развёрнутого списка
    
    Сложность: O(n) по времени, O(1) по памяти
    
    Пример:
        >>> # 1 -> 2 -> 3 -> None
        >>> # становится
        >>> # 3 -> 2 -> 1 -> None
    """
    prev = None
    current = head
    
    while current:
        # Сохраняем следующий узел
        next_node = current.next
        # Разворачиваем ссылку
        current.next = prev
        # Двигаемся вперёд
        prev = current
        current = next_node
    
    return prev


def reverse_list_recursive(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    Разворот списка рекурсивно.
    
    Сложность: O(n) по времени, O(n) по памяти (стек)
    """
    # Базовый случай
    if not head or not head.next:
        return head
    
    # Рекурсивно разворачиваем хвост
    new_head = reverse_list_recursive(head.next)
    
    # Разворачиваем текущую связь
    head.next.next = head
    head.next = None
    
    return new_head


def reverse_between(head: Optional[ListNode], left: int, right: int) -> Optional[ListNode]:
    """
    Разворот части списка от позиции left до right.
    
    Аргументы:
        head: голова списка
        left, right: границы разворота (1-based)
    
    Возвращает:
        ListNode: голова изменённого списка
    
    Сложность: O(n)
    
    Пример:
        >>> # 1 -> 2 -> 3 -> 4 -> 5, left=2, right=4
        >>> # становится
        >>> # 1 -> 4 -> 3 -> 2 -> 5
    """
    if not head or left == right:
        return head
    
    # Создаём фиктивный узел для упрощения граничных случаев
    dummy = ListNode(0)
    dummy.next = head
    prev = dummy
    
    # Доходим до позиции left
    for _ in range(left - 1):
        prev = prev.next
    
    # Разворачиваем segment
    current = prev.next
    next_node = None
    
    for _ in range(right - left + 1):
        temp = current.next
        current.next = next_node
        next_node = current
        current = temp
    
    # Соединяем развёрнутую часть с остальным списком
    prev.next.next = current
    prev.next = next_node
    
    return dummy.next


# ===== СЕРЕДИНА СПИСКА =====

def middle_node(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    Нахождение середины списка (метод двух указателей).
    
    Если длина нечётная — возвращается средний узел.
    Если чётная — второй из двух средних.
    
    Аргументы:
        head: голова списка
    
    Возвращает:
        ListNode: средний узел
    
    Сложность: O(n) по времени, O(1) по памяти
    """
    slow = head
    fast = head
    
    # Fast движется в 2 раза быстрее
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    
    return slow


def middle_node_left(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    Нахождение левой середины (для чётной длины).
    
    Полезно для разделения списка на две части.
    """
    if not head:
        return None
    
    slow = head
    fast = head.next
    
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    
    return slow


# ===== K-Й ЭЛЕМЕНТ С КОНЦА =====

def nth_from_end(head: Optional[ListNode], n: int) -> Optional[ListNode]:
    """
    N-й элемент с конца списка.
    
    Метод двух указателей с разницей n.
    
    Аргументы:
        head: голова списка
        n: позиция с конца (1-based)
    
    Возвращает:
        ListNode: n-й узел с конца или None
    
    Сложность: O(n) по времени, O(1) по памяти
    
    Пример:
        >>> # 1 -> 2 -> 3 -> 4 -> 5, n=2
        >>> # возвращается узел со значением 4
    """
    fast = head
    slow = head
    
    # Fast уходит вперёд на n шагов
    for _ in range(n):
        if not fast:
            return None  # n больше длины списка
        fast = fast.next
    
    # Оба указателя движутся синхронно
    while fast:
        slow = slow.next
        fast = fast.next
    
    return slow


def remove_nth_from_end(head: Optional[ListNode], n: int) -> Optional[ListNode]:
    """
    Удаление N-го узла с конца.
    
    Сложность: O(n)
    """
    dummy = ListNode(0)
    dummy.next = head
    
    fast = dummy
    slow = dummy
    
    # Fast уходит на n+1 шагов
    for _ in range(n + 1):
        if not fast:
            return head
        fast = fast.next
    
    # Движемся до конца
    while fast:
        slow = slow.next
        fast = fast.next
    
    # Удаляем узел
    slow.next = slow.next.next
    
    return dummy.next


# ===== ОБНАРУЖЕНИЕ ЦИКЛА =====

def has_cycle(head: Optional[ListNode]) -> bool:
    """
    Проверка наличия цикла (алгоритм Флойда).
    
    Использует два указателя: медленный и быстрый.
    Если есть цикл — они встретятся.
    
    Аргументы:
        head: голова списка
    
    Возвращает:
        bool: True если есть цикл
    
    Сложность: O(n) по времени, O(1) по памяти
    """
    if not head or not head.next:
        return False
    
    slow = head
    fast = head
    
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        
        if slow == fast:
            return True
    
    return False


def detect_cycle_start(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    Нахождение начала цикла.
    
    После встречи fast и slow, сбрасываем один из них
    на голову и движемся синхронно до встречи.
    
    Аргументы:
        head: голова списка
    
    Возвращает:
        ListNode: узел, где начинается цикл, или None
    
    Сложность: O(n)
    """
    if not head or not head.next:
        return None
    
    slow = head
    fast = head
    
    # Фаза 1: обнаружение цикла
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        
        if slow == fast:
            break
    else:
        return None  # Цикла нет
    
    # Фаза 2: находим начало
    slow = head
    while slow != fast:
        slow = slow.next
        fast = fast.next
    
    return slow


def get_cycle_length(head: Optional[ListNode]) -> int:
    """
    Вычисление длины цикла.
    
    После обнаружения цикла, фиксируем узел и считаем шаги до возврата.
    """
    if not head or not head.next:
        return 0
    
    slow = head
    fast = head
    
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        
        if slow == fast:
            # Считаем длину
            length = 1
            current = slow.next
            while current != slow:
                current = current.next
                length += 1
            return length
    
    return 0


# ===== СЛИЯНИЕ СПИСКОВ =====

def merge_two_sorted(l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
    """
    Слияние двух отсортированных списков.
    
    Аргументы:
        l1, l2: головы отсортированных списков
    
    Возвращает:
        ListNode: голова объединённого отсортированного списка
    
    Сложность: O(n + m) по времени, O(1) по памяти
    
    Пример:
        >>> # l1: 1 -> 2 -> 4
        >>> # l2: 1 -> 3 -> 4
        >>> # результат: 1 -> 1 -> 2 -> 3 -> 4 -> 4
    """
    dummy = ListNode(0)
    current = dummy
    
    while l1 and l2:
        if l1.val <= l2.val:
            current.next = l1
            l1 = l1.next
        else:
            current.next = l2
            l2 = l2.next
        current = current.next
    
    # Присоединяем оставшуюся часть
    current.next = l1 if l1 else l2
    
    return dummy.next


def merge_two_sorted_recursive(l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
    """
    Рекурсивное слияние отсортированных списков.
    """
    if not l1:
        return l2
    if not l2:
        return l1
    
    if l1.val <= l2.val:
        l1.next = merge_two_sorted_recursive(l1.next, l2)
        return l1
    else:
        l2.next = merge_two_sorted_recursive(l1, l2.next)
        return l2


def merge_k_sorted(lists: List[Optional[ListNode]]) -> Optional[ListNode]:
    """
    Слияние K отсортированных списков.
    
    Использует divide and conquer.
    
    Аргументы:
        lists: список голов отсортированных списков
    
    Возвращает:
        ListNode: голова объединённого списка
    
    Сложность: O(N log k), где N — общее количество узлов
    """
    if not lists:
        return None
    
    def merge_range(left: int, right: int) -> Optional[ListNode]:
        """Слияние списков в диапазоне [left, right]."""
        if left == right:
            return lists[left]
        
        mid = (left + right) // 2
        l1 = merge_range(left, mid)
        l2 = merge_range(mid + 1, right)
        
        return merge_two_sorted(l1, l2)
    
    return merge_range(0, len(lists) - 1)


# ===== СОРТИРОВКА СПИСКА =====

def sort_list(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    Сортировка списка (Merge Sort).
    
    Аргументы:
        head: голова списка
    
    Возвращает:
        ListNode: голова отсортированного списка
    
    Сложность: O(n log n) по времени, O(log n) по памяти (рекурсия)
    """
    # Базовый случай
    if not head or not head.next:
        return head
    
    # Находим середину
    mid = middle_node_left(head)
    right_head = mid.next
    mid.next = None  # Разрываем связь
    
    # Рекурсивно сортируем обе части
    left = sort_list(head)
    right = sort_list(right_head)
    
    # Сливаем
    return merge_two_sorted(left, right)


# ===== ПАЛИНДРОМ =====

def is_palindrome_list(head: Optional[ListNode]) -> bool:
    """
    Проверка, является ли список палиндромом.
    
    Алгоритм:
    1. Находим середину
    2. Разворачиваем вторую половину
    3. Сравниваем
    4. Восстанавливаем (опционально)
    
    Аргументы:
        head: голова списка
    
    Возвращает:
        bool: True если палиндром
    
    Сложность: O(n) по времени, O(1) по памяти
    """
    if not head or not head.next:
        return True
    
    # Находим середину
    slow = head
    fast = head.next
    
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    
    # Разворачиваем вторую половину
    second_half = reverse_list(slow.next)
    
    # Сравниваем
    first = head
    second = second_half
    result = True
    
    while second:
        if first.val != second.val:
            result = False
            break
        first = first.next
        second = second.next
    
    # Восстанавливаем (опционально)
    slow.next = reverse_list(second_half)
    
    return result


# ===== ПЕРЕСЕЧЕНИЕ СПИСКОВ =====

def get_intersection_node(headA: Optional[ListNode], headB: Optional[ListNode]) -> Optional[ListNode]:
    """
    Нахождение узла пересечения двух списков.
    
    Списки могут разветвляться, но после пересечения идут вместе.
    
    Аргументы:
        headA, headB: головы двух списков
    
    Возвращает:
        ListNode: узел пересечения или None
    
    Сложность: O(n + m) по времени, O(1) по памяти
    
    Алгоритм:
    - Проходим оба списка, после конца переключаемся на другой
    - При одинаковой длине пересечение найдётся сразу
    - При разной длине разница компенсируется переключением
    """
    if not headA or not headB:
        return None
    
    pA = headA
    pB = headB
    
    # Указатели встретятся в точке пересечения или в None
    while pA != pB:
        pA = pA.next if pA else headB
        pB = pB.next if pB else headA
    
    return pA


# ===== КОПИРОВАНИЕ СЛУЧАЙНЫХ УКАЗАТЕЛЕЙ =====

class NodeWithRandom:
    """Узел со случайным указателем."""
    
    def __init__(self, val: int = 0, next: 'NodeWithRandom' = None, random: 'NodeWithRandom' = None):
        self.val = val
        self.next = next
        self.random = random
    
    def __repr__(self):
        return f"Node({self.val})"


def copy_random_list(head: Optional[NodeWithRandom]) -> Optional[NodeWithRandom]:
    """
    Копирование списка со случайными указателями.
    
    Аргументы:
        head: голова списка с random указателями
    
    Возвращает:
        NodeWithRandom: голова копии
    
    Сложность: O(n) по времени, O(n) по памяти
    
    Алгоритм:
    1. Проходим и создаём копии узлов, сохраняя в хеш-таблицу
    2. Проходим снова и устанавливаем next и random
    """
    if not head:
        return None
    
    # Хеш-таблица: оригинал -> копия
    mapping = {}
    
    # Первый проход: создаём копии
    current = head
    while current:
        mapping[current] = NodeWithRandom(current.val)
        current = current.next
    
    # Второй проход: устанавливаем ссылки
    current = head
    while current:
        copy = mapping[current]
        copy.next = mapping.get(current.next)
        copy.random = mapping.get(current.random)
        current = current.next
    
    return mapping[head]


def copy_random_list_optimized(head: Optional[NodeWithRandom]) -> Optional[NodeWithRandom]:
    """
    Копирование со случайными указателями без дополнительной памяти.
    
    O(1) по памяти, O(n) по времени.
    
    Алгоритм:
    1. Вставляем копии после оригиналов
    2. Устанавливаем random (copy.random = original.random.next)
    3. Разделяем списки
    """
    if not head:
        return None
    
    # Шаг 1: создаём копии и вставляем после оригиналов
    current = head
    while current:
        copy = NodeWithRandom(current.val)
        copy.next = current.next
        current.next = copy
        current = copy.next
    
    # Шаг 2: устанавливаем random
    current = head
    while current:
        if current.random:
            current.next.random = current.random.next
        current = current.next.next
    
    # Шаг 3: разделяем списки
    dummy = NodeWithRandom(0)
    copy_current = dummy
    current = head
    
    while current:
        copy_current.next = current.next
        copy_current = copy_current.next
        current.next = current.next.next
        current = current.next
    
    return dummy.next


# ===== РАЗДЕЛЕНИЕ СПИСКА =====

def partition_list(head: Optional[ListNode], x: int) -> Optional[ListNode]:
    """
    Разделение списка по значению x.
    
    Все элементы < x идут до элементов >= x.
    Относительный порядок сохраняется.
    
    Аргументы:
        head: голова списка
        x: значение разделения
    
    Возвращает:
        ListNode: голова разделённого списка
    
    Сложность: O(n)
    """
    # Два фиктивных узла для двух списков
    less_dummy = ListNode(0)
    greater_dummy = ListNode(0)
    
    less = less_dummy
    greater = greater_dummy
    current = head
    
    while current:
        if current.val < x:
            less.next = current
            less = less.next
        else:
            greater.next = current
            greater = greater.next
        current = current.next
    
    # Соединяем
    less.next = greater_dummy.next
    greater.next = None  # Важно!
    
    return less_dummy.next


# ===== ROTATE LIST =====

def rotate_right(head: Optional[ListNode], k: int) -> Optional[ListNode]:
    """
    Поворот списка вправо на k позиций.
    
    Аргументы:
        head: голова списка
        k: количество поворотов
    
    Возвращает:
        ListNode: голова повёрнутого списка
    
    Сложность: O(n)
    
    Пример:
        >>> # 1 -> 2 -> 3 -> 4 -> 5, k=2
        >>> # становится
        >>> # 4 -> 5 -> 1 -> 2 -> 3
    """
    if not head or not head.next or k == 0:
        return head
    
    # Вычисляем длину
    length = 1
    tail = head
    while tail.next:
        tail = tail.next
        length += 1
    
    # Нормализуем k
    k = k % length
    if k == 0:
        return head
    
    # Находим новую точку разрыва
    new_tail = head
    for _ in range(length - k - 1):
        new_tail = new_tail.next
    
    # Переносим
    new_head = new_tail.next
    new_tail.next = None
    tail.next = head
    
    return new_head


# ===== СВОЙ СПИСОК С ДУБЛИКАТАМИ =====

def delete_duplicates_sorted(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    Удаление дубликатов из отсортированного списка.
    
    Оставляем по одному экземпляру каждого значения.
    
    Сложность: O(n)
    """
    current = head
    
    while current and current.next:
        if current.val == current.next.val:
            current.next = current.next.next
        else:
            current = current.next
    
    return head


def delete_all_duplicates_sorted(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    Удаление всех узлов с дублирующимися значениями.
    
    Сложность: O(n)
    """
    dummy = ListNode(0)
    dummy.next = head
    prev = dummy
    
    while head:
        # Проверяем, есть ли дубликаты
        if head.next and head.val == head.next.val:
            # Пропускаем все узлы с этим значением
            duplicate_val = head.val
            while head and head.val == duplicate_val:
                head = head.next
            prev.next = head
        else:
            prev = head
            head = head.next
    
    return dummy.next


# ===== ADD TWO NUMBERS =====

def add_two_numbers(l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
    """
    Сложение двух чисел, представленных списками.
    
    Цифры хранятся в обратном порядке (младшая цифра первой).
    
    Аргументы:
        l1, l2: списки цифр
    
    Возвращает:
        ListNode: сумма в виде списка
    
    Сложность: O(max(n, m))
    
    Пример:
        >>> # l1: 2 -> 4 -> 3 (342)
        >>> # l2: 5 -> 6 -> 4 (465)
        >>> # результат: 7 -> 0 -> 8 (807)
    """
    dummy = ListNode(0)
    current = dummy
    carry = 0
    
    while l1 or l2 or carry:
        val1 = l1.val if l1 else 0
        val2 = l2.val if l2 else 0
        
        total = val1 + val2 + carry
        carry = total // 10
        
        current.next = ListNode(total % 10)
        current = current.next
        
        l1 = l1.next if l1 else None
        l2 = l2.next if l2 else None
    
    return dummy.next


# ===== FLATTEN MULTILEVEL LIST =====

class MultiLevelNode:
    """Узел многоуровневого списка."""
    
    def __init__(self, val: int = 0, next: 'MultiLevelNode' = None, child: 'MultiLevelNode' = None):
        self.val = val
        self.next = next
        self.child = child


def flatten_multilevel(head: Optional[MultiLevelNode]) -> Optional[MultiLevelNode]:
    """
    Выпрямление многоуровневого списка.
    
    Аргументы:
        head: голова многоуровневого списка
    
    Возвращает:
        MultiLevelNode: выпрямленный список
    
    Сложность: O(n)
    """
    if not head:
        return None
    
    dummy = MultiLevelNode(0)
    dummy.next = head
    prev = dummy
    
    stack = [head]
    
    while stack:
        current = stack.pop()
        prev.next = current
        
        if current.next:
            stack.append(current.next)
        
        if current.child:
            stack.append(current.child)
            current.child = None
        
        prev = current
    
    return dummy.next


if __name__ == "__main__":
    print(__doc__)
    print("\n" + "="*60)
    
    # Создаём тестовый список
    head = ListNode.from_list([1, 2, 3, 4, 5])
    print(f"Исходный список: {head.to_list()}")
    
    # Обход
    print(f"\nОбход: {traverse(head)}")
    print(f"Длина: {get_length(head)}")
    
    # Разворот
    reversed_head = reverse_list(ListNode.from_list([1, 2, 3, 4, 5]))
    print(f"\nРазворот: {reversed_head.to_list()}")
    
    # Середина
    head = ListNode.from_list([1, 2, 3, 4, 5])
    mid = middle_node(head)
    print(f"\nСередина: {mid.val}")
    
    head = ListNode.from_list([1, 2, 3, 4, 5, 6])
    mid = middle_node(head)
    print(f"Середина (чётная длина): {mid.val}")
    
    # N-й с конца
    head = ListNode.from_list([1, 2, 3, 4, 5])
    nth = nth_from_end(head, 2)
    print(f"\n2-й с конца: {nth.val}")
    
    # Слияние
    l1 = ListNode.from_list([1, 2, 4])
    l2 = ListNode.from_list([1, 3, 4])
    merged = merge_two_sorted(l1, l2)
    print(f"\nСлияние [1,2,4] и [1,3,4]: {merged.to_list()}")
    
    # Сортировка
    unsorted = ListNode.from_list([4, 2, 1, 3])
    sorted_head = sort_list(unsorted)
    print(f"\nСортировка [4,2,1,3]: {sorted_head.to_list()}")
    
    # Палиндром
    pal = ListNode.from_list([1, 2, 2, 1])
    print(f"\n[1,2,2,1] палиндром: {is_palindrome_list(pal)}")
    
    pal = ListNode.from_list([1, 2, 3, 2, 1])
    print(f"[1,2,3,2,1] палиндром: {is_palindrome_list(pal)}")
    
    # Цикл
    cyclic = ListNode.from_list([1, 2, 3, 4, 5])
    cyclic.next.next.next.next.next = cyclic.next  # 5 -> 2
    print(f"\nНаличие цикла: {has_cycle(cyclic)}")
    print(f"Начало цикла: {detect_cycle_start(cyclic).val}")
    
    # Сложение чисел
    num1 = ListNode.from_list([2, 4, 3])  # 342
    num2 = ListNode.from_list([5, 6, 4])  # 465
    result = add_two_numbers(num1, num2)
    print(f"\n342 + 465 = {result.to_list()}")  # 807
    
    # Rotate
    head = ListNode.from_list([1, 2, 3, 4, 5])
    rotated = rotate_right(head, 2)
    print(f"\nRotate right на 2: {rotated.to_list()}")
