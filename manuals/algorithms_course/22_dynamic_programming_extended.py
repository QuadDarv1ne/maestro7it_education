"""
ДИНАМИЧЕСКОЕ ПРОГРАММИРОВАНИЕ — РАСШИРЕННЫЙ РАЗБОР (DP EXTENDED)

Глава 10 учебного пособия.

Темы:
- 1D DP: классические задачи (Fibonacci, House Robber, Jump Game)
- 2D DP: редакционное расстояние, наибольшая общая подпоследовательность
- Задача о рюкзаке (0/1, unbounded, multiple)
- DP на интервалах (Matrix Chain, Burst Balloons)
- DP на подмасках (Bitmask DP)
- Backtracking с мемоизацией (Word Break, Palindrome Partitioning)
- Оптимизация памяти DP
"""

from functools import lru_cache
from typing import List, Dict, Tuple, Optional


# =============================================================================
# 1D ДИНАМИЧЕСКОЕ ПРОГРАММИРОВАНИЕ
# =============================================================================

def climb_stairs(n: int) -> int:
    """
    Количество способов подняться на n ступеней (шаг 1 или 2).

    Аргументы:
        n: количество ступеней

    Возвращает:
        int: количество способов

    Сложность: O(n) по времени, O(1) по памяти

    Математически идентично числам Фибоначчи.

    Пример:
        >>> climb_stairs(5)
        8
    """
    if n <= 2:
        return n
    a, b = 1, 2
    for _ in range(3, n + 1):
        a, b = b, a + b
    return b


def house_robber(nums: List[int]) -> int:
    """
    Задача о грабителе: максимальная сумма без смежных домов.

    Нельзя грабить два соседних дома. Найти максимальную добычу.

    Аргументы:
        nums: список сумм в каждом доме

    Возвращает:
        int: максимальная добыча

    Сложность: O(n) по времени, O(1) по памяти

    Рекуррентность:
        dp[i] = max(dp[i-1], dp[i-2] + nums[i])

    Пример:
        >>> house_robber([2, 7, 9, 3, 1])
        12  # 2 + 9 + 1
    """
    prev2 = prev1 = 0
    for num in nums:
        prev2, prev1 = prev1, max(prev1, prev2 + num)
    return prev1


def house_robber_circle(nums: List[int]) -> int:
    """
    Задача о грабителе: дома расположены по кругу.

    Первый и последний дом смежны.
    Решение: max(robber(nums[:-1]), robber(nums[1:])).

    Аргументы:
        nums: список сумм (круговой)

    Возвращает:
        int: максимальная добыча

    Сложность: O(n)

    Пример:
        >>> house_robber_circle([2, 3, 2])
        3
    """
    if len(nums) == 1:
        return nums[0]
    return max(house_robber(nums[:-1]), house_robber(nums[1:]))


def decode_ways(s: str) -> int:
    """
    Количество способов декодировать строку цифр в буквы.

    'A'-'Z' кодируются как '1'-'26'.

    Аргументы:
        s: строка из цифр

    Возвращает:
        int: количество декодирований

    Сложность: O(n) по времени, O(1) по памяти

    Пример:
        >>> decode_ways("226")
        3  # "BBF", "BZ", "VF"
    """
    if not s or s[0] == '0':
        return 0

    prev2, prev1 = 1, 1

    for i in range(1, len(s)):
        cur = 0
        # Один символ
        if s[i] != '0':
            cur += prev1
        # Два символа
        two = int(s[i-1:i+1])
        if 10 <= two <= 26:
            cur += prev2
        prev2, prev1 = prev1, cur

    return prev1


def min_cost_climbing(cost: List[int]) -> int:
    """
    Минимальная стоимость подъёма по лестнице.

    Можно начать с индекса 0 или 1.
    С позиции i можно прыгнуть на 1 или 2 ступени.

    Аргументы:
        cost: стоимость каждой ступени

    Возвращает:
        int: минимальная стоимость достижения вершины

    Сложность: O(n) по времени, O(1) по памяти

    Пример:
        >>> min_cost_climbing([10, 15, 20])
        15
    """
    prev2, prev1 = 0, 0
    for c in cost:
        prev2, prev1 = prev1, min(prev1, prev2) + c
    return min(prev1, prev2)


