"""
ПРЕФИКСНЫЕ СУММЫ (PREFIX SUMS)

Условие применения:
- Многократные запросы суммы на отрезках
- Подсчёт подмассивов с заданными свойствами
- Задачи на разность элементов

Суть метода:
Предварительно вычисляем массив prefix, где prefix[i] = сумма первых i элементов.
После этого сумма на любом отрезке [l, r] вычисляется за O(1):
    sum(l, r) = prefix[r+1] - prefix[l]

Сложность: O(n) на предвычисление, O(1) на каждый запрос

Ключевая идея:
Тратим O(n) времени один раз, чтобы каждый запрос выполнялся за O(1).
Это даёт огромный выигрыш при большом количестве запросов.

Обобщения:
- 2D префиксные суммы: сумма в прямоугольнике за O(1)
- Разностный массив: эффективные обновления на отрезке
"""


class PrefixSum:
    """
    Класс для быстрого вычисления сумм на отрезках.
    
    Сначала выполняется предвычисление за O(n),
    затем каждый запрос выполняется за O(1).
    
    Пример:
        >>> ps = PrefixSum([1, 2, 3, 4, 5])
        >>> ps.range_sum(1, 3)
        9
    """
    
    def __init__(self, arr):
        """
        Инициализация с предвычислением префиксных сумм.
        
        Аргументы:
            arr: список чисел
        
        Сложность: O(n) времени и памяти
        """
        self.prefix = [0] * (len(arr) + 1)
        for i in range(len(arr)):
            self.prefix[i + 1] = self.prefix[i] + arr[i]
    
    def range_sum(self, left, right):
        """
        Сумма на отрезке [left, right] включительно.
        
        Аргументы:
            left: левая граница (включительно)
            right: правая граница (включительно)
        
        Возвращает:
            число: сумма элементов на отрезке
        
        Сложность: O(1)
        """
        return self.prefix[right + 1] - self.prefix[left]


def count_subarrays_with_sum(arr, k):
    """
    Подсчёт количества подмассивов с суммой ровно k.
    
    Используем хеш-таблицу для хранения количества вхождений
    каждой префиксной суммы.
    
    Аргументы:
        arr: список чисел (могут быть отрицательные!)
        k: искомая сумма
    
    Возвращает:
        int: количество подмассивов с суммой k
    
    Сложность: O(n) по времени, O(n) по памяти
    
    Идея:
        Если prefix[j] - prefix[i] = k, то подмассив [i+1, j] имеет сумму k.
        Для каждого prefix[j] ищем, сколько раз встречалось prefix[j] - k.
    
    Пример:
        >>> count_subarrays_with_sum([1, 1, 1], 2)
        2
    """
    from collections import defaultdict
    
    count = 0
    prefix_sum = 0
    sum_count = defaultdict(int)
    sum_count[0] = 1  # Пустой префикс
    
    for num in arr:
        prefix_sum += num
        # Если (prefix_sum - k) встречался ранее, есть подмассив с суммой k
        count += sum_count[prefix_sum - k]
        sum_count[prefix_sum] += 1
    
    return count


def count_subarrays_sum_at_least_k(arr, k):
    """
    Количество подмассивов с суммой ≥ k.
    
    Для положительных чисел можно использовать скользящее окно.
    Для произвольных — монотонную очередь.
    
    Аргументы:
        arr: список положительных чисел
        k: минимальная сумма
    
    Возвращает:
        int: количество подмассивов
    
    Сложность: O(n) для положительных, O(n log n) для произвольных
    
    Пример:
        >>> count_subarrays_sum_at_least_k([2, 3, 1, 4], 5)
        5
    """
    n = len(arr)
    count = 0
    prefix = [0] * (n + 1)
    
    for i in range(n):
        prefix[i + 1] = prefix[i] + arr[i]
    
    # Для каждого правого края находим минимальный левый
    left = 0
    for right in range(1, n + 1):
        while left < right and prefix[right] - prefix[left] >= k:
            left += 1
        count += left
    
    return count


class PrefixSum2D:
    """
    Двумерные префиксные суммы.
    
    Позволяют вычислять сумму элементов в любом прямоугольнике за O(1).
    
    Пример:
        >>> matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        >>> ps = PrefixSum2D(matrix)
        >>> ps.rect_sum(0, 0, 1, 1)  # Сумма в прямоугольнике (0,0)-(1,1)
        12
    """
    
    def __init__(self, matrix):
        """
        Инициализация с предвычислением.
        
        Аргументы:
            matrix: двумерный список чисел
        
        Сложность: O(m × n) времени и памяти
        """
        if not matrix or not matrix[0]:
            self.prefix = [[0]]
            return
        
        rows, cols = len(matrix), len(matrix[0])
        self.prefix = [[0] * (cols + 1) for _ in range(rows + 1)]
        
        for i in range(rows):
            for j in range(cols):
                self.prefix[i + 1][j + 1] = (
                    self.prefix[i][j + 1] +
                    self.prefix[i + 1][j] -
                    self.prefix[i][j] +
                    matrix[i][j]
                )
    
    def rect_sum(self, r1, c1, r2, c2):
        """
        Сумма в прямоугольнике от (r1, c1) до (r2, c2) включительно.
        
        Сложность: O(1)
        """
        return (
            self.prefix[r2 + 1][c2 + 1] -
            self.prefix[r1][c2 + 1] -
            self.prefix[r2 + 1][c1] +
            self.prefix[r1][c1]
        )


