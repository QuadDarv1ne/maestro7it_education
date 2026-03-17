"""
СОРТИРОВКИ — РАСШИРЕННЫЙ РАЗБОР (SORTING EXTENDED)

Глава 9 учебного пособия.

Темы:
- Quicksort (простой и in-place с randomized pivot)
- Mergesort (классический и Bottom-Up без рекурсии)
- Heapsort (in-place через max-heap)
- Сортировка подсчётом и поразрядная (Counting / Radix Sort)
- Сортировка слиянием K отсортированных массивов
- Порядковая статистика (K-й наименьший за O(n))
- Внешняя сортировка (External Sort) — концептуальный разбор
"""

import heapq
import random
from typing import List, Tuple


# =============================================================================
# QUICKSORT
# =============================================================================

def quicksort_simple(arr: List[int]) -> List[int]:
    """
    Быстрая сортировка (простая версия).

    Не изменяет исходный массив; создаёт новые списки.

    Аргументы:
        arr: список для сортировки

    Возвращает:
        list: отсортированный массив

    Сложность: O(n log n) среднее, O(n²) худшее
    Память: O(n log n) — из-за создания новых списков

    Пример:
        >>> quicksort_simple([3, 1, 4, 1, 5, 9, 2, 6])
        [1, 1, 2, 3, 4, 5, 6, 9]
    """
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left   = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right  = [x for x in arr if x > pivot]
    return quicksort_simple(left) + middle + quicksort_simple(right)


def quicksort_inplace(arr: List[int], lo: int = 0, hi: int = None) -> List[int]:
    """
    Быстрая сортировка in-place с рандомизацией pivot.

    Рандомизация устраняет квадратичный худший случай на
    отсортированных / обратно отсортированных данных.

    Аргументы:
        arr: список для сортировки (изменяется на месте)
        lo: левая граница
        hi: правая граница (включительно)

    Возвращает:
        list: тот же список, отсортированный

    Сложность: O(n log n) среднее, O(n²) худшее (редко при randomize)
    Память: O(log n) — стек рекурсии

    Пример:
        >>> arr = [3, 1, 4, 1, 5, 9, 2, 6]
        >>> quicksort_inplace(arr)
        [1, 1, 2, 3, 4, 5, 6, 9]
    """
    if hi is None:
        hi = len(arr) - 1

    if lo >= hi:
        return arr

    # Рандомизированный выбор pivot
    rand_idx = random.randint(lo, hi)
    arr[rand_idx], arr[hi] = arr[hi], arr[rand_idx]

    p = _partition_lomuto(arr, lo, hi)
    quicksort_inplace(arr, lo, p - 1)
    quicksort_inplace(arr, p + 1, hi)
    return arr


def _partition_lomuto(arr: List[int], lo: int, hi: int) -> int:
    """
    Схема разбиения Ломуто.

    Pivot = arr[hi]. Все элементы ≤ pivot перемещаются влево.
    Возвращает итоговую позицию pivot.
    """
    pivot = arr[hi]
    i = lo
    for j in range(lo, hi):
        if arr[j] <= pivot:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
    arr[i], arr[hi] = arr[hi], arr[i]
    return i


def quicksort_3way(arr: List[int], lo: int = 0, hi: int = None) -> List[int]:
    """
    Трёхпутевая быстрая сортировка (Dutch National Flag).

    Эффективна для данных с большим количеством дубликатов:
    разделяем на три части < pivot | == pivot | > pivot.

    Аргументы:
        arr: список для сортировки
        lo, hi: границы текущего подмассива

    Сложность: O(n log n) среднее, O(n) для массива из одинаковых элементов

    Пример:
        >>> arr = [2, 3, 2, 1, 2, 3, 1, 2]
        >>> quicksort_3way(arr)
        [1, 1, 2, 2, 2, 2, 3, 3]
    """
    if hi is None:
        hi = len(arr) - 1
    if lo >= hi:
        return arr

    pivot = arr[lo]
    lt, gt = lo, hi     # arr[lo..lt-1] < pivot, arr[gt+1..hi] > pivot
    i = lo

    while i <= gt:
        if arr[i] < pivot:
            arr[lt], arr[i] = arr[i], arr[lt]
            lt += 1
            i += 1
        elif arr[i] > pivot:
            arr[i], arr[gt] = arr[gt], arr[i]
            gt -= 1
        else:
            i += 1

    quicksort_3way(arr, lo, lt - 1)
    quicksort_3way(arr, gt + 1, hi)
    return arr


