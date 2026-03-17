"""
ПРОДВИНУТЫЕ СТРУКТУРЫ ДАННЫХ (ADVANCED DATA STRUCTURES)

Глава 7 учебного пособия.

Темы:
- Монотонный стек (Monotonic Stack)
- Дек и скользящий максимум
- LRU Cache (хеш-таблица + двусвязный список)
- Trie (префиксное дерево)
- Система непересекающихся множеств (DSU / Union-Find)

Каждая структура сопровождается:
1. Реализацией с нуля
2. Решением классической задачи
3. Анализом сложности
"""

from collections import deque, OrderedDict
from typing import List, Optional


# =============================================================================
# МОНОТОННЫЙ СТЕК (MONOTONIC STACK)
# =============================================================================

def next_greater_element(nums: List[int]) -> List[int]:
    """
    Следующий больший элемент для каждого элемента массива.

    Для каждого nums[i] находим первый элемент справа, который больше nums[i].
    Если такого нет — возвращаем -1.

    Аргументы:
        nums: список чисел

    Возвращает:
        list: next_greater[i] — следующий больший элемент для nums[i]

    Сложность: O(n) по времени, O(n) по памяти

    Ключевая идея:
        Поддерживаем стек индексов с убывающими значениями.
        Когда встречаем элемент больше вершины стека — нашли ответ для неё.

    Пример:
        >>> next_greater_element([4, 5, 2, 25])
        [5, 25, 25, -1]
    """
    n = len(nums)
    result = [-1] * n
    stack = []  # индексы элементов, для которых ответ ещё не найден

    for i in range(n):
        # Пока стек не пуст и текущий элемент больше вершины стека
        while stack and nums[stack[-1]] < nums[i]:
            result[stack.pop()] = nums[i]
        stack.append(i)

    return result


def next_greater_circular(nums: List[int]) -> List[int]:
    """
    Следующий больший элемент в циклическом массиве.

    Массив считается циклическим: за последним элементом идёт первый.

    Аргументы:
        nums: список чисел

    Возвращает:
        list: следующие большие элементы с учётом цикличности

    Сложность: O(n)

    Приём: проходим массив дважды (индексы по модулю n).

    Пример:
        >>> next_greater_circular([1, 2, 1])
        [2, -1, 2]
    """
    n = len(nums)
    result = [-1] * n
    stack = []

    for i in range(2 * n):          # два прохода
        idx = i % n
        while stack and nums[stack[-1]] < nums[idx]:
            result[stack.pop()] = nums[idx]
        if i < n:
            stack.append(idx)

    return result


def daily_temperatures(temperatures: List[int]) -> List[int]:
    """
    Количество дней ожидания до более тёплой погоды.

    Для каждого дня определяем, через сколько дней температура
    станет выше текущей.

    Аргументы:
        temperatures: список дневных температур

    Возвращает:
        list: wait[i] — дней до потепления (0 если никогда)

    Сложность: O(n)

    Пример:
        >>> daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73])
        [1, 1, 4, 2, 1, 1, 0, 0]
    """
    n = len(temperatures)
    result = [0] * n
    stack = []  # индексы дней с «ожидающими» температурами

    for i in range(n):
        while stack and temperatures[stack[-1]] < temperatures[i]:
            j = stack.pop()
            result[j] = i - j
        stack.append(i)

    return result


def largest_rectangle_histogram(heights: List[int]) -> int:
    """
    Наибольший прямоугольник в гистограмме.

    Дан массив высот столбцов единичной ширины.
    Найти площадь наибольшего прямоугольника.

    Аргументы:
        heights: список высот столбцов

    Возвращает:
        int: максимальная площадь прямоугольника

    Сложность: O(n) по времени, O(n) по памяти

    Алгоритм:
        Монотонный возрастающий стек.
        Когда текущая высота меньше вершины — вычисляем площадь с
        вершиной как минимальной высотой.
        Добавляем «0» в конец для принудительной очистки стека.

    Пример:
        >>> largest_rectangle_histogram([2, 1, 5, 6, 2, 3])
        10
    """
    max_area = 0
    stack = []  # индексы в порядке возрастания высот

    for i, h in enumerate(heights + [0]):
        while stack and heights[stack[-1]] > h:
            height = heights[stack.pop()]
            width = i if not stack else i - stack[-1] - 1
            max_area = max(max_area, height * width)
        stack.append(i)

    return max_area


