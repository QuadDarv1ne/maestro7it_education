"""
КУЧА / ПИРАМИДА (HEAP)

Куча — это специализированная структура данных типа "дерево",
обладающая свойством кучи: каждый родитель меньше/больше своих детей.

Min-Heap: каждый родитель меньше детей (минимум на вершине)
Max-Heap: каждый родитель больше детей (максимум на вершине)

В Python:
- heapq — min-heap по умолчанию
- Для max-heap: умножаем значения на -1

Основные операции:
- heapify: построение кучи из массива — O(n)
- push: добавление элемента — O(log n)
- pop: извлечение корня — O(log n)
- peek: просмотр корня — O(1)

Применение:
- Приоритетные очереди
- Сортировка (Heap Sort)
- K наибольших/наименьших элементов
- Слияние K отсортированных массивов
- Нахождение медианы потока
"""

import heapq


# ===== ОСНОВЫ РАБОТЫ С HEAPQ =====

def heap_basics():
    """
    Демонстрация основных операций с кучей в Python.
    
    heapq работает с обычными списками, превращая их в кучи.
    """
    # Создание кучи
    arr = [3, 1, 4, 1, 5, 9, 2, 6]
    heapq.heapify(arr)  # Преобразование в кучу in-place — O(n)
    print(f"Куча: {arr}")  # Минимум в начале
    
    # Добавление элемента
    heapq.heappush(arr, 0)
    print(f"После добавления 0: {arr}")
    
    # Извлечение минимума
    minimum = heapq.heappop(arr)
    print(f"Извлечённый минимум: {minimum}, куча: {arr}")
    
    # Просмотр минимума без извлечения
    print(f"Текущий минимум: {arr[0]}")


# ===== ПРИОРИТЕТНАЯ ОЧЕРЕДЬ =====

class PriorityQueue:
    """
    Приоритетная очередь на основе кучи.
    
    Элементы извлекаются в порядке приоритета (меньше = выше приоритет).
    Для каждого элемента хранится (приоритет, счётчик, значение).
    Счётчик обеспечивает FIFO для элементов с равным приоритетом.
    
    Пример:
        >>> pq = PriorityQueue()
        >>> pq.push("task1", 3)
        >>> pq.push("task2", 1)
        >>> pq.push("task3", 2)
        >>> pq.pop()
        'task2'
    """
    
    def __init__(self):
        self._heap = []
        self._counter = 0
    
    def push(self, item, priority):
        """
        Добавить элемент с приоритетом.
        
        Аргументы:
            item: значение
            priority: приоритет (меньше = выше приоритет)
        
        Сложность: O(log n)
        """
        heapq.heappush(self._heap, (priority, self._counter, item))
        self._counter += 1
    
    def pop(self):
        """Извлечь элемент с наивысшим приоритетом. O(log n)"""
        if self.is_empty():
            raise IndexError("Очередь пуста")
        return heapq.heappop(self._heap)[2]
    
    def peek(self):
        """Просмотреть элемент с наивысшим приоритетом. O(1)"""
        if self.is_empty():
            raise IndexError("Очередь пуста")
        return self._heap[0][2]
    
    def is_empty(self):
        return len(self._heap) == 0
    
    def size(self):
        return len(self._heap)


# ===== K НАИБОЛЬШИХ / НАИМЕНЬШИХ ЭЛЕМЕНТОВ =====

def k_smallest(nums, k):
    """
    Найти k наименьших элементов.
    
    Аргументы:
        nums: список чисел
        k: количество элементов
    
    Возвращает:
        list: k наименьших элементов в возрастающем порядке
    
    Сложность: O(n log k) — эффективнее сортировки при k << n
    
    Пример:
        >>> k_smallest([3, 1, 4, 1, 5, 9, 2, 6], 3)
        [1, 1, 2]
    """
    return heapq.nsmallest(k, nums)


def k_largest(nums, k):
    """
    Найти k наибольших элементов.
    
    Аргументы:
        nums: список чисел
        k: количество элементов
    
    Возвращает:
        list: k наибольших элементов в убывающем порядке
    
    Сложность: O(n log k)
    
    Пример:
        >>> k_largest([3, 1, 4, 1, 5, 9, 2, 6], 3)
        [9, 6, 5]
    """
    return heapq.nlargest(k, nums)


def k_largest_efficient(nums, k):
    """
    Эффективное нахождение k наибольших с min-heap размера k.
    
    Альтернативная реализация, явно использующая кучу.
    """
    if k >= len(nums):
        return sorted(nums, reverse=True)
    
    heap = nums[:k]
    heapq.heapify(heap)  # Min-heap размера k
    
    for num in nums[k:]:
        if num > heap[0]:
            heapq.heapreplace(heap, num)  # Заменить минимум
    
    return sorted(heap, reverse=True)