# =============================================================================
# MERGESORT
# =============================================================================

def mergesort(arr: List[int]) -> List[int]:
    """
    Сортировка слиянием (Top-Down, рекурсивная).

    Аргументы:
        arr: список для сортировки

    Возвращает:
        list: новый отсортированный список

    Сложность: O(n log n) по времени, O(n) по памяти
    Стабильная.

    Пример:
        >>> mergesort([5, 3, 8, 1, 9, 2])
        [1, 2, 3, 5, 8, 9]
    """
    n = len(arr)
    if n <= 1:
        return arr
    mid = n // 2
    return _merge(mergesort(arr[:mid]), mergesort(arr[mid:]))


def _merge(left: List[int], right: List[int]) -> List[int]:
    """Слить два отсортированных списка в один."""
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def mergesort_bottomup(arr: List[int]) -> List[int]:
    """
    Сортировка слиянием Bottom-Up (без рекурсии).

    Сначала сортируем подмассивы длины 1, затем 2, 4, 8, ...
    Не использует стек вызовов — подходит для очень больших данных.

    Аргументы:
        arr: список для сортировки

    Возвращает:
        list: отсортированный список

    Сложность: O(n log n) по времени, O(n) по памяти

    Пример:
        >>> mergesort_bottomup([5, 3, 8, 1, 9, 2])
        [1, 2, 3, 5, 8, 9]
    """
    n = len(arr)
    result = arr[:]
    size = 1

    while size < n:
        for lo in range(0, n, 2 * size):
            mid = min(lo + size, n)
            hi  = min(lo + 2 * size, n)
            merged = _merge(result[lo:mid], result[mid:hi])
            result[lo:hi] = merged
        size *= 2

    return result


def count_inversions(arr: List[int]) -> Tuple[List[int], int]:
    """
    Подсчёт инверсий в массиве через Mergesort.

    Инверсия — пара (i, j) такая, что i < j, но arr[i] > arr[j].
    Метод: при слиянии, если правый элемент меньше левого,
    он образует инверсии со всеми оставшимися элементами левой части.

    Аргументы:
        arr: список чисел

    Возвращает:
        tuple: (отсортированный массив, количество инверсий)

    Сложность: O(n log n)

    Применение:
        Оценка похожести рейтингов (метрика Кендалла).

    Пример:
        >>> count_inversions([3, 1, 2])
        ([1, 2, 3], 2)
    """
    def sort_and_count(a: List[int]) -> Tuple[List[int], int]:
        if len(a) <= 1:
            return a, 0
        mid = len(a) // 2
        left, lc = sort_and_count(a[:mid])
        right, rc = sort_and_count(a[mid:])
        merged = []
        inversions = lc + rc
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i]); i += 1
            else:
                merged.append(right[j]); j += 1
                inversions += len(left) - i    # все оставшиеся в left
        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged, inversions

    return sort_and_count(arr)


# =============================================================================
# HEAPSORT
# =============================================================================