def trap_rain_water(height: List[int]) -> int:
    """
    Задача о накоплении дождевой воды.

    Дан рельеф в виде массива высот.
    Определить, сколько единиц воды задержится после дождя.

    Аргументы:
        height: список высот

    Возвращает:
        int: количество единиц воды

    Сложность: O(n) по времени, O(1) по памяти (метод двух указателей)

    Пример:
        >>> trap_rain_water([0,1,0,2,1,0,1,3,2,1,2,1])
        6
    """
    left, right = 0, len(height) - 1
    left_max = right_max = 0
    water = 0

    while left < right:
        if height[left] <= height[right]:
            if height[left] >= left_max:
                left_max = height[left]
            else:
                water += left_max - height[left]
            left += 1
        else:
            if height[right] >= right_max:
                right_max = height[right]
            else:
                water += right_max - height[right]
            right -= 1

    return water


# =============================================================================
# СКОЛЬЗЯЩИЙ МАКСИМУМ (SLIDING WINDOW MAXIMUM)
# =============================================================================

def max_sliding_window(nums: List[int], k: int) -> List[int]:
    """
    Максимум в каждом окне размера k.

    Аргументы:
        nums: список чисел
        k: размер скользящего окна

    Возвращает:
        list: максимум для каждого положения окна

    Сложность: O(n) по времени, O(k) по памяти

    Алгоритм:
        Монотонный убывающий дек хранит ИНДЕКСЫ элементов.
        Инвариант: nums[dq[0]] — максимум текущего окна.
        При добавлении нового элемента выталкиваем из хвоста все
        меньшие — они никогда не станут максимумом.

    Пример:
        >>> max_sliding_window([1,3,-1,-3,5,3,6,7], 3)
        [3, 3, 5, 5, 6, 7]
    """
    if not nums or k == 0:
        return []

    dq = deque()   # хранит индексы; dq[0] — индекс максимума окна
    result = []

    for i, val in enumerate(nums):
        # Удаляем индексы за пределами окна
        if dq and dq[0] < i - k + 1:
            dq.popleft()
        # Удаляем индексы с меньшими значениями — они бесполезны
        while dq and nums[dq[-1]] < val:
            dq.pop()
        dq.append(i)

        if i >= k - 1:
            result.append(nums[dq[0]])

    return result


# =============================================================================
# LRU CACHE
# =============================================================================