# ===== СЛИЯНИЕ K ОТСОРТИРОВАННЫХ МАССИВОВ =====

def merge_k_sorted(arrays):
    """
    Слияние K отсортированных массивов.
    
    Аргументы:
        arrays: список отсортированных списков
    
    Возвращает:
        list: объединённый отсортированный список
    
    Сложность: O(N log K), где N — общее количество элементов
    
    Пример:
        >>> merge_k_sorted([[1, 4, 7], [2, 5, 8], [3, 6, 9]])
        [1, 2, 3, 4, 5, 6, 7, 8, 9]
    """
    heap = []
    result = []
    
    # Инициализация: первый элемент каждого массива
    for i, arr in enumerate(arrays):
        if arr:
            heapq.heappush(heap, (arr[0], i, 0))
    
    while heap:
        val, arr_idx, elem_idx = heapq.heappop(heap)
        result.append(val)
        
        # Добавляем следующий элемент из того же массива
        if elem_idx + 1 < len(arrays[arr_idx]):
            next_val = arrays[arr_idx][elem_idx + 1]
            heapq.heappush(heap, (next_val, arr_idx, elem_idx + 1))
    
    return result


# ===== МЕДИАНА ПОТОКА ДАННЫХ =====

class MedianFinder:
    """
    Нахождение медианы потока данных.
    
    Использует две кучи:
    - max_heap для левой половины (меньшие элементы)
    - min_heap для правой половины (большие элементы)
    
    Пример:
        >>> mf = MedianFinder()
        >>> for n in [1, 2, 3]:
        ...     mf.add_num(n)
        ...     print(mf.find_median())
        1.0
        1.5
        2.0
    """
    
    def __init__(self):
        # max_heap храним как отрицательные значения
        self.max_heap = []  # Левая половина (меньшие)
        self.min_heap = []  # Правая половина (большие)
    
    def add_num(self, num):
        """
        Добавить число в структуру.
        
        Балансируем кучи так, чтобы размер отличался не более чем на 1.
        
        Сложность: O(log n)
        """
        # Добавляем в max_heap, затем балансируем
        heapq.heappush(self.max_heap, -num)
        
        # Перемещаем максимум из max_heap в min_heap
        heapq.heappush(self.min_heap, -heapq.heappop(self.max_heap))
        
        # Если min_heap больше, возвращаем элемент в max_heap
        if len(self.min_heap) > len(self.max_heap):
            heapq.heappush(self.max_heap, -heapq.heappop(self.min_heap))
    
    def find_median(self):
        """
        Найти текущую медиану.
        
        Возвращает:
            float: медиана
        
        Сложность: O(1)
        """
        if len(self.max_heap) > len(self.min_heap):
            return -self.max_heap[0]
        return (-self.max_heap[0] + self.min_heap[0]) / 2


# ===== ТОП K ЧАСТЫХ ЭЛЕМЕНТОВ =====

def top_k_frequent(nums, k):
    """
    Найти k наиболее часто встречающихся элементов.
    
    Аргументы:
        nums: список чисел
        k: количество элементов
    
    Возвращает:
        list: k элементов с наибольшей частотой
    
    Сложность: O(n log k)
    
    Пример:
        >>> top_k_frequent([1, 1, 1, 2, 2, 3], 2)
        [1, 2]
    """
    from collections import Counter
    
    # Подсчёт частот
    counter = Counter(nums)
    
    # Используем heap для нахождения top k
    # (-частота, элемент) для max-heap эффекта
    heap = []
    
    for num, freq in counter.items():
        heapq.heappush(heap, (-freq, num))
    
    return [heapq.heappop(heap)[1] for _ in range(k)]


# ===== K-Я СТАТИСТИКА =====

def find_kth_largest(nums, k):
    """
    Найти k-й по величине элемент.
    
    Используем min-heap размера k.
    
    Аргументы:
        nums: список чисел
        k: порядковый номер по убыванию (1 = максимум)
    
    Возвращает:
        int: k-й по величине элемент
    
    Сложность: O(n log k)
    
    Пример:
        >>> find_kth_largest([3, 2, 1, 5, 6, 4], 2)
        5
    """
    heap = nums[:k]
    heapq.heapify(heap)
    
    for num in nums[k:]:
        if num > heap[0]:
            heapq.heapreplace(heap, num)
    
    return heap[0]


