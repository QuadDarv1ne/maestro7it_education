"""
СОРТИРОВКА МАССИВОВ (ARRAY SORTING)

Сортировка — одна из фундаментальных задач информатики.
Правильный выбор алгоритма сортировки критически важен для производительности.

Основные алгоритмы сортировки:
1. Пузырьковая сортировка (Bubble Sort) — O(n²)
2. Сортировка выбором (Selection Sort) — O(n²)
3. Сортировка вставками (Insertion Sort) — O(n²)
4. Сортировка слиянием (Merge Sort) — O(n log n)
5. Быстрая сортировка (Quick Sort) — O(n log n) в среднем
6. Пирамидальная сортировка (Heap Sort) — O(n log n)
7. Сортировка подсчётом (Counting Sort) — O(n + k)
8. Поразрядная сортировка (Radix Sort) — O(d·(n + k))

Выбор алгоритма:
- n ≤ 50: вставками (простая, эффективна на малых данных)
- n ≤ 1000: быстрая сортировка
- n > 1000: Timsort (встроенная в Python)
- Ограниченный диапазон значений: подсчётом
- Стабильность важна: слиянием или Timsort
"""


def bubble_sort(arr):
    """
    Пузырьковая сортировка.
    
    Многократно проходит по массиву, меняя соседние элементы,
    если они в неправильном порядке. "Тяжёлые" элементы "всплывают" в конец.
    
    Аргументы:
        arr: список для сортировки (изменяется in-place)
    
    Возвращает:
        list: отсортированный массив
    
    Сложность: O(n²) по времени, O(1) по памяти
    Стабильность: Да
    
    Пример:
        >>> bubble_sort([64, 34, 25, 12, 22, 11, 90])
        [11, 12, 22, 25, 34, 64, 90]
    """
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        # Оптимизация: если не было обменов — массив отсортирован
        if not swapped:
            break
    return arr


def selection_sort(arr):
    """
    Сортировка выбором.
    
    Находит минимальный элемент в неотсортированной части
    и помещает его в конец отсортированной части.
    
    Аргументы:
        arr: список для сортировки (изменяется in-place)
    
    Возвращает:
        list: отсортированный массив
    
    Сложность: O(n²) по времени, O(1) по памяти
    Стабильность: Нет
    
    Пример:
        >>> selection_sort([64, 25, 12, 22, 11])
        [11, 12, 22, 25, 64]
    """
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


def insertion_sort(arr):
    """
    Сортировка вставками.
    
    Строит отсортированный массив слева направо,
    вставляя каждый новый элемент в правильную позицию.
    
    Аргументы:
        arr: список для сортировки (изменяется in-place)
    
    Возвращает:
        list: отсортированный массив
    
    Сложность: O(n²) по времени, O(1) по памяти
    Стабильность: Да
    Особенность: O(n) на почти отсортированных данных!
    
    Пример:
        >>> insertion_sort([12, 11, 13, 5, 6])
        [5, 6, 11, 12, 13]
    """
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def merge_sort(arr):
    """
    Сортировка слиянием.
    
    Разделяет массив пополам, рекурсивно сортирует каждую половину,
    затем сливает отсортированные половины.
    
    Аргументы:
        arr: список для сортировки
    
    Возвращает:
        list: новый отсортированный массив
    
    Сложность: O(n log n) по времени, O(n) по памяти
    Стабильность: Да
    Особенность: Гарантированная сложность O(n log n)
    
    Пример:
        >>> merge_sort([38, 27, 43, 3, 9, 82, 10])
        [3, 9, 10, 27, 38, 43, 82]
    """
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    return _merge(left, right)


def _merge(left, right):
    """Вспомогательная функция для слияния двух отсортированных массивов."""
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def quick_sort(arr):
    """
    Быстрая сортировка.
    
    Выбирает опорный элемент (pivot), разделяет массив на элементы
    меньше и больше pivot, рекурсивно сортирует части.
    
    Аргументы:
        arr: список для сортировки
    
    Возвращает:
        list: новый отсортированный массив
    
    Сложность: O(n log n) в среднем, O(n²) в худшем случае
    Память: O(log n) для рекурсии
    Стабильность: Нет
    
    Пример:
        >>> quick_sort([10, 7, 8, 9, 1, 5])
        [1, 5, 7, 8, 9, 10]
    """
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quick_sort(left) + middle + quick_sort(right)


def quick_sort_inplace(arr, low=0, high=None):
    """
    Быстрая сортировка in-place.
    
    Более эффективная версия с экономией памяти.
    Использует схему разбиения Ломуто.
    
    Аргументы:
        arr: список для сортировки (изменяется in-place)
        low: левая граница
        high: правая граница
    
    Сложность: O(n log n) в среднем
    """
    if high is None:
        high = len(arr) - 1
    
    if low < high:
        pi = _partition(arr, low, high)
        quick_sort_inplace(arr, low, pi - 1)
        quick_sort_inplace(arr, pi + 1, high)
    
    return arr