class LRUCache:
    """
    Кэш с вытеснением давно неиспользуемых (Least Recently Used).

    Поддерживает операции get и put за O(1).

    Реализация:
        Комбинация хеш-таблицы (O(1) доступ по ключу) и
        двусвязного списка (O(1) перемещение и удаление узлов).
        Голова списка — самый недавно использованный элемент.
        Хвост — наиболее «старый», кандидат на вытеснение.

    Атрибуты:
        capacity: максимальная ёмкость кэша

    Пример:
        >>> cache = LRUCache(2)
        >>> cache.put(1, 1)
        >>> cache.put(2, 2)
        >>> cache.get(1)    # возвращает 1
        1
        >>> cache.put(3, 3) # вытесняет ключ 2
        >>> cache.get(2)    # возвращает -1 (не найден)
        -1
    """

    class _Node:
        """Узел двусвязного списка для LRU Cache."""
        __slots__ = ('key', 'val', 'prev', 'next')

        def __init__(self, key: int = 0, val: int = 0):
            self.key = key
            self.val = val
            self.prev = None
            self.next = None

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}                    # key -> Node

        # Фиктивные узлы-стражи (sentinel): head <-> ... <-> tail
        # Между ними — реальные узлы от самого нового к самому старому
        self._head = self._Node()
        self._tail = self._Node()
        self._head.next = self._tail
        self._tail.prev = self._head

    def _remove(self, node: '_Node') -> None:
        """Удалить узел из двусвязного списка. O(1)."""
        node.prev.next = node.next
        node.next.prev = node.prev

    def _insert_front(self, node: '_Node') -> None:
        """Вставить узел сразу за head (в начало). O(1)."""
        node.next = self._head.next
        node.prev = self._head
        self._head.next.prev = node
        self._head.next = node

    def get(self, key: int) -> int:
        """
        Получить значение по ключу.

        При обращении элемент перемещается в начало (самый свежий).

        Возвращает:
            int: значение или -1 если ключ не найден

        Сложность: O(1)
        """
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._remove(node)
        self._insert_front(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        """
        Вставить или обновить пару ключ-значение.

        При превышении ёмкости вытесняет наименее используемый элемент.

        Сложность: O(1)
        """
        if key in self.cache:
            self._remove(self.cache[key])
        node = self._Node(key, value)
        self._insert_front(node)
        self.cache[key] = node

        if len(self.cache) > self.capacity:
            # Вытесняем LRU — узел перед tail
            lru = self._tail.prev
            self._remove(lru)
            del self.cache[lru.key]


# =============================================================================
# TRIE (ПРЕФИКСНОЕ ДЕРЕВО)
# =============================================================================

class TrieNode:
    """Узел префиксного дерева."""
    __slots__ = ('children', 'is_end')

    def __init__(self):
        self.children: dict = {}
        self.is_end: bool = False    # True, если узел завершает слово


class Trie:
    """
    Префиксное дерево (Trie).

    Структура данных для эффективного хранения и поиска строк.

    Основные операции:
        insert   — O(m), m — длина слова
        search   — O(m)
        startsWith — O(m)

    Преимущество перед хеш-таблицей:
        Поиск по префиксу за O(m) без перебора всех ключей.

    Применение:
        Автодополнение, проверка орфографии, IP-маршрутизация.

    Пример:
        >>> trie = Trie()
        >>> trie.insert("apple")
        >>> trie.search("apple")
        True
        >>> trie.search("app")
        False
        >>> trie.starts_with("app")
        True
    """

    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """
        Вставка слова в Trie.

        Сложность: O(m)
        """
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True

    def search(self, word: str) -> bool:
        """
        Проверка наличия слова в Trie.

        Сложность: O(m)
        """
        node = self._find_node(word)
        return node is not None and node.is_end

    def starts_with(self, prefix: str) -> bool:
        """
        Проверка наличия слова с данным префиксом.

        Сложность: O(m)
        """
        return self._find_node(prefix) is not None

    def _find_node(self, prefix: str) -> Optional[TrieNode]:
        """Найти узел, соответствующий последнему символу prefix."""
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node

    def count_words_with_prefix(self, prefix: str) -> int:
        """
        Подсчёт количества слов с данным префиксом.

        Сложность: O(m + W), W — количество слов с данным префиксом.
        """
        node = self._find_node(prefix)
        if node is None:
            return 0

        count = 0
        stack = [node]
        while stack:
            cur = stack.pop()
            if cur.is_end:
                count += 1
            stack.extend(cur.children.values())
        return count


# =============================================================================
# СИСТЕМА НЕПЕРЕСЕКАЮЩИХСЯ МНОЖЕСТВ (DSU / UNION-FIND)
# =============================================================================

class DSU:
    """
    Система непересекающихся множеств (Disjoint Set Union).

    Также известна как Union-Find.

    Эффективно решает задачи:
        - Принадлежность двух элементов одному множеству
        - Объединение двух множеств
        - Подсчёт числа связных компонент

    Оптимизации:
        1. Сжатие пути (path compression): find рекурсивно сжимает путь к корню.
        2. Объединение по рангу (union by rank): меньшее дерево присоединяется
           к большему, предотвращая вырождение.

    Сложность:
        Амортизированное O(α(n)) ≈ O(1) на операцию,
        где α — обратная функция Аккермана (растёт крайне медленно).

    Пример:
        >>> dsu = DSU(5)
        >>> dsu.union(0, 1)
        True
        >>> dsu.union(1, 2)
        True
        >>> dsu.connected(0, 2)
        True
        >>> dsu.components()
        3
    """

    def __init__(self, n: int):
        """
        Инициализация n непересекающихся множеств {0}, {1}, ..., {n-1}.

        Аргументы:
            n: количество элементов
        """
        self.parent = list(range(n))
        self.rank = [0] * n
        self._count = n              # количество компонент

    def find(self, x: int) -> int:
        """
        Найти корень (представитель) множества для элемента x.

        Применяет сжатие пути: все узлы на пути к корню
        напрямую присоединяются к корню.

        Сложность: O(α(n)) амортизированно
        """
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])   # сжатие пути
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        """
        Объединить множества, содержащие x и y.

        Возвращает:
            bool: True если множества были разными (произошло объединение)

        Сложность: O(α(n)) амортизированно
        """
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False                  # уже в одном множестве

        # Объединение по рангу: меньший ранг под больший
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1

        self._count -= 1
        return True

    def connected(self, x: int, y: int) -> bool:
        """Проверить, принадлежат ли x и y одному множеству."""
        return self.find(x) == self.find(y)

    def components(self) -> int:
        """Вернуть текущее количество компонент."""
        return self._count