def find_kth_smallest(nums, k):
    """
    Найти k-й наименьший элемент.
    
    Аргументы:
        nums: список чисел
        k: порядковый номер по возрастанию (1 = минимум)
    
    Возвращает:
        int: k-й наименьший элемент
    
    Пример:
        >>> find_kth_smallest([3, 2, 1, 5, 6, 4], 2)
        2
    """
    # Используем max-heap (отрицательные значения)
    heap = [-x for x in nums[:k]]
    heapq.heapify(heap)
    
    for num in nums[k:]:
        if -num > heap[0]:
            heapq.heapreplace(heap, -num)
    
    return -heap[0]


# ===== СКОЛЬЗЯЩАЯ МЕДИАНА =====

def sliding_window_median(nums, k):
    """
    Медиана каждого окна размера k.
    
    Два heap'а (max и min) с ленивым удалением элементов.
    
    Аргументы:
        nums: список чисел
        k: размер окна
    
    Возвращает:
        list: медианы для каждого окна
    
    Сложность: O(n log k)
    """
    from collections import defaultdict
    
    result = []
    max_heap = []  # Отрицательные значения
    min_heap = []
    delayed = defaultdict(int)  # Элементы, помеченные на удаление
    
    def prune(heap, is_max_heap):
        """Удаляем элементы, помеченные на удаление."""
        while heap:
            num = -heap[0] if is_max_heap else heap[0]
            if (is_max_heap and delayed[num] > 0 and -heap[0] == num) or \
               (not is_max_heap and delayed[num] > 0 and heap[0] == num):
                delayed[num] -= 1
                if delayed[num] == 0:
                    del delayed[num]
                heapq.heappop(heap)
            else:
                break
    
    def balance():
        """Балансировка heap'ов."""
        if len(max_heap) > len(min_heap) + 1:
            heapq.heappush(min_heap, -heapq.heappop(max_heap))
            prune(max_heap, True)
        elif len(max_heap) < len(min_heap):
            heapq.heappush(max_heap, -heapq.heappop(min_heap))
            prune(min_heap, False)
    
    def get_median():
        if k % 2 == 1:
            return -max_heap[0]
        return (-max_heap[0] + min_heap[0]) / 2
    
    # Инициализация первого окна
    for i in range(k):
        num = nums[i]
        if not max_heap or num <= -max_heap[0]:
            heapq.heappush(max_heap, -num)
        else:
            heapq.heappush(min_heap, num)
        balance()
    
    result.append(get_median())
    
    # Скользим по массиву
    for i in range(k, len(nums)):
        out_num = nums[i - k]
        in_num = nums[i]
        
        delayed[out_num] += 1
        
        # Определяем, из какого heap'а удаляем
        if out_num <= -max_heap[0]:
            if out_num == -max_heap[0]:
                prune(max_heap, True)
        else:
            if out_num == min_heap[0]:
                prune(min_heap, False)
        
        # Добавляем новый элемент
        if in_num <= -max_heap[0]:
            heapq.heappush(max_heap, -in_num)
        else:
            heapq.heappush(min_heap, in_num)
        
        balance()
        prune(max_heap, True)
        prune(min_heap, False)
        
        result.append(get_median())
    
    return result


if __name__ == "__main__":
    print(__doc__)
    print("\n" + "="*60)
    
    # Основы
    print("Основы работы с кучей:")
    heap_basics()
    
    # Приоритетная очередь
    print("\nПриоритетная очередь:")
    pq = PriorityQueue()
    pq.push("Низкий приоритет", 3)
    pq.push("Высокий приоритет", 1)
    pq.push("Средний приоритет", 2)
    while not pq.is_empty():
        print(f"  Извлечено: {pq.pop()}")
    
    # K наибольших
    print("\nK наибольших элементов:")
    nums = [3, 1, 4, 1, 5, 9, 2, 6]
    print(f"  Массив: {nums}")
    print(f"  Топ-3: {k_largest(nums, 3)}")
    
    # Медиана потока
    print("\nМедиана потока данных:")
    mf = MedianFinder()
    for n in [1, 2, 3, 4]:
        mf.add_num(n)
        print(f"  После добавления {n}: медиана = {mf.find_median()}")
    
    # K-я статистика
    print("\nK-я статистика:")
    nums = [3, 2, 1, 5, 6, 4]
    print(f"  Массив: {nums}")
    print(f"  2-й наибольший: {find_kth_largest(nums, 2)}")
    print(f"  2-й наименьший: {find_kth_smallest(nums, 2)}")
    
    # Слияние K массивов
    print("\nСлияние K отсортированных массивов:")
    arrays = [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
    print(f"  Массивы: {arrays}")
    print(f"  Результат: {merge_k_sorted(arrays)}")