def _partition(arr, low, high):
    """Разбиение для быстрой сортировки."""
    pivot = arr[high]
    i = low - 1
    
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def heap_sort(arr):
    """
    Пирамидальная сортировка.
    
    Использует структуру данных "куча" (heap).
    Строит max-heap, затем последовательно извлекает максимум.
    
    Аргументы:
        arr: список для сортировки (изменяется in-place)
    
    Возвращает:
        list: отсортированный массив
    
    Сложность: O(n log n) гарантированно
    Память: O(1)
    Стабильность: Нет
    
    Пример:
        >>> heap_sort([12, 11, 13, 5, 6, 7])
        [5, 6, 7, 11, 12, 13]
    """
    n = len(arr)
    
    # Построение max-heap
    for i in range(n // 2 - 1, -1, -1):
        _heapify(arr, n, i)
    
    # Извлечение элементов из кучи
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        _heapify(arr, i, 0)
    
    return arr


def _heapify(arr, n, i):
    """Восстановление свойства кучи."""
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2
    
    if left < n and arr[left] > arr[largest]:
        largest = left
    if right < n and arr[right] > arr[largest]:
        largest = right
    
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        _heapify(arr, n, largest)


def counting_sort(arr):
    """
    Сортировка подсчётом.
    
    Подходит для сортировки целых чисел в ограниченном диапазоне.
    Подсчитывает количество каждого элемента.
    
    Аргументы:
        arr: список целых чисел для сортировки
    
    Возвращает:
        list: отсортированный массив
    
    Сложность: O(n + k), где k — диапазон значений
    Память: O(k)
    Стабильность: Да
    
    Пример:
        >>> counting_sort([4, 2, 2, 8, 3, 3, 1])
        [1, 2, 2, 3, 3, 4, 8]
    """
    if not arr:
        return arr
    
    max_val = max(arr)
    min_val = min(arr)
    range_val = max_val - min_val + 1
    
    # Подсчёт
    count = [0] * range_val
    for num in arr:
        count[num - min_val] += 1
    
    # Восстановление
    result = []
    for i, c in enumerate(count):
        result.extend([i + min_val] * c)
    
    return result


def radix_sort(arr):
    """
    Поразрядная сортировка.
    
    Сортирует числа по разрядам, от младших к старшим.
    Использует сортировку подсчётом для каждого разряда.
    
    Аргументы:
        arr: список целых чисел для сортировки
    
    Возвращает:
        list: отсортированный массив
    
    Сложность: O(d·(n + k)), d — количество разрядов
    Память: O(n + k)
    Стабильность: Да
    
    Пример:
        >>> radix_sort([170, 45, 75, 90, 802, 24, 2, 66])
        [2, 24, 45, 66, 75, 90, 170, 802]
    """
    if not arr:
        return arr
    
    max_val = max(arr)
    exp = 1
    
    while max_val // exp > 0:
        arr = _counting_sort_by_digit(arr, exp)
        exp *= 10
    
    return arr


def _counting_sort_by_digit(arr, exp):
    """Сортировка подсчётом по определённому разряду."""
    n = len(arr)
    output = [0] * n
    count = [0] * 10
    
    for num in arr:
        digit = (num // exp) % 10
        count[digit] += 1
    
    for i in range(1, 10):
        count[i] += count[i - 1]
    
    for i in range(n - 1, -1, -1):
        digit = (arr[i] // exp) % 10
        output[count[digit] - 1] = arr[i]
        count[digit] -= 1
    
    return output


def shell_sort(arr):
    """
    Сортировка Шелла.
    
    Улучшенная версия сортировки вставками.
    Сначала сортирует элементы на большом расстоянии,
    затем уменьшает интервал.
    
    Аргументы:
        arr: список для сортировки (изменяется in-place)
    
    Возвращает:
        list: отсортированный массив
    
    Сложность: зависит от последовательности интервалов
                O(n log²n) для последовательности Хиббарда
    Память: O(1)
    
    Пример:
        >>> shell_sort([12, 34, 54, 2, 3])
        [2, 3, 12, 34, 54]
    """
    n = len(arr)
    gap = n // 2
    
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2
    
    return arr


if __name__ == "__main__":
    print(__doc__)
    print("\n" + "="*60)
    
    test_arrays = [
        [64, 34, 25, 12, 22, 11, 90],
        [38, 27, 43, 3, 9, 82, 10],
        [10, 7, 8, 9, 1, 5],
        [170, 45, 75, 90, 802, 24, 2, 66]
    ]
    
    algorithms = [
        ("Пузырьковая", bubble_sort),
        ("Выбором", selection_sort),
        ("Вставками", insertion_sort),
        ("Слиянием", merge_sort),
        ("Быстрая", quick_sort),
        ("Пирамидальная", heap_sort),
        ("Подсчётом", counting_sort),
        ("Поразрядная", radix_sort),
        ("Шелла", shell_sort),
    ]
    
    for arr in test_arrays[:1]:
        print(f"\nИсходный массив: {arr}")
        for name, func in algorithms:
            result = func(arr.copy())
            print(f"  {name}: {result}")
