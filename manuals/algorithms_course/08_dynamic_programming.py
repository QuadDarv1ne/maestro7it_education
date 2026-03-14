"""
ДИНАМИЧЕСКОЕ ПРОГРАММИРОВАНИЕ (DYNAMIC PROGRAMMING)

Динамическое программирование — метод решения задач путём разбиения
на перекрывающиеся подзадачи и сохранения результатов для повторного использования.

Ключевые концепции:
1. Перекрывающиеся подзадачи — одни и те же подзадачи решаются многократно
2. Оптимальная подструктура — оптимальное решение содержит оптимальные решения подзадач
3. Мемоизация — сохранение результатов (сверху-вниз)
4. Табуляция — построение таблицы результатов (снизу-вверх)

Два подхода:
- Сверху-вниз (Top-Down): рекурсия + мемоизация
- Снизу-вверх (Bottom-Up): итеративное заполнение таблицы

Классические задачи:
- Числа Фибоначчи
- Задача о рюкзаке
- Наибольшая общая подпоследовательность
- Редакционное расстояние
- Задача о монетах
- Наибольшая возрастающая подпоследовательность
"""


# ===== ЧИСЛА ФИБОНАЧЧИ =====

def fibonacci_naive(n):
    """
    Наивная рекурсивная реализация чисел Фибоначчи.
    
    ВНИМАНИЕ: Экспоненциальная сложность!
    Показывает проблему перекрывающихся подзадач.
    
    Сложность: O(2^n) — катастрофически медленно
    """
    if n <= 1:
        return n
    return fibonacci_naive(n - 1) + fibonacci_naive(n - 2)


def fibonacci_memo(n, memo=None):
    """
    Числа Фибоначчи с мемоизацией (Top-Down).
    
    Сохраняем результаты каждого вызова в словаре.
    При повторном вызове берём готовый результат.
    
    Аргументы:
        n: номер числа Фибоначчи
        memo: словарь для хранения результатов
    
    Возвращает:
        int: n-е число Фибоначчи
    
    Сложность: O(n) по времени, O(n) по памяти
    
    Пример:
        >>> fibonacci_memo(50)
        12586269025
    """
    if memo is None:
        memo = {}
    
    if n in memo:
        return memo[n]
    
    if n <= 1:
        return n
    
    memo[n] = fibonacci_memo(n - 1, memo) + fibonacci_memo(n - 2, memo)
    return memo[n]


def fibonacci_dp(n):
    """
    Числа Фибоначчи методом Bottom-Up.
    
    Итеративно строим таблицу от базовых случаев до n.
    Оптимальный вариант по памяти можно улучшить до O(1).
    
    Аргументы:
        n: номер числа Фибоначчи
    
    Возвращает:
        int: n-е число Фибоначчи
    
    Сложность: O(n) по времени, O(1) по памяти
    
    Пример:
        >>> fibonacci_dp(50)
        12586269025
    """
    if n <= 1:
        return n
    
    prev, curr = 0, 1
    for _ in range(2, n + 1):
        prev, curr = curr, prev + curr
    
    return curr


# ===== ЗАДАЧА О РЮКЗАКЕ =====

def knapsack_01(weights, values, capacity):
    """
    Классическая задача о рюкзаке 0/1.
    
    Дано n предметов с весами и ценностями.
    Рюкзак имеет ограниченную вместимость.
    Каждый предмет можно взять или не взять (0 или 1).
    Максимизировать ценность.
    
    Аргументы:
        weights: список весов предметов
        values: список ценностей предметов
        capacity: вместимость рюкзака
    
    Возвращает:
        int: максимальная ценность
    
    Сложность: O(n × capacity) по времени и памяти
    
    Пример:
        >>> knapsack_01([1, 3, 4, 5], [1, 4, 5, 7], 7)
        9
    """
    n = len(weights)
    # dp[i][w] = максимальная ценность первых i предметов при вместимости w
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            # Не берём предмет i
            dp[i][w] = dp[i - 1][w]
            
            # Берём предмет i (если помещается)
            if weights[i - 1] <= w:
                dp[i][w] = max(
                    dp[i][w],
                    dp[i - 1][w - weights[i - 1]] + values[i - 1]
                )
    
    return dp[n][capacity]


def knapsack_01_optimized(weights, values, capacity):
    """
    Задача о рюкзаке с оптимизацией памяти.
    
    Используем только один одномерный массив.
    Важно: перебираем вместимость справа налево!
    
    Сложность: O(n × capacity) по времени, O(capacity) по памяти
    """
    dp = [0] * (capacity + 1)
    
    for weight, value in zip(weights, values):
        for w in range(capacity, weight - 1, -1):
            dp[w] = max(dp[w], dp[w - weight] + value)
    
    return dp[capacity]