# =============================================================================
# 2D ДИНАМИЧЕСКОЕ ПРОГРАММИРОВАНИЕ
# =============================================================================

def edit_distance(word1: str, word2: str) -> int:
    """
    Редакционное расстояние Левенштейна.

    Минимальное количество операций (вставка, удаление, замена)
    для превращения word1 в word2.

    Аргументы:
        word1, word2: строки

    Возвращает:
        int: редакционное расстояние

    Сложность: O(m × n) по времени, O(min(m, n)) по памяти (оптимизированный)

    Рекуррентность:
        dp[i][j] = dp[i-1][j-1]             если word1[i-1] == word2[j-1]
        dp[i][j] = 1 + min(dp[i-1][j],      # удаление
                           dp[i][j-1],       # вставка
                           dp[i-1][j-1])     # замена

    Пример:
        >>> edit_distance("horse", "ros")
        3
    """
    m, n = len(word1), len(word2)
    # Оптимизация: используем одну строку вместо матрицы
    dp = list(range(n + 1))

    for i in range(1, m + 1):
        prev = dp[0]
        dp[0] = i
        for j in range(1, n + 1):
            temp = dp[j]
            if word1[i - 1] == word2[j - 1]:
                dp[j] = prev
            else:
                dp[j] = 1 + min(prev, dp[j], dp[j - 1])
            prev = temp

    return dp[n]


