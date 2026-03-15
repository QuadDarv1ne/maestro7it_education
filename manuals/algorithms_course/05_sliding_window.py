"""
СКОЛЬЗЯЩЕЕ ОКНО (SLIDING WINDOW)

Условие применения:
- Задачи на подмассивы или подстроки
- Поиск оптимального непрерывного отрезка

Суть метода:
Непрерывный диапазон элементов ("окно") скользит по данным.
При сдвиге окна обновляем результат за O(1), а не пересчитываем заново.

Сложность: O(n) по времени, O(k) или O(1) по памяти

Два типа окон:
1. Фиксированного размера — длина окна k не меняется
   Пример: найти максимальную сумму подмассива длины k
2. Переменного размера — окно расширяется и сжимается
   Пример: найти минимальный подмассив с суммой ≥ target

Ключевая идея:
Вместо O(n²) проверок всех подмассивов — один проход O(n) с обновлением.
"""


def max_sum_subarray_fixed(arr, k):
    """
    Максимальная сумма подмассива фиксированной длины k.
    
    Классический пример скользящего окна фиксированного размера.
    
    Аргументы:
        arr: список чисел
        k: длина подмассива
    
    Возвращает:
        int: максимальная сумма подмассива длины k
             или None, если k > len(arr)
    
    Сложность: O(n) по времени, O(1) по памяти
    
    Пример:
        >>> max_sum_subarray_fixed([2, 1, 5, 1, 3, 2], 3)
        9
    """
    if k > len(arr):
        return None
    
    # Сумма первого окна
    window_sum = sum(arr[:k])
    max_sum = window_sum
    
    # Скользим по массиву
    for i in range(k, len(arr)):
        # Вычитаем уходящий элемент, добавляем новый
        window_sum = window_sum - arr[i - k] + arr[i]
        max_sum = max(max_sum, window_sum)
    
    return max_sum


def min_length_subarray_sum(arr, target):
    """
    Минимальная длина подмассива с суммой ≥ target.
    
    Скользящее окно переменного размера: расширяется вправо,
    затем сжимается слева для минимизации.
    
    Аргументы:
        arr: список положительных чисел
        target: целевая сумма
    
    Возвращает:
        int: минимальная длина или 0, если не найдено
    
    Сложность: O(n) по времени, O(1) по памяти
    
    Пример:
        >>> min_length_subarray_sum([2, 3, 1, 2, 4, 3], 7)
        2
    """
    left = 0
    window_sum = 0
    min_length = float('inf')
    
    for right in range(len(arr)):
        window_sum += arr[right]
        
        # Сжимаем окно слева, пока сумма >= target
        while window_sum >= target:
            min_length = min(min_length, right - left + 1)
            window_sum -= arr[left]
            left += 1
    
    return min_length if min_length != float('inf') else 0


def longest_substring_without_repeats(s):
    """
    Самая длинная подстрока без повторяющихся символов.
    
    Используем словарь для хранения последней позиции каждого символа.
    
    Аргументы:
        s: строка
    
    Возвращает:
        int: длина самой длинной подстроки без повторений
    
    Сложность: O(n) по времени, O(min(n, m)) по памяти (m — размер алфавита)
    
    Пример:
        >>> longest_substring_without_repeats("abcabcbb")
        3
        >>> longest_substring_without_repeats("bbbbb")
        1
    """
    char_index = {}  # Последняя позиция каждого символа
    left = 0
    max_length = 0
    
    for right, char in enumerate(s):
        # Если символ уже в окне — сдвигаем левую границу
        if char in char_index and char_index[char] >= left:
            left = char_index[char] + 1
        
        char_index[char] = right
        max_length = max(max_length, right - left + 1)
    
    return max_length


def longest_substring_k_distinct(s, k):
    """
    Самая длинная подстрока с максимум k различными символами.
    
    Аргументы:
        s: строка
        k: максимальное количество различных символов
    
    Возвращает:
        int: длина самой длинной подстроки
    
    Сложность: O(n) по времени, O(k) по памяти
    
    Пример:
        >>> longest_substring_k_distinct("eceba", 2)
        3
    """
    if k == 0:
        return 0
    
    char_count = {}
    left = 0
    max_length = 0
    
    for right, char in enumerate(s):
        char_count[char] = char_count.get(char, 0) + 1
        
        # Сжимаем окно, пока количество различных символов > k
        while len(char_count) > k:
            left_char = s[left]
            char_count[left_char] -= 1
            if char_count[left_char] == 0:
                del char_count[left_char]
            left += 1
        
        max_length = max(max_length, right - left + 1)
    
    return max_length