class DifferenceArray:
    """
    Разностный массив для эффективных обновлений на отрезке.
    
    Вместо O(n) на каждое обновление отрезка — O(1).
    После всех обновлений восстанавливаем итоговый массив за O(n).
    
    Идея:
        Вместо хранения arr[i], храним diff[i] = arr[i] - arr[i-1].
        Добавление val на [l, r]: diff[l] += val, diff[r+1] -= val.
    
    Пример:
        >>> da = DifferenceArray([1, 2, 3, 4, 5])
        >>> da.add(1, 3, 10)  # Добавить 10 к элементам [1, 3]
        >>> da.get_result()
        [1, 12, 13, 14, 5]
    """
    
    def __init__(self, arr):
        """
        Инициализация разностного массива.
        
        Аргументы:
            arr: исходный список
        """
        self.n = len(arr)
        self.diff = [0] * self.n
        self.diff[0] = arr[0]
        
        for i in range(1, self.n):
            self.diff[i] = arr[i] - arr[i - 1]
    
    def add(self, left, right, value):
        """
        Добавить value ко всем элементам отрезка [left, right].
        
        Сложность: O(1)
        """
        self.diff[left] += value
        if right + 1 < self.n:
            self.diff[right + 1] -= value
    
    def get_result(self):
        """
        Получить итоговый массив после всех обновлений.
        
        Сложность: O(n)
        """
        result = [0] * self.n
        result[0] = self.diff[0]
        for i in range(1, self.n):
            result[i] = result[i - 1] + self.diff[i]
        return result


def find_pivot_index(nums):
    """
    Найти индекс, где сумма слева равна сумме справа.
    
    Используем префиксные суммы для эффективного вычисления.
    
    Аргументы:
        nums: список чисел
    
    Возвращает:
        int: индекс pivot или -1, если не найден
    
    Сложность: O(n) по времени, O(1) по памяти
    
    Пример:
        >>> find_pivot_index([1, 7, 3, 6, 5, 6])
        3
    """
    total = sum(nums)
    left_sum = 0
    
    for i, num in enumerate(nums):
        # right_sum = total - left_sum - num
        if left_sum == total - left_sum - num:
            return i
        left_sum += num
    
    return -1


def product_except_self(nums):
    """
    Произведение всех элементов, кроме текущего.
    
    Аналог префиксных сумм, но для произведения.
    
    Аргументы:
        nums: список чисел
    
    Возвращает:
        list: произведение всех элементов кроме nums[i]
    
    Сложность: O(n) по времени, O(1) дополнительной памяти
    
    Пример:
        >>> product_except_self([1, 2, 3, 4])
        [24, 12, 8, 6]
    """
    n = len(nums)
    result = [1] * n
    
    # Произведение слева от i
    left_product = 1
    for i in range(n):
        result[i] = left_product
        left_product *= nums[i]
    
    # Умножаем на произведение справа от i
    right_product = 1
    for i in range(n - 1, -1, -1):
        result[i] *= right_product
        right_product *= nums[i]
    
    return result


if __name__ == "__main__":
    print(__doc__)
    print("\n" + "="*50)
    
    # Демонстрация PrefixSum
    arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    ps = PrefixSum(arr)
    print(f"Массив: {arr}")
    print(f"Сумма [2, 5]: {ps.range_sum(2, 5)}")
    print(f"Сумма [0, 9]: {ps.range_sum(0, 9)}")
    
    # Демонстрация подсчёта подмассивов
    arr2 = [1, 1, 1]
    print(f"\nМассив: {arr2}")
    print(f"Подмассивов с суммой 2: {count_subarrays_with_sum(arr2, 2)}")
    
    # Демонстрация разностного массива
    arr3 = [1, 2, 3, 4, 5]
    da = DifferenceArray(arr3)
    da.add(1, 3, 10)
    print(f"\nИсходный: {arr3}")
    print(f"После добавления 10 к [1,3]: {da.get_result()}")
    
    # Демонстрация двумерных сумм
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    ps2d = PrefixSum2D(matrix)
    print(f"\nМатрица: {matrix}")
    print(f"Сумма прямоугольника (0,0)-(1,1): {ps2d.rect_sum(0, 0, 1, 1)}")
