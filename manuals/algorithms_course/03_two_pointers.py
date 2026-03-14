"""
МЕТОД ДВУХ УКАЗАТЕЛЕЙ (TWO POINTERS)

Условие применения:
- Отсортированный массив
- Задачи на поиск пары элементов
- Задачи на подстроки/подмассивы
- Удаление элементов in-place

Суть метода:
Используем два индекса (указателя), которые движутся по массиву.
Указатели могут двигаться навстречу друг другу или в одном направлении.

Сложность: O(n) по времени, O(1) по дополнительной памяти

Преимущество:
Позволяет снизить сложность с O(n²) до O(n) для многих задач на пары.

Два основных варианта:
1. Указатели навстречу — для поиска пары в отсортированном массиве
2. Указатели в одном направлении — для удаления дубликатов, скользящего окна
"""


def two_sum_sorted(nums, target):
    """
    Поиск двух чисел с заданной суммой в отсортированном массиве.
    
    Возвращает индексы двух чисел, которые в сумме дают target.
    
    Аргументы:
        nums: отсортированный список чисел
        target: искомая сумма
    
    Возвращает:
        list: [index1, index2] или пустой список, если пара не найдена
    
    Сложность: O(n) по времени, O(1) по памяти
    
    Пример:
        >>> two_sum_sorted([2, 7, 11, 15], 9)
        [0, 1]
    """
    left, right = 0, len(nums) - 1
    
    while left < right:
        current_sum = nums[left] + nums[right]
        
        if current_sum == target:
            return [left, right]
        elif current_sum < target:
            left += 1   # Сумма мала — берём большее число слева
        else:
            right -= 1  # Сумма велика — берём меньшее число справа
    
    return []  # Пара не найдена


def max_water_container(height):
    """
    Задача о контейнере с водой.
    
    Найти две вертикальные линии, которые вместе с осью X образуют
    контейнер, вмещающий максимум воды.
    
    Аргументы:
        height: список высот вертикальных линий
    
    Возвращает:
        int: максимальная площадь воды
    
    Сложность: O(n) по времени, O(1) по памяти
    
    Пример:
        >>> max_water_container([1, 8, 6, 2, 5, 4, 8, 3, 7])
        49
    """
    left, right = 0, len(height) - 1
    max_area = 0
    
    while left < right:
        # Площадь = ширина × минимальная высота
        width = right - left
        current_area = width * min(height[left], height[right])
        max_area = max(max_area, current_area)
        
        # Сдвигаем указатель с меньшей высотой
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    
    return max_area


def remove_duplicates_sorted(nums):
    """
    Удаление дубликатов из отсортированного массива in-place.
    
    Аргументы:
        nums: отсортированный список (изменяется на месте)
    
    Возвращает:
        int: новая длина массива без дубликатов
    
    Сложность: O(n) по времени, O(1) по памяти
    
    Пример:
        >>> nums = [1, 1, 2, 2, 2, 3, 4, 4]
        >>> remove_duplicates_sorted(nums)
        5
        >>> nums[:5]
        [1, 2, 3, 4]
    """
    if not nums:
        return 0
    
    slow = 0  # Позиция для записи уникального элемента
    
    for fast in range(1, len(nums)):
        if nums[fast] != nums[slow]:
            slow += 1
            nums[slow] = nums[fast]
    
    return slow + 1


def is_palindrome(s):
    """
    Проверка строки на палиндром.
    
    Аргументы:
        s: строка для проверки
    
    Возвращает:
        bool: True если строка — палиндром
    
    Сложность: O(n) по времени, O(1) по памяти
    
    Пример:
        >>> is_palindrome("racecar")
        True
        >>> is_palindrome("hello")
        False
    """
    left, right = 0, len(s) - 1
    
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    
    return True


def three_sum(nums):
    """
    Поиск всех уникальных троек с нулевой суммой.
    
    Аргументы:
        nums: список чисел
    
    Возвращает:
        list: список троек [num1, num2, num3], сумма которых равна 0
    
    Сложность: O(n²) по времени, O(1) дополнительной памяти
    
    Пример:
        >>> three_sum([-1, 0, 1, 2, -1, -4])
        [[-1, -1, 2], [-1, 0, 1]]
    """
    nums.sort()
    result = []
    n = len(nums)
    
    for i in range(n - 2):
        # Пропускаем дубликаты для первого элемента
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        
        # Два указателя для поиска пары
        left, right = i + 1, n - 1
        
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            
            if total < 0:
                left += 1
            elif total > 0:
                right -= 1
            else:
                result.append([nums[i], nums[left], nums[right]])
                
                # Пропускаем дубликаты
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                
                left += 1
                right -= 1
    
    return result


def move_zeros(nums):
    """
    Перемещение всех нулей в конец массива in-place.
    
    Аргументы:
        nums: список чисел (изменяется на месте)
    
    Возвращает:
        None (массив изменяется in-place)
    
    Сложность: O(n) по времени, O(1) по памяти
    
    Пример:
        >>> nums = [0, 1, 0, 3, 12]
        >>> move_zeros(nums)
        >>> nums
        [1, 3, 12, 0, 0]
    """
    slow = 0  # Позиция для записи ненулевого элемента
    
    for fast in range(len(nums)):
        if nums[fast] != 0:
            nums[slow], nums[fast] = nums[fast], nums[slow]
            slow += 1


if __name__ == "__main__":
    print(__doc__)
    print("\n" + "="*50)
    
    # Демонстрация two_sum_sorted
    arr = [2, 7, 11, 15]
    print(f"Массив: {arr}")
    print(f"Поиск суммы 9: {two_sum_sorted(arr, 9)}")
    
    # Демонстрация max_water_container
    heights = [1, 8, 6, 2, 5, 4, 8, 3, 7]
    print(f"\nВысоты: {heights}")
    print(f"Максимальная площадь воды: {max_water_container(heights)}")
    
    # Демонстрация three_sum
    nums = [-1, 0, 1, 2, -1, -4]
    print(f"\nМассив: {nums}")
    print(f"Тройки с суммой 0: {three_sum(nums)}")