def longest_common_subsequence(text1: str, text2: str) -> str:
    """
    Наибольшая общая подпоследовательность (LCS) с восстановлением.

    Аргументы:
        text1, text2: строки

    Возвращает:
        str: сама наибольшая общая подпоследовательность

    Сложность: O(m × n) по времени и памяти

    Пример:
        >>> longest_common_subsequence("abcde", "ace")
        'ace'
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
            i -= 1; j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            i -= 1
        else:
            j -= 1

    return ''.join(reversed(lcs))


def max_square(matrix: List[List[str]]) -> int:
    """
    Наибольший квадрат из единиц в бинарной матрице.

    Аргументы:
        matrix: бинарная матрица ('0' и '1')

    Возвращает:
        int: площадь наибольшего квадрата

    Сложность: O(m × n) по времени и памяти

    Рекуррентность:
        dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
                   если matrix[i][j] == '1', иначе 0.

    Пример:
        >>> max_square([["1","0","1","0"],["1","0","1","1"],["1","1","1","1"]])
        4
    """
    if not matrix:
        return 0
    rows, cols = len(matrix), len(matrix[0])
    dp = [[0] * cols for _ in range(rows)]
    max_side = 0

    for i in range(rows):
        for j in range(cols):
            if matrix[i][j] == '1':
                if i == 0 or j == 0:
                    dp[i][j] = 1
                else:
                    dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
                max_side = max(max_side, dp[i][j])

    return max_side * max_side


# =============================================================================
# ЗАДАЧИ О РЮКЗАКЕ
# =============================================================================

def knapsack_01(weights: List[int], values: List[int], W: int) -> int:
    """
    Задача о рюкзаке 0/1.

    Каждый предмет берётся 0 или 1 раз.

    Аргументы:
        weights: список весов
        values: список ценностей
        W: вместимость рюкзака

    Возвращает:
        int: максимальная ценность

    Сложность: O(n × W) по времени, O(W) по памяти (оптимизировано)

    Важно: проходим вместимость справа налево, чтобы каждый предмет
    использовался не более одного раза.

    Пример:
        >>> knapsack_01([1, 3, 4, 5], [1, 4, 5, 7], 7)
        9
    """
    dp = [0] * (W + 1)
    for w, v in zip(weights, values):
        for cap in range(W, w - 1, -1):     # справа налево!
            dp[cap] = max(dp[cap], dp[cap - w] + v)
    return dp[W]


def knapsack_unbounded(weights: List[int], values: List[int], W: int) -> int:
    """
    Задача о рюкзаке с неограниченным количеством предметов.

    Каждый предмет можно брать любое число раз.

    Аргументы:
        weights, values, W: аналогично knapsack_01

    Возвращает:
        int: максимальная ценность

    Сложность: O(n × W)

    Отличие от 0/1: проходим вместимость слева направо.

    Пример:
        >>> knapsack_unbounded([1, 3, 4], [1, 4, 5], 7)
        11  # 3+4 → берём предмет весом 3 дважды + предмет весом 1
    """
    dp = [0] * (W + 1)
    for cap in range(1, W + 1):
        for w, v in zip(weights, values):
            if w <= cap:
                dp[cap] = max(dp[cap], dp[cap - w] + v)
    return dp[W]


def coin_change(coins: List[int], amount: int) -> int:
    """
    Минимальное количество монет для заданной суммы.

    Частный случай unbounded knapsack: все ценности = 1, минимизируем.

    Аргументы:
        coins: доступные номиналы
        amount: целевая сумма

    Возвращает:
        int: минимальное количество монет или -1 если невозможно

    Сложность: O(amount × n)

    Пример:
        >>> coin_change([1, 2, 5], 11)
        3  # 5 + 5 + 1
    """
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a:
                dp[a] = min(dp[a], dp[a - c] + 1)
    return dp[amount] if dp[amount] != float('inf') else -1


def partition_equal_subset(nums: List[int]) -> bool:
    """
    Разбить массив на два подмножества с равными суммами.

    Эквивалентно: Subset Sum с target = sum(nums) // 2.

    Аргументы:
        nums: список чисел

    Возвращает:
        bool: True если разбиение возможно

    Сложность: O(n × sum)

    Пример:
        >>> partition_equal_subset([1, 5, 11, 5])
        True  # [1, 5, 5] и [11]
    """
    total = sum(nums)
    if total % 2 != 0:
        return False
    target = total // 2
    dp = [False] * (target + 1)
    dp[0] = True
    for num in nums:
        for s in range(target, num - 1, -1):
            dp[s] = dp[s] or dp[s - num]
    return dp[target]


# =============================================================================
# DP НА ИНТЕРВАЛАХ
# =============================================================================

def matrix_chain_order(dims: List[int]) -> int:
    """
    Минимальная стоимость перемножения цепочки матриц.

    dims[i-1] × dims[i] — размер i-й матрицы.
    Стоимость перемножения A[p×q] × B[q×r] = p × q × r.

    Аргументы:
        dims: список размерностей (n+1 элемент для n матриц)

    Возвращает:
        int: минимальное количество операций умножения

    Сложность: O(n³) по времени, O(n²) по памяти

    Пример:
        >>> matrix_chain_order([10, 30, 5, 60])
        4500  # (A1 × A2) × A3 vs A1 × (A2 × A3) и т.д.
    """
    n = len(dims) - 1       # количество матриц
    dp = [[0] * n for _ in range(n)]

    for length in range(2, n + 1):          # длина цепочки
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = float('inf')
            for k in range(i, j):
                cost = dp[i][k] + dp[k+1][j] + dims[i] * dims[k+1] * dims[j+1]
                dp[i][j] = min(dp[i][j], cost)

    return dp[0][n - 1]


def burst_balloons(nums: List[int]) -> int:
    """
    Задача о лопании шаров: максимальное количество монет.

    Лопнуть шар i даёт nums[i-1] * nums[i] * nums[i+1] монет.
    Лопаем все шары в оптимальном порядке.

    Аргументы:
        nums: список значений шаров

    Возвращает:
        int: максимальное количество монет

    Сложность: O(n³) по времени, O(n²) по памяти

    Приём: вместо «какой лопнуть первым» думаем «какой лопнуть последним»
    в интервале [i, j].

    Пример:
        >>> burst_balloons([3, 1, 5, 8])
        167
    """
    nums = [1] + nums + [1]     # добавляем граничные 1
    n = len(nums)
    dp = [[0] * n for _ in range(n)]

    for length in range(2, n):
        for left in range(0, n - length):
            right = left + length
            for k in range(left + 1, right):
                dp[left][right] = max(
                    dp[left][right],
                    nums[left] * nums[k] * nums[right] + dp[left][k] + dp[k][right]
                )

    return dp[0][n - 1]


# =============================================================================
# BITMASK DP
# =============================================================================

def traveling_salesman(dist: List[List[int]]) -> int:
    """
    Задача коммивояжёра (TSP) через Bitmask DP.

    Найти кратчайший Гамильтонов цикл в полном взвешенном графе.

    Аргументы:
        dist: матрица расстояний n × n

    Возвращает:
        int: длина кратчайшего цикла

    Сложность: O(n² × 2^n) по времени, O(n × 2^n) по памяти
    Применимо при n ≤ 20.

    Пример:
        >>> dist = [[0,10,15,20],[10,0,35,25],[15,35,0,30],[20,25,30,0]]
        >>> traveling_salesman(dist)
        80
    """
    n = len(dist)
    full = (1 << n) - 1

    # dp[mask][v] — минимальная стоимость пути, посетившего вершины из mask,
    # заканчивающегося в v
    dp = [[float('inf')] * n for _ in range(1 << n)]
    dp[1][0] = 0                # начинаем в вершине 0

    for mask in range(1 << n):
        for u in range(n):
            if dp[mask][u] == float('inf'):
                continue
            if not (mask >> u) & 1:
                continue
            for v in range(n):
                if (mask >> v) & 1:
                    continue
                new_mask = mask | (1 << v)
                new_cost = dp[mask][u] + dist[u][v]
                dp[new_mask][v] = min(dp[new_mask][v], new_cost)

    return min(dp[full][v] + dist[v][0] for v in range(1, n))


def count_hamiltonian_paths(graph: List[List[int]]) -> int:
    """
    Подсчёт гамильтоновых путей в ориентированном графе.

    Аргументы:
        graph: матрица смежности (0/1)

    Возвращает:
        int: количество гамильтоновых путей

    Сложность: O(n² × 2^n)
    """
    n = len(graph)
    dp = [[0] * n for _ in range(1 << n)]

    for v in range(n):
        dp[1 << v][v] = 1

    for mask in range(1 << n):
        for u in range(n):
            if dp[mask][u] == 0 or not (mask >> u) & 1:
                continue
            for v in range(n):
                if (mask >> v) & 1 or not graph[u][v]:
                    continue
                dp[mask | (1 << v)][v] += dp[mask][u]

    full = (1 << n) - 1
    return sum(dp[full])


# =============================================================================
# BACKTRACKING С МЕМОИЗАЦИЕЙ
# =============================================================================

def word_break(s: str, word_dict: List[str]) -> bool:
    """
    Проверка, можно ли разбить строку на слова из словаря.

    Аргументы:
        s: строка
        word_dict: список допустимых слов

    Возвращает:
        bool: True если разбиение возможно

    Сложность: O(n² × m), m — средняя длина слова в словаре

    Пример:
        >>> word_break("leetcode", ["leet", "code"])
        True
    """
    word_set = set(word_dict)
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True

    for i in range(1, n + 1):
        for j in range(i):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break

    return dp[n]


def word_break_all(s: str, word_dict: List[str]) -> List[str]:
    """
    Все способы разбить строку на слова из словаря.

    Аргументы:
        s: строка
        word_dict: список допустимых слов

    Возвращает:
        list: список всех разбиений

    Сложность: O(n × 2^n) в худшем случае

    Пример:
        >>> word_break_all("catsanddog", ["cat","cats","and","sand","dog"])
        ['cats and dog', 'cat sand dog']
    """
    word_set = set(word_dict)
    memo: Dict[int, List[str]] = {}

    def dp(start: int) -> List[str]:
        if start in memo:
            return memo[start]
        if start == len(s):
            return [""]
        result = []
        for end in range(start + 1, len(s) + 1):
            word = s[start:end]
            if word in word_set:
                for rest in dp(end):
                    result.append(word if not rest else f"{word} {rest}")
        memo[start] = result
        return result

    return dp(0)


@lru_cache(maxsize=None)
def count_palindrome_substrings(s: str) -> int:
    """
    Количество палиндромных подстрок через мемоизацию.

    Аргументы:
        s: строка

    Возвращает:
        int: количество палиндромных подстрок

    Сложность: O(n²)

    Пример:
        >>> count_palindrome_substrings("aaa")
        6
    """
    count = 0

    def expand(l: int, r: int):
        nonlocal count
        while l >= 0 and r < len(s) and s[l] == s[r]:
            count += 1
            l -= 1; r += 1

    for i in range(len(s)):
        expand(i, i)        # нечётные палиндромы
        expand(i, i + 1)    # чётные палиндромы

    return count


# =============================================================================
# ДЕМОНСТРАЦИЯ
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("ДИНАМИЧЕСКОЕ ПРОГРАММИРОВАНИЕ — РАСШИРЕННЫЙ РАЗБОР")
    print("=" * 60)

    # --- 1D DP ---
    print("\n[1] 1D DP — классические задачи")
    print(f"  Лестница (n=10): {climb_stairs(10)} способов")
    print(f"  Грабитель [2,7,9,3,1]: {house_robber([2, 7, 9, 3, 1])}")
    print(f"  Грабитель круговой [2,3,2]: {house_robber_circle([2, 3, 2])}")
    print(f"  Декодирование '226': {decode_ways('226')} способа")
    print(f"  Минимальная стоимость [10,15,20]: {min_cost_climbing([10, 15, 20])}")

    # --- 2D DP ---
    print("\n[2] 2D DP — строки и матрицы")
    print(f"  Edit Distance 'horse'→'ros': {edit_distance('horse', 'ros')}")
    print(f"  LCS 'abcde' и 'ace': '{longest_common_subsequence('abcde', 'ace')}'")
    matrix = [["1","0","1","0","0"],
              ["1","0","1","1","1"],
              ["1","1","1","1","1"],
              ["1","0","0","1","0"]]
    print(f"  Наибольший квадрат из единиц: {max_square(matrix)}")

    # --- Рюкзак ---
    print("\n[3] Задачи о рюкзаке")
    w = [1, 3, 4, 5]
    v = [1, 4, 5, 7]
    W = 7
    print(f"  0/1 Knapsack (W={W}): {knapsack_01(w, v, W)}")
    print(f"  Unbounded Knapsack: {knapsack_unbounded([1,3,4], [1,4,5], 7)}")
    print(f"  Coin Change [1,2,5]→11: {coin_change([1, 2, 5], 11)} монеты")
    print(f"  Partition Equal Subset [1,5,11,5]: {partition_equal_subset([1, 5, 11, 5])}")

    # --- DP на интервалах ---
    print("\n[4] DP на интервалах")
    dims = [10, 30, 5, 60]
    print(f"  Matrix Chain {dims}: {matrix_chain_order(dims)} операций")
    print(f"  Burst Balloons [3,1,5,8]: {burst_balloons([3, 1, 5, 8])} монет")

    # --- Bitmask DP ---
    print("\n[5] Bitmask DP")
    dist_tsp = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ]
    print(f"  TSP (4 города): {traveling_salesman(dist_tsp)}")

    # --- Backtracking + мемо ---
    print("\n[6] Backtracking с мемоизацией")
    print(f"  Word Break 'leetcode': {word_break('leetcode', ['leet','code'])}")
    parts = word_break_all("catsanddog", ["cat", "cats", "and", "sand", "dog"])
    print(f"  Все разбиения 'catsanddog': {parts}")
    print(f"  Палиндромных подстрок в 'aaa': {count_palindrome_substrings('aaa')}")
    print(f"  Палиндромных подстрок в 'abcba': {count_palindrome_substrings('abcba')}")
