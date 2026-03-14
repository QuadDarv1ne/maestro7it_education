"""
БИНАРНЫЙ ПОИСК (BINARY SEARCH)

Условие применения: массив отсортирован.

Суть алгоритма:
Берём середину массива, сравниваем с искомым значением, отбрасываем половину массива.
Повторяем, пока не найдём элемент или не останется элементов.

Сложность: O(log n)

Почему это эффективно?
В массиве из 1 000 000 000 элементов:
- Линейный поиск: до 1 000 000 000 сравнений
- Бинарный поиск: максимум 30 сравнений (log₂(10⁹) ≈ 30)

Вариации бинарного поиска:
1. Классический — найти индекс элемента
2. lower_bound — первый элемент ≥ target (левая граница)
3. upper_bound — первый элемент > target (правая граница)
"""


def binary_search(arr, target):
    """
    Классический бинарный поиск.
    
    Возвращает индекс target в отсортированном массиве arr.
    Если элемент не найден, возвращает -1.
    
    Аргументы:
        arr: отсортированный список чисел
        target: искомое значение
    
    Возвращает:
        int: индекс элемента или -1
    
    Сложность: O(log n) по времени, O(1) по памяти
    
    Пример:
        >>> binary_search([1, 3, 5, 7, 9], 5)
        2
        >>> binary_search([1, 3, 5, 7, 9], 4)
        -1
    """
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2  # Индекс середины
        
        if arr[mid] == target:
            return mid              # Элемент найден!
        elif arr[mid] < target:
            left = mid + 1          # Ищем в правой половине
        else:
            right = mid - 1         # Ищем в левой половине
    
    return -1  # Элемент не найден


def lower_bound(arr, target):
    """
    Поиск левой границы (lower bound).
    
    Находит индекс первого элемента, который больше или равен target.
    Если все элементы меньше target, возвращает len(arr).
    
    Аргументы:
        arr: отсортированный список
        target: искомое значение
    
    Возвращает:
        int: индекс первого элемента >= target
    
    Сложность: O(log n)
    
    Пример:
        >>> lower_bound([1, 2, 2, 2, 3, 4], 2)
        1
        >>> lower_bound([1, 2, 3], 5)
        3
    """
    left, right = 0, len(arr)
    
    while left < right:
        mid = (left + right) // 2
        if arr[mid] < target:
            left = mid + 1
        else:
            right = mid
    
    return left


def upper_bound(arr, target):
    """
    Поиск правой границы (upper bound).
    
    Находит индекс первого элемента, который строго больше target.
    Если все элементы меньше или равны target, возвращает len(arr).
    
    Аргументы:
        arr: отсортированный список
        target: искомое значение
    
    Возвращает:
        int: индекс первого элемента > target
    
    Сложность: O(log n)
    
    Пример:
        >>> upper_bound([1, 2, 2, 2, 3, 4], 2)
        4
    """
    left, right = 0, len(arr)
    
    while left < right:
        mid = (left + right) // 2
        if arr[mid] <= target:
            left = mid + 1
        else:
            right = mid
    
    return left


def count_in_range(arr, low, high):
    """
    Подсчёт количества элементов в диапазоне [low, high] включительно.
    
    Использует lower_bound и upper_bound для эффективного подсчёта.
    
    Аргументы:
        arr: отсортированный список
        low: нижняя граница диапазона
        high: верхняя граница диапазона
    
    Возвращает:
        int: количество элементов в диапазоне
    
    Сложность: O(log n)
    
    Пример:
        >>> count_in_range([1, 2, 2, 3, 3, 3, 4, 5], 2, 3)
        5
    """
    return upper_bound(arr, high) - lower_bound(arr, low)


def binary_search_answer(left, right, check):
    """
    Бинарный поиск по ответу.
    
    Находит минимальное значение в диапазоне [left, right],
    для которого функция check возвращает True.
    
    Аргументы:
        left: левая граница поиска
        right: правая граница поиска
        check: функция, принимающая значение и возвращающая bool
    
    Возвращает:
        минимальное значение, для которого check(value) == True
    
    Сложность: O(log(right - left)) вызовов check
    
    Пример использования:
        # Найти минимальную скорость для прибытия вовремя
        >>> binary_search_answer(1, 100, lambda x: x >= 50)
        50
    """
    while left < right:
        mid = (left + right) // 2
        if check(mid):
            right = mid
        else:
            left = mid + 1
    return left


if __name__ == "__main__":
    print(__doc__)
    print("\n" + "="*50)
    
    # Демонстрация работы
    arr = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
    print(f"Массив: {arr}")
    
    # Классический поиск
    print(f"\nПоиск 23: индекс = {binary_search(arr, 23)}")
    print(f"Поиск 1: индекс = {binary_search(arr, 1)}")
    
    # Поиск границ
    arr_with_dups = [1, 2, 2, 2, 3, 4, 4, 5]
    print(f"\nМассив с дубликатами: {arr_with_dups}")
    print(f"lower_bound(2) = {lower_bound(arr_with_dups, 2)}")
    print(f"upper_bound(2) = {upper_bound(arr_with_dups, 2)}")
    print(f"Количество двоек: {count_in_range(arr_with_dups, 2, 2)}")