# ===== ЗАДАЧА О МОНЕТАХ =====

def coin_change_min_coins(coins, amount):
    """
    Минимальное количество монет для суммы.
    
    Даны номиналы монет и сумма. Найти минимальное
    количество монет, дающих эту сумму.
    
    Аргументы:
        coins: список номиналов монет
        amount: целевая сумма
    
    Возвращает:
        int: минимальное количество монет или -1, если невозможно
    
    Сложность: O(amount × len(coins))
    
    Пример:
        >>> coin_change_min_coins([1, 2, 5], 11)
        3
    """
    # dp[a] = минимальное количество монет для суммы a
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    
    for a in range(1, amount + 1):
        for coin in coins:
            if coin <= a:
                dp[a] = min(dp[a], dp[a - coin] + 1)
    
    return dp[amount] if dp[amount] != float('inf') else -1


def coin_change_ways(coins, amount):
    """
    Количество способов составить сумму из монет.
    
    Аргументы:
        coins: список номиналов монет
        amount: целевая сумма
    
    Возвращает:
        int: количество способов
    
    Сложность: O(amount × len(coins))
    
    Пример:
        >>> coin_change_ways([1, 2, 5], 5)
        4
    """
    dp = [0] * (amount + 1)
    dp[0] = 1  # Один способ составить сумму 0 — не брать монеты
    
    for coin in coins:
        for a in range(coin, amount + 1):
            dp[a] += dp[a - coin]
    
    return dp[amount]


# ===== НАИБОЛЬШАЯ ОБЩАЯ ПОДПОСЛЕДОВАТЕЛЬНОСТЬ =====

def longest_common_subsequence(text1, text2):
    """
    Наибольшая общая подпоследовательность (LCS).
    
    Найти длину самой длинной подпоследовательности,
    общей для двух строк.
    
    Аргументы:
        text1: первая строка
        text2: вторая строка
    
    Возвращает:
        int: длина LCS
    
    Сложность: O(m × n) по времени и памяти
    
    Пример:
        >>> longest_common_subsequence("abcde", "ace")
        3
    """
    m, n = len(text1), len(text2)
    # dp[i][j] = LCS длины text1[:i] и text2[:j]
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    return dp[m][n]


def lcs_string(text1, text2):
    """
    Получить саму наибольшую общую подпоследовательность.
    
    Возвращает:
        str: строка LCS
    """
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    # Восстановление LCS
    lcs = []
    i, j = m, n
    while i > 0 and j > 0:
        if text1[i - 1] == text2[j - 1]:
            lcs.append(text1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    
    return ''.join(reversed(lcs))


# ===== РЕДАКЦИОННОЕ РАССТОЯНИЕ =====

def edit_distance(word1, word2):
    """
    Редакционное расстояние (Левенштейна).
    
    Минимальное количество операций (вставка, удаление, замена)
    для превращения word1 в word2.
    
    Аргументы:
        word1: первая строка
        word2: вторая строка
    
    Возвращает:
        int: редакционное расстояние
    
    Сложность: O(m × n)
    
    Пример:
        >>> edit_distance("horse", "ros")
        3
    """
    m, n = len(word1), len(word2)
    # dp[i][j] = расстояние между word1[:i] и word2[:j]
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Базовые случаи
    for i in range(m + 1):
        dp[i][0] = i  # i удалений
    for j in range(n + 1):
        dp[0][j] = j  # j вставок
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]  # Совпадение
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],      # Удаление
                    dp[i][j - 1],      # Вставка
                    dp[i - 1][j - 1]   # Замена
                )
    
    return dp[m][n]


# ===== НАИБОЛЬШАЯ ВОЗРАСТАЮЩАЯ ПОДПОСЛЕДОВАТЕЛЬНОСТЬ =====

def longest_increasing_subsequence(nums):
    """
    Наибольшая возрастающая подпоследовательность (LIS).
    
    Аргументы:
        nums: список чисел
    
    Возвращает:
        int: длина LIS
    
    Сложность: O(n²) — классический DP
    
    Пример:
        >>> longest_increasing_subsequence([10, 9, 2, 5, 3, 7, 101, 18])
        4
    """
    if not nums:
        return 0
    
    n = len(nums)
    # dp[i] = длина LIS, заканчивающейся в позиции i
    dp = [1] * n
    
    for i in range(1, n):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    
    return max(dp)


def lis_optimized(nums):
    """
    LIS с бинарным поиском. O(n log n).
    
    Используем массив tails, где tails[i] = минимальный
    последний элемент LIS длины i+1.
    """
    import bisect
    
    tails = []
    for num in nums:
        pos = bisect.bisect_left(tails, num)
        if pos == len(tails):
            tails.append(num)
        else:
            tails[pos] = num
    
    return len(tails)