def heapsort(arr: List[int]) -> List[int]:
    """
    Пирамидальная сортировка in-place.

    Этапы:
        1. Построение max-heap за O(n).
        2. n раз: переставить корень (максимум) в конец,
           восстановить свойство кучи за O(log n).

    Аргументы:
        arr: список для сортировки (изменяется на месте)

    Возвращает:
        list: тот же список, отсортированный

    Сложность: O(n log n) гарантировано, O(1) памяти
    Не стабилен. На практике медленнее Quicksort из-за кэш-промахов.

    Пример:
        >>> heapsort([12, 11, 13, 5, 6, 7])
        [5, 6, 7, 11, 12, 13]
    """
    n = len(arr)

    def sift_down(root: int, size: int) -> None:
        """Восстановить свойство max-heap для поддерева с корнем root."""
        while True:
            largest = root
            l, r = 2 * root + 1, 2 * root + 2
            if l < size and arr[l] > arr[largest]:
                largest = l
            if r < size and arr[r] > arr[largest]:
                largest = r
            if largest == root:
                break
            arr[root], arr[largest] = arr[largest], arr[root]
            root = largest

    # Построение max-heap
    for i in range(n // 2 - 1, -1, -1):
        sift_down(i, n)

    # Извлечение элементов: максимум в конец, восстановление кучи
    for end in range(n - 1, 0, -1):
        arr[0], arr[end] = arr[end], arr[0]
        sift_down(0, end)

    return arr


# =============================================================================
# COUNTING SORT И RADIX SORT
# =============================================================================

def counting_sort_stable(arr: List[int], key=None) -> List[int]:
    """
    Стабильная сортировка подсчётом.

    Работает только для целых чисел в ограниченном диапазоне.
    Используется как вспомогательный шаг в Radix Sort.

    Аргументы:
        arr: список целых чисел
        key: функция извлечения ключа (по умолчанию сам элемент)

    Возвращает:
        list: отсортированный список

    Сложность: O(n + k), k — диапазон значений ключа

    Пример:
        >>> counting_sort_stable([4, 2, 2, 8, 3, 3, 1])
        [1, 2, 2, 3, 3, 4, 8]
    """
    if not arr:
        return arr

    if key is None:
        key = lambda x: x

    keys = [key(x) for x in arr]
    min_k, max_k = min(keys), max(keys)
    k = max_k - min_k + 1

    count = [0] * k
    for kv in keys:
        count[kv - min_k] += 1

    # Накопленные суммы (позиции)
    for i in range(1, k):
        count[i] += count[i - 1]

    # Стабильное заполнение (справа налево для сохранения порядка)
    result = [None] * len(arr)
    for i in range(len(arr) - 1, -1, -1):
        kv = keys[i] - min_k
        count[kv] -= 1
        result[count[kv]] = arr[i]

    return result


def radix_sort(arr: List[int]) -> List[int]:
    """
    Поразрядная сортировка (LSD Radix Sort).

    Сортирует целые числа по разрядам от младшего к старшему.
    Использует стабильную сортировку подсчётом на каждом разряде.

    Аргументы:
        arr: список неотрицательных целых чисел

    Возвращает:
        list: отсортированный список

    Сложность: O(d × (n + 10)) = O(d × n), d — количество разрядов
    Память: O(n + 10) = O(n)
    Стабильна.

    Пример:
        >>> radix_sort([170, 45, 75, 90, 802, 24, 2, 66])
        [2, 24, 45, 66, 75, 90, 170, 802]
    """
    if not arr:
        return arr

    max_val = max(arr)
    exp = 1

    result = arr[:]
    while max_val // exp > 0:
        result = counting_sort_stable(result, key=lambda x, e=exp: (x // e) % 10)
        exp *= 10

    return result


# =============================================================================
# СЛИЯНИЕ K ОТСОРТИРОВАННЫХ МАССИВОВ
# =============================================================================

def merge_k_sorted(arrays: List[List[int]]) -> List[int]:
    """
    Слияние K отсортированных массивов.

    Использует min-heap для эффективного выбора наименьшего элемента.

    Аргументы:
        arrays: список отсортированных массивов

    Возвращает:
        list: объединённый отсортированный массив

    Сложность: O(N log K), N — суммарное количество элементов,
               K — количество массивов

    Пример:
        >>> merge_k_sorted([[1, 4, 7], [2, 5, 8], [3, 6, 9]])
        [1, 2, 3, 4, 5, 6, 7, 8, 9]
    """
    heap = []
    for i, arr in enumerate(arrays):
        if arr:
            heapq.heappush(heap, (arr[0], i, 0))   # (значение, массив, индекс)

    result = []
    while heap:
        val, arr_i, elem_i = heapq.heappop(heap)
        result.append(val)
        if elem_i + 1 < len(arrays[arr_i]):
            next_val = arrays[arr_i][elem_i + 1]
            heapq.heappush(heap, (next_val, arr_i, elem_i + 1))

    return result


# =============================================================================
# ПОРЯДКОВАЯ СТАТИСТИКА (QUICKSELECT)
# =============================================================================

def quickselect(arr: List[int], k: int) -> int:
    """
    K-й наименьший элемент (алгоритм Quickselect).

    Аналог Quicksort, но рекурсия только в нужную сторону.
    Изменяет массив на месте.

    Аргументы:
        arr: список чисел (будет изменён)
        k: порядковый номер (0-based, 0 = минимум)

    Возвращает:
        int: k-й наименьший элемент

    Сложность: O(n) среднее, O(n²) худшее (устраняется рандомизацией)

    Пример:
        >>> quickselect([3, 2, 1, 5, 6, 4], 1)
        2  # 2-й наименьший (0-based)
    """
    lo, hi = 0, len(arr) - 1

    while lo < hi:
        # Рандомизированный pivot
        pivot_i = random.randint(lo, hi)
        arr[pivot_i], arr[hi] = arr[hi], arr[pivot_i]

        p = _partition_lomuto(arr, lo, hi)

        if p == k:
            break
        elif p < k:
            lo = p + 1
        else:
            hi = p - 1

    return arr[k]


def kth_largest(nums: List[int], k: int) -> int:
    """
    K-й наибольший элемент.

    Обёртка над quickselect: k-й наибольший = (n-k)-й наименьший.

    Аргументы:
        nums: список чисел
        k: порядковый номер (1-based, 1 = максимум)

    Возвращает:
        int: k-й наибольший элемент

    Сложность: O(n) среднее

    Пример:
        >>> kth_largest([3, 2, 1, 5, 6, 4], 2)
        5
    """
    return quickselect(nums[:], len(nums) - k)


# =============================================================================
# СОРТИРОВКА ПО НЕСКОЛЬКИМ КРИТЕРИЯМ
# =============================================================================

def sort_students(students: List[Tuple[str, int, float]]) -> List[Tuple]:
    """
    Сортировка студентов по нескольким критериям.

    Критерии (по убыванию приоритета):
        1. Оценка по убыванию
        2. Средний балл по убыванию
        3. Имя по возрастанию

    Аргументы:
        students: список кортежей (имя, оценка, средний_балл)

    Возвращает:
        list: отсортированный список студентов

    Пример:
        >>> students = [("Анна", 5, 4.8), ("Борис", 5, 4.9), ("Вера", 4, 4.5)]
        >>> sort_students(students)
        [('Борис', 5, 4.9), ('Анна', 5, 4.8), ('Вера', 4, 4.5)]
    """
    return sorted(students, key=lambda s: (-s[1], -s[2], s[0]))


# =============================================================================
# ДЕМОНСТРАЦИЯ
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("СОРТИРОВКИ — РАСШИРЕННЫЙ РАЗБОР")
    print("=" * 60)

    original = [5, 3, 8, 1, 9, 2, 7, 4, 6]
    print(f"\nИсходный массив: {original}")

    print("\n[1] Quicksort (простой):")
    print(f"  {quicksort_simple(original)}")

    print("\n[2] Quicksort (in-place + random pivot):")
    arr = original[:]
    print(f"  {quicksort_inplace(arr)}")

    print("\n[3] Quicksort (3-way, с дубликатами):")
    arr3 = [2, 3, 2, 1, 2, 3, 1, 2]
    print(f"  Исходный: {arr3}")
    print(f"  Результат: {quicksort_3way(arr3[:])}")

    print("\n[4] Mergesort (Top-Down):")
    print(f"  {mergesort(original)}")

    print("\n[5] Mergesort (Bottom-Up, без рекурсии):")
    print(f"  {mergesort_bottomup(original)}")

    print("\n[6] Подсчёт инверсий:")
    inv_arr = [3, 1, 2]
    sorted_arr, inv_count = count_inversions(inv_arr)
    print(f"  Массив: {inv_arr}")
    print(f"  Инверсий: {inv_count} ({sorted_arr})")

    inv_arr2 = [5, 4, 3, 2, 1]
    _, inv_count2 = count_inversions(inv_arr2)
    print(f"  Массив {inv_arr2} → инверсий: {inv_count2}")

    print("\n[7] Heapsort:")
    arr_h = original[:]
    print(f"  {heapsort(arr_h)}")

    print("\n[8] Radix Sort:")
    rad = [170, 45, 75, 90, 802, 24, 2, 66]
    print(f"  Исходный: {rad}")
    print(f"  Результат: {radix_sort(rad)}")

    print("\n[9] Слияние K отсортированных массивов:")
    arrays = [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
    print(f"  Входные: {arrays}")
    print(f"  Результат: {merge_k_sorted(arrays)}")

    print("\n[10] Quickselect (K-й наименьший):")
    qs_arr = [3, 2, 1, 5, 6, 4]
    print(f"  Массив: {qs_arr}")
    print(f"  2-й наименьший (0-based k=1): {quickselect(qs_arr[:], 1)}")
    print(f"  2-й наибольший (k=2): {kth_largest(qs_arr[:], 2)}")

    print("\n[11] Многокритериальная сортировка студентов:")
    students = [
        ("Анна", 5, 4.8),
        ("Борис", 5, 4.9),
        ("Вера", 4, 4.5),
        ("Григорий", 5, 4.8),
    ]
    for s in sort_students(students):
        print(f"  {s[0]:12} оценка={s[1]}  ср.балл={s[2]}")