def count_islands(grid: List[List[str]]) -> int:
    """
    Подсчёт числа островов на карте.

    Остров — связная группа клеток '1' (суша), окружённая '0' (водой).
    Связность — по 4 направлениям (вверх, вниз, влево, вправо).

    Аргументы:
        grid: матрица символов '0' и '1'

    Возвращает:
        int: количество островов

    Сложность: O(m × n) по времени и памяти

    Решение через DSU:
        Каждую '1' объединяем с соседними '1'. Количество компонент
        в конце равно числу островов.

    Пример:
        >>> grid = [
        ...     ["1","1","0","0","0"],
        ...     ["1","1","0","0","0"],
        ...     ["0","0","1","0","0"],
        ...     ["0","0","0","1","1"]
        ... ]
        >>> count_islands(grid)
        3
    """
    if not grid or not grid[0]:
        return 0

    rows, cols = len(grid), len(grid[0])
    dsu = DSU(rows * cols)
    water_cells = 0

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '0':
                water_cells += 1
                continue
            # Объединяем с правым и нижним соседом (если суша)
            if r + 1 < rows and grid[r + 1][c] == '1':
                dsu.union(r * cols + c, (r + 1) * cols + c)
            if c + 1 < cols and grid[r][c + 1] == '1':
                dsu.union(r * cols + c, r * cols + c + 1)

    return dsu.components() - water_cells


# =============================================================================
# ДЕМОНСТРАЦИЯ
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("ПРОДВИНУТЫЕ СТРУКТУРЫ ДАННЫХ")
    print("=" * 60)

    # --- Монотонный стек ---
    print("\n[1] Монотонный стек")
    nums = [4, 5, 2, 25]
    print(f"  Массив: {nums}")
    print(f"  Следующий больший: {next_greater_element(nums)}")

    nums2 = [1, 2, 1]
    print(f"\n  Циклический массив: {nums2}")
    print(f"  Следующий больший (цикл): {next_greater_circular(nums2)}")

    temps = [73, 74, 75, 71, 69, 72, 76, 73]
    print(f"\n  Температуры: {temps}")
    print(f"  Дней до потепления: {daily_temperatures(temps)}")

    heights = [2, 1, 5, 6, 2, 3]
    print(f"\n  Гистограмма: {heights}")
    print(f"  Максимальный прямоугольник: {largest_rectangle_histogram(heights)}")

    # --- Скользящий максимум ---
    print("\n[2] Скользящий максимум")
    w = [1, 3, -1, -3, 5, 3, 6, 7]
    k = 3
    print(f"  Массив: {w}, k={k}")
    print(f"  Максимумы: {max_sliding_window(w, k)}")

    # --- Дождевая вода ---
    print("\n[3] Дождевая вода")
    h = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
    print(f"  Рельеф: {h}")
    print(f"  Накопленная вода: {trap_rain_water(h)}")

    # --- LRU Cache ---
    print("\n[4] LRU Cache (ёмкость 2)")
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    print(f"  get(1) = {cache.get(1)}")    # 1
    cache.put(3, 3)                         # вытесняет ключ 2
    print(f"  get(2) = {cache.get(2)}")    # -1
    print(f"  get(3) = {cache.get(3)}")    # 3

    # --- Trie ---
    print("\n[5] Trie (префиксное дерево)")
    trie = Trie()
    words = ["apple", "app", "application", "apply", "apt"]
    for w_item in words:
        trie.insert(w_item)
    print(f"  Вставлены слова: {words}")
    print(f"  search('apple')  = {trie.search('apple')}")
    print(f"  search('appl')   = {trie.search('appl')}")
    print(f"  starts_with('app') = {trie.starts_with('app')}")
    print(f"  Слов с префиксом 'app': {trie.count_words_with_prefix('app')}")

    # --- DSU ---
    print("\n[6] DSU / Union-Find")
    dsu = DSU(6)
    edges = [(0, 1), (1, 2), (3, 4)]
    for u, v in edges:
        dsu.union(u, v)
    print(f"  Рёбра: {edges}, вершин: 6")
    print(f"  connected(0, 2) = {dsu.connected(0, 2)}")
    print(f"  connected(0, 3) = {dsu.connected(0, 3)}")
    print(f"  Компонент: {dsu.components()}")

    # --- Острова ---
    print("\n[7] Подсчёт островов через DSU")
    grid = [
        ["1", "1", "0", "0", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "1", "0", "0"],
        ["0", "0", "0", "1", "1"]
    ]
    print(f"  Островов: {count_islands(grid)}")