# ===== СУММА ПОДМНОЖЕСТВА =====

def subset_sum(nums, target):
    """
    Задача о сумме подмножества.
    
    Можно ли выбрать подмножество с суммой ровно target?
    
    Аргументы:
        nums: список положительных чисел
        target: целевая сумма
    
    Возвращает:
        bool: True, если можно набрать сумму
    
    Сложность: O(n × target)
    
    Пример:
        >>> subset_sum([3, 34, 4, 12, 5, 2], 9)
        True
    """
    # dp[s] = можно ли набрать сумму s
    dp = [False] * (target + 1)
    dp[0] = True  # Пустое подмножество даёт сумму 0
    
    for num in nums:
        for s in range(target, num - 1, -1):
            dp[s] = dp[s] or dp[s - num]
    
    return dp[target]


# ===== УНИКАЛЬНЫЕ ПУТИ =====

def unique_paths(m, n):
    """
    Количество уникальных путей в сетке.
    
    Робот в левом верхнем углу сетки m×n.
    Может двигаться только вправо или вниз.
    Сколько путей до правого нижнего угла?
    
    Аргументы:
        m: количество строк
        n: количество столбцов
    
    Возвращает:
        int: количество уникальных путей
    
    Сложность: O(m × n)
    
    Пример:
        >>> unique_paths(3, 7)
        28
    """
    # dp[i][j] = количество путей до клетки (i, j)
    dp = [[1] * n for _ in range(m)]
    
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1]
    
    return dp[m - 1][n - 1]


def unique_paths_optimized(m, n):
    """Оптимизация памяти до O(n)."""
    dp = [1] * n
    
    for _ in range(1, m):
        for j in range(1, n):
            dp[j] += dp[j - 1]
    
    return dp[n - 1]


# ===== РАЗРЕЗ СТРОКИ =====

def palindrome_partitioning_min_cuts(s):
    """
    Минимальное количество разрезов для палиндромного разбиения.
    
    Аргументы:
        s: строка
    
    Возвращает:
        int: минимальное количество разрезов
    
    Сложность: O(n²)
    
    Пример:
        >>> palindrome_partitioning_min_cuts("aab")
        1
    """
    n = len(s)
    if n == 0:
        return 0
    
    # is_pal[i][j] = True, если s[i:j+1] — палиндром
    is_pal = [[False] * n for _ in range(n)]
    
    # Все подстроки длины 1 — палиндромы
    for i in range(n):
        is_pal[i][i] = True
    
    # Подстроки длины 2
    for i in range(n - 1):
        if s[i] == s[i + 1]:
            is_pal[i][i + 1] = True
    
    # Подстроки длины >= 3
    for length in range(3, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j] and is_pal[i + 1][j - 1]:
                is_pal[i][j] = True
    
    # dp[i] = минимальное разрезов для s[:i+1]
    dp = [0] * n
    
    for i in range(n):
        if is_pal[0][i]:
            dp[i] = 0  # Вся строка s[:i+1] — палиндром
        else:
            dp[i] = i  # Максимум i разрезов
            for j in range(i):
                if is_pal[j + 1][i]:
                    dp[i] = min(dp[i], dp[j] + 1)
    
    return dp[n - 1]


if __name__ == "__main__":
    print(__doc__)
    print("\n" + "="*60)
    
    # Тест Фибоначчи
    print("Фибоначчи:")
    print(f"  F(40) мемоизация: {fibonacci_memo(40)}")
    print(f"  F(40) DP: {fibonacci_dp(40)}")
    
    # Тест рюкзака
    print("\nЗадача о рюкзаке:")
    weights = [1, 3, 4, 5]
    values = [1, 4, 5, 7]
    capacity = 7
    print(f"  Веса: {weights}, Ценности: {values}, Вместимость: {capacity}")
    print(f"  Максимальная ценность: {knapsack_01(weights, values, capacity)}")
    
    # Тест монет
    print("\nЗадача о монетах:")
    coins = [1, 2, 5]
    amount = 11
    print(f"  Номиналы: {coins}, Сумма: {amount}")
    print(f"  Минимум монет: {coin_change_min_coins(coins, amount)}")
    print(f"  Количество способов для 5: {coin_change_ways(coins, 5)}")
    
    # Тест LCS
    print("\nНаибольшая общая подпоследовательность:")
    print(f"  LCS('abcde', 'ace') = '{lcs_string('abcde', 'ace')}'")
    
    # Тест LIS
    print("\nНаибольшая возрастающая подпоследовательность:")
    nums = [10, 9, 2, 5, 3, 7, 101, 18]
    print(f"  LIS {nums} = {longest_increasing_subsequence(nums)}")
    
    # Тест путей
    print("\nУникальные пути в сетке 3×7:")
    print(f"  Количество путей: {unique_paths(3, 7)}")