def min_window_substring(s, t):
    """
    Минимальное окно в s, содержащее все символы t.
    
    Классическая задача на скользящее окно переменного размера.
    
    Аргументы:
        s: исходная строка
        t: строка с обязательными символами
    
    Возвращает:
        str: минимальная подстрока или пустая строка
    
    Сложность: O(|s| + |t|) по времени, O(|t|) по памяти
    
    Пример:
        >>> min_window_substring("ADOBECODEBANC", "ABC")
        'BANC'
    """
    if not s or not t:
        return ""
    
    from collections import Counter
    
    need = Counter(t)
    missing = len(t)  # Сколько символов ещё нужно найти
    left = 0
    min_len = float('inf')
    min_start = 0
    
    for right, char in enumerate(s):
        if need[char] > 0:
            missing -= 1
        need[char] -= 1
        
        # Все символы найдены — сжимаем окно
        while missing == 0:
            if right - left + 1 < min_len:
                min_len = right - left + 1
                min_start = left
            
            need[s[left]] += 1
            if need[s[left]] > 0:
                missing += 1
            left += 1
    
    return s[min_start:min_start + min_len] if min_len != float('inf') else ""


def find_all_anagrams(s, p):
    """
    Найти все стартовые индексы анаграмм строки p в строке s.
    
    Анаграмма — перестановка символов. Используем фиксированное окно.
    
    Аргументы:
        s: исходная строка
        p: образец-анаграмма
    
    Возвращает:
        list: список стартовых индексов
    
    Сложность: O(|s| + |p|) по времени
    
    Пример:
        >>> find_all_anagrams("cbaebabacd", "abc")
        [0, 6]
    """
    from collections import Counter
    
    if len(p) > len(s):
        return []
    
    p_count = Counter(p)
    window_count = Counter(s[:len(p)])
    result = []
    
    if window_count == p_count:
        result.append(0)
    
    # Скользим окном
    for i in range(len(p), len(s)):
        # Добавляем новый символ
        window_count[s[i]] = window_count.get(s[i], 0) + 1
        
        # Удаляем уходящий символ
        left_char = s[i - len(p)]
        window_count[left_char] -= 1
        if window_count[left_char] == 0:
            del window_count[left_char]
        
        if window_count == p_count:
            result.append(i - len(p) + 1)
    
    return result


def max_consecutive_ones_with_flip(nums, k):
    """
    Максимальная последовательность единиц, если можно инвертировать k нулей.
    
    Аргументы:
        nums: список из 0 и 1
        k: максимальное количество инверсий
    
    Возвращает:
        int: максимальная длина последовательности единиц
    
    Сложность: O(n) по времени, O(1) по памяти
    
    Пример:
        >>> max_consecutive_ones_with_flip([1,1,1,0,0,0,1,1,1,1,0], 2)
        6
    """
    left = 0
    zeros = 0
    max_length = 0
    
    for right in range(len(nums)):
        if nums[right] == 0:
            zeros += 1
        
        # Слишком много нулей — сжимаем окно
        while zeros > k:
            if nums[left] == 0:
                zeros -= 1
            left += 1
        
        max_length = max(max_length, right - left + 1)
    
    return max_length


if __name__ == "__main__":
    print(__doc__)
    print("\n" + "="*50)
    
    # Демонстрация фиксированного окна
    arr = [2, 1, 5, 1, 3, 2]
    k = 3
    print(f"Массив: {arr}")
    print(f"Максимальная сумма подмассива длины {k}: {max_sum_subarray_fixed(arr, k)}")
    
    # Демонстрация переменного окна
    arr2 = [2, 3, 1, 2, 4, 3]
    target = 7
    print(f"\nМассив: {arr2}")
    print(f"Минимальная длина подмассива с суммой ≥ {target}: {min_length_subarray_sum(arr2, target)}")
    
    # Демонстрация подстроки без повторений
    s = "abcabcbb"
    print(f"\nСтрока: '{s}'")
    print(f"Самая длинная подстрока без повторений: {longest_substring_without_repeats(s)}")
    
    # Демонстрация минимального окна
    s1, t = "ADOBECODEBANC", "ABC"
    print(f"\nСтрока: '{s1}', образец: '{t}'")
    print(f"Минимальное окно: '{min_window_substring(s1, t)}'")
