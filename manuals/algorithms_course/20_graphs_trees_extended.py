"""
ГРАФЫ И ДЕРЕВЬЯ — РАСШИРЕННЫЕ АЛГОРИТМЫ (GRAPHS & TREES EXTENDED)

Глава 8 учебного пособия.

Темы:
- BFS / DFS с восстановлением пути
- Топологическая сортировка (Kahn's algorithm + DFS)
- Алгоритм Дейкстры
- Минимальное остовное дерево (Kruskal, Prim)
- Обходы бинарного дерева (итеративные)
- Наименьший общий предок (LCA) за O(log n)
- Сериализация / десериализация дерева
"""

import heapq
from collections import deque, defaultdict
from typing import List, Optional, Dict, Tuple


# =============================================================================
# ВСПОМОГАТЕЛЬНЫЕ КЛАССЫ
# =============================================================================

class TreeNode:
    """Узел бинарного дерева."""
    def __init__(self, val: int = 0, left: 'TreeNode' = None,
                 right: 'TreeNode' = None):
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self):
        return f"TreeNode({self.val})"


# =============================================================================
# BFS / DFS С ВОССТАНОВЛЕНИЕМ ПУТИ
# =============================================================================

def bfs_with_path(graph: Dict, start, end) -> List:
    """
    Кратчайший путь в невзвешенном графе (BFS).

    Аргументы:
        graph: словарь {вершина: [соседи]}
        start: начальная вершина
        end: конечная вершина

    Возвращает:
        list: путь от start до end или [] если пути нет

    Сложность: O(V + E)

    Пример:
        >>> g = {0: [1, 2], 1: [3], 2: [3], 3: []}
        >>> bfs_with_path(g, 0, 3)
        [0, 1, 3]
    """
    if start == end:
        return [start]

    visited = {start: None}     # вершина -> откуда пришли
    queue = deque([start])

    while queue:
        v = queue.popleft()
        for nei in graph.get(v, []):
            if nei not in visited:
                visited[nei] = v
                if nei == end:
                    return _reconstruct(visited, start, end)
                queue.append(nei)

    return []


def _reconstruct(parent: Dict, start, end) -> List:
    """Восстановить путь по словарю предшественников."""
    path = []
    cur = end
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    return path[::-1]


def dfs_all_paths(graph: Dict, start, end) -> List[List]:
    """
    Все пути от start до end в ориентированном ациклическом графе.

    Аргументы:
        graph: словарь {вершина: [соседи]}
        start: начальная вершина
        end: конечная вершина

    Возвращает:
        list: список всех простых путей

    Сложность: O(V! / (V - E)!) в худшем случае (полный граф)

    Пример:
        >>> g = {0: [1, 2], 1: [3], 2: [3], 3: []}
        >>> dfs_all_paths(g, 0, 3)
        [[0, 1, 3], [0, 2, 3]]
    """
    result = []

    def dfs(v, path: List, visited: set):
        if v == end:
            result.append(path[:])
            return
        for nei in graph.get(v, []):
            if nei not in visited:
                visited.add(nei)
                path.append(nei)
                dfs(nei, path, visited)
                path.pop()
                visited.remove(nei)

    dfs(start, [start], {start})
    return result


# =============================================================================
# ТОПОЛОГИЧЕСКАЯ СОРТИРОВКА
# =============================================================================

def topological_sort_kahn(n: int, edges: List[Tuple[int, int]]) -> List[int]:
    """
    Топологическая сортировка алгоритмом Кана (BFS).

    Алгоритм Кана итеративен и прост в реализации:
    1. Вычисляем входящую степень каждой вершины.
    2. Добавляем в очередь все вершины с нулевой входящей степенью.
    3. Извлекаем вершину, уменьшаем входящую степень соседей.
    4. Соседей с нулевой степенью добавляем в очередь.

    Аргументы:
        n: количество вершин (0..n-1)
        edges: список рёбер [(u, v), ...] означает u -> v

    Возвращает:
        list: топологический порядок или [] при наличии цикла

    Сложность: O(V + E)

    Пример:
        >>> topological_sort_kahn(4, [(0,1),(0,2),(1,3),(2,3)])
        [0, 1, 2, 3]  # или [0, 2, 1, 3]
    """
    in_degree = [0] * n
    graph = defaultdict(list)

    for u, v in edges:
        graph[u].append(v)
        in_degree[v] += 1

    queue = deque(v for v in range(n) if in_degree[v] == 0)
    result = []

    while queue:
        v = queue.popleft()
        result.append(v)
        for nei in graph[v]:
            in_degree[nei] -= 1
            if in_degree[nei] == 0:
                queue.append(nei)

    return result if len(result) == n else []   # [] если есть цикл


def topological_sort_dfs(n: int, edges: List[Tuple[int, int]]) -> Optional[List[int]]:
    """
    Топологическая сортировка через DFS.

    Использует раскраску вершин для обнаружения циклов:
    WHITE (0) -> GRAY (1, в стеке рекурсии) -> BLACK (2, обработан).
    Если встречаем GRAY — цикл.

    Аргументы:
        n: количество вершин
        edges: список рёбер

    Возвращает:
        list: топологический порядок или None при наличии цикла

    Сложность: O(V + E)
    """
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)

    WHITE, GRAY, BLACK = 0, 1, 2
    color = [WHITE] * n
    result = []

    def dfs(v: int) -> bool:
        color[v] = GRAY
        for nei in graph[v]:
            if color[nei] == GRAY:
                return False        # цикл
            if color[nei] == WHITE and not dfs(nei):
                return False
        color[v] = BLACK
        result.append(v)
        return True

    for v in range(n):
        if color[v] == WHITE:
            if not dfs(v):
                return None

    return result[::-1]


# =============================================================================
# АЛГОРИТМ ДЕЙКСТРЫ
# =============================================================================

def dijkstra(graph: Dict[int, List[Tuple[int, int]]], start: int) -> Dict[int, int]:
    """
    Кратчайшие пути от вершины start (алгоритм Дейкстры).

    Аргументы:
        graph: {вершина: [(сосед, вес), ...]}
        start: начальная вершина

    Возвращает:
        dict: {вершина: кратчайшее расстояние от start}

    Сложность: O((V + E) log V) с двоичной кучей

    Ограничение: все веса должны быть неотрицательными.

    Пример:
        >>> g = {0: [(1,4),(2,1)], 1: [(3,1)], 2: [(1,2),(3,5)], 3: []}
        >>> dijkstra(g, 0)
        {0: 0, 1: 3, 2: 1, 3: 4}
    """
    dist = defaultdict(lambda: float('inf'))
    dist[start] = 0
    heap = [(0, start)]   # (расстояние, вершина)
    visited = set()

    while heap:
        d, v = heapq.heappop(heap)
        if v in visited:
            continue
        visited.add(v)
        for nei, w in graph.get(v, []):
            nd = d + w
            if nd < dist[nei]:
                dist[nei] = nd
                heapq.heappush(heap, (nd, nei))

    return dict(dist)


def dijkstra_path(graph: Dict, start: int, end: int) -> Tuple[int, List[int]]:
    """
    Кратчайший путь между двумя вершинами с восстановлением маршрута.

    Возвращает:
        tuple: (расстояние, путь) или (inf, [])

    Сложность: O((V + E) log V)
    """
    dist = defaultdict(lambda: float('inf'))
    dist[start] = 0
    prev = {start: None}
    heap = [(0, start)]
    visited = set()

    while heap:
        d, v = heapq.heappop(heap)
        if v == end:
            return d, _reconstruct(prev, start, end)
        if v in visited:
            continue
        visited.add(v)
        for nei, w in graph.get(v, []):
            nd = d + w
            if nd < dist[nei]:
                dist[nei] = nd
                prev[nei] = v
                heapq.heappush(heap, (nd, nei))

    return float('inf'), []


# =============================================================================
# МИНИМАЛЬНОЕ ОСТОВНОЕ ДЕРЕВО
# =============================================================================

def kruskal(n: int, edges: List[Tuple[int, int, int]]) -> Tuple[int, List]:
    """
    Алгоритм Крускала — минимальное остовное дерево.

    Жадный алгоритм: сортируем рёбра по весу, добавляем ребро,
    если оно не создаёт цикл (проверяем через DSU).

    Аргументы:
        n: количество вершин
        edges: список рёбер [(u, v, вес), ...]

    Возвращает:
        tuple: (суммарный вес МОД, список рёбер МОД)

    Сложность: O(E log E) — доминирует сортировка

    Пример:
        >>> kruskal(4, [(0,1,1),(0,2,4),(1,2,2),(1,3,5),(2,3,3)])
        (6, [(0,1,1),(1,2,2),(2,3,3)])
    """
    parent = list(range(n))
    rank = [0] * n

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        rx, ry = find(x), find(y)
        if rx == ry:
            return False
        if rank[rx] < rank[ry]:
            rx, ry = ry, rx
        parent[ry] = rx
        if rank[rx] == rank[ry]:
            rank[rx] += 1
        return True

    edges_sorted = sorted(edges, key=lambda e: e[2])
    mst_weight = 0
    mst_edges = []

    for u, v, w in edges_sorted:
        if union(u, v):
            mst_weight += w
            mst_edges.append((u, v, w))
            if len(mst_edges) == n - 1:
                break

    return mst_weight, mst_edges


def prim(n: int, graph: Dict[int, List[Tuple[int, int]]]) -> int:
    """
    Алгоритм Прима — минимальное остовное дерево.

    Стартуем из вершины 0, жадно добавляем минимальное ребро,
    ведущее из посещённого множества в непосещённое.

    Аргументы:
        n: количество вершин
        graph: {вершина: [(сосед, вес), ...]}

    Возвращает:
        int: суммарный вес МОД (-1 если граф несвязный)

    Сложность: O((V + E) log V)
    """
    visited = set()
    heap = [(0, 0)]   # (вес ребра, вершина)
    total = 0

    while heap and len(visited) < n:
        w, v = heapq.heappop(heap)
        if v in visited:
            continue
        visited.add(v)
        total += w
        for nei, ew in graph.get(v, []):
            if nei not in visited:
                heapq.heappush(heap, (ew, nei))

    return total if len(visited) == n else -1


# =============================================================================
# ИТЕРАТИВНЫЕ ОБХОДЫ БИНАРНОГО ДЕРЕВА
# =============================================================================

def inorder_iterative(root: Optional[TreeNode]) -> List[int]:
    """
    Итеративный симметричный (inorder) обход.

    Сложность: O(n) по времени, O(h) по памяти (h — высота дерева)

    Пример:
        >>> inorder_iterative(TreeNode(1, TreeNode(2), TreeNode(3)))
        [2, 1, 3]
    """
    result, stack, curr = [], [], root
    while curr or stack:
        while curr:                 # идём влево до упора
            stack.append(curr)
            curr = curr.left
        curr = stack.pop()          # обрабатываем узел
        result.append(curr.val)
        curr = curr.right           # переходим вправо
    return result


def preorder_iterative(root: Optional[TreeNode]) -> List[int]:
    """
    Итеративный прямой (preorder) обход.

    Сложность: O(n) по времени, O(h) по памяти
    """
    if not root:
        return []
    result, stack = [], [root]
    while stack:
        node = stack.pop()
        result.append(node.val)
        if node.right:              # правый первым (LIFO)
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    return result


def postorder_iterative(root: Optional[TreeNode]) -> List[int]:
    """
    Итеративный обратный (postorder) обход.

    Приём: preorder (корень-правый-левый), затем разворот.

    Сложность: O(n) по времени, O(n) по памяти
    """
    if not root:
        return []
    result, stack = [], [root]
    while stack:
        node = stack.pop()
        result.append(node.val)
        if node.left:
            stack.append(node.left)
        if node.right:
            stack.append(node.right)
    return result[::-1]


def level_order(root: Optional[TreeNode]) -> List[List[int]]:
    """
    Обход по уровням (BFS).

    Возвращает:
        list: список списков значений по уровням

    Сложность: O(n) по времени, O(w) по памяти (w — ширина дерева)
    """
    if not root:
        return []
    result, queue = [], deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(level)
    return result


# =============================================================================
# НАИМЕНЬШИЙ ОБЩИЙ ПРЕДОК (LCA)
# =============================================================================

def lca_binary_tree(root: Optional[TreeNode], p: TreeNode,
                     q: TreeNode) -> Optional[TreeNode]:
    """
    Наименьший общий предок в произвольном бинарном дереве.

    Алгоритм: если оба найдены в разных поддеревьях — текущий узел
    и есть LCA; если один — возвращаем его.

    Сложность: O(n) по времени, O(h) по памяти

    Пример:
        Для дерева [3,5,1,6,2,0,8] и p=5, q=1 → LCA = 3
        Для p=5, q=4 → LCA = 5
    """
    if not root or root == p or root == q:
        return root
    left = lca_binary_tree(root.left, p, q)
    right = lca_binary_tree(root.right, p, q)
    if left and right:
        return root
    return left or right


def lca_bst(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    """
    Наименьший общий предок в BST.

    Используем свойство BST: если оба значения меньше корня — LCA слева,
    если оба больше — справа, иначе — корень.

    Сложность: O(h), O(log n) для сбалансированного BST
    """
    while root:
        if p.val < root.val and q.val < root.val:
            root = root.left
        elif p.val > root.val and q.val > root.val:
            root = root.right
        else:
            return root
    return root


class BinaryLiftingLCA:
    """
    LCA за O(log n) с предобработкой O(n log n).

    Метод двоичного подъёма (Binary Lifting).
    Используется для множества запросов LCA на одном дереве.

    Идея: ancestor[v][k] = предок вершины v на 2^k уровней выше.
    Заполняем таблицу через DP: ancestor[v][k] = ancestor[ancestor[v][k-1]][k-1].
    LCA(u, v): выравниваем глубины, затем бинарно поднимаемся.

    Пример:
        >>> # Дерево: 0 - 1 - 2
        >>> #             |
        >>> #             3
        >>> lca = BinaryLiftingLCA(4, [(0,1),(1,2),(1,3)], root=0)
        >>> lca.query(2, 3)
        1
    """

    def __init__(self, n: int, edges: List[Tuple[int, int]], root: int = 0):
        """
        Предобработка дерева.

        Аргументы:
            n: количество вершин
            edges: список рёбер (неориентированных)
            root: корень дерева
        """
        import math
        self.n = n
        self.LOG = max(1, int(math.log2(n)) + 1)
        self.depth = [0] * n
        self.ancestor = [[-1] * n for _ in range(self.LOG)]

        adj = defaultdict(list)
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)

        # BFS для вычисления глубин и прямых предков
        visited = [False] * n
        queue = deque([root])
        visited[root] = True
        self.ancestor[0][root] = root

        while queue:
            v = queue.popleft()
            for nei in adj[v]:
                if not visited[nei]:
                    visited[nei] = True
                    self.depth[nei] = self.depth[v] + 1
                    self.ancestor[0][nei] = v
                    queue.append(nei)

        # Заполнение таблицы DP
        for k in range(1, self.LOG):
            for v in range(n):
                if self.ancestor[k - 1][v] != -1:
                    self.ancestor[k][v] = self.ancestor[k - 1][self.ancestor[k - 1][v]]

    def query(self, u: int, v: int) -> int:
        """
        Найти LCA(u, v).

        Сложность: O(log n)
        """
        # Выравниваем глубины
        if self.depth[u] < self.depth[v]:
            u, v = v, u
        diff = self.depth[u] - self.depth[v]
        for k in range(self.LOG):
            if (diff >> k) & 1:
                u = self.ancestor[k][u]
        if u == v:
            return u
        # Бинарно поднимаемся до LCA
        for k in range(self.LOG - 1, -1, -1):
            if self.ancestor[k][u] != self.ancestor[k][v]:
                u = self.ancestor[k][u]
                v = self.ancestor[k][v]
        return self.ancestor[0][u]


# =============================================================================
# СЕРИАЛИЗАЦИЯ / ДЕСЕРИАЛИЗАЦИЯ ДЕРЕВА
# =============================================================================

def serialize(root: Optional[TreeNode]) -> str:
    """
    Сериализация бинарного дерева в строку (preorder).

    Аргументы:
        root: корень дерева

    Возвращает:
        str: строковое представление вида "1,2,null,null,3,null,null"

    Сложность: O(n)
    """
    parts = []

    def dfs(node):
        if not node:
            parts.append("null")
            return
        parts.append(str(node.val))
        dfs(node.left)
        dfs(node.right)

    dfs(root)
    return ",".join(parts)


def deserialize(data: str) -> Optional[TreeNode]:
    """
    Десериализация строки в бинарное дерево.

    Аргументы:
        data: строка вида "1,2,null,null,3,null,null"

    Возвращает:
        TreeNode: корень восстановленного дерева

    Сложность: O(n)
    """
    vals = iter(data.split(","))

    def build() -> Optional[TreeNode]:
        v = next(vals)
        if v == "null":
            return None
        node = TreeNode(int(v))
        node.left = build()
        node.right = build()
        return node

    return build()


# =============================================================================
# ДЕМОНСТРАЦИЯ
# =============================================================================

def _build_tree(vals: List[Optional[int]]) -> Optional[TreeNode]:
    """Построить дерево из списка значений (BFS-порядок, None = пустой узел)."""
    if not vals:
        return None
    root = TreeNode(vals[0])
    queue = deque([root])
    i = 1
    while queue and i < len(vals):
        node = queue.popleft()
        if i < len(vals) and vals[i] is not None:
            node.left = TreeNode(vals[i])
            queue.append(node.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            node.right = TreeNode(vals[i])
            queue.append(node.right)
        i += 1
    return root


if __name__ == "__main__":
    print("=" * 60)
    print("ГРАФЫ И ДЕРЕВЬЯ — РАСШИРЕННЫЕ АЛГОРИТМЫ")
    print("=" * 60)

    # --- BFS с путём ---
    print("\n[1] BFS — кратчайший путь")
    g = {0: [1, 2], 1: [3], 2: [3], 3: []}
    print(f"  Граф: {dict(g)}")
    print(f"  Путь 0→3: {bfs_with_path(g, 0, 3)}")
    print(f"  Все пути 0→3: {dfs_all_paths(g, 0, 3)}")

    # --- Топологическая сортировка ---
    print("\n[2] Топологическая сортировка")
    n, edges = 6, [(5, 2), (5, 0), (4, 0), (4, 1), (2, 3), (3, 1)]
    print(f"  Рёбра: {edges}")
    print(f"  Kahn:  {topological_sort_kahn(n, edges)}")
    print(f"  DFS:   {topological_sort_dfs(n, edges)}")

    # --- Дейкстра ---
    print("\n[3] Алгоритм Дейкстры")
    wg = {0: [(1, 4), (2, 1)], 1: [(3, 1)], 2: [(1, 2), (3, 5)], 3: []}
    dists = dijkstra(wg, 0)
    print(f"  Расстояния от 0: {dists}")
    d, path = dijkstra_path(wg, 0, 3)
    print(f"  Путь 0→3: {path}, длина: {d}")

    # --- МОД ---
    print("\n[4] Минимальное остовное дерево")
    mst_edges_list = [(0, 1, 1), (0, 2, 4), (1, 2, 2), (1, 3, 5), (2, 3, 3)]
    w, mst = kruskal(4, mst_edges_list)
    print(f"  Kruskal: вес={w}, рёбра={mst}")

    prim_g = {
        0: [(1, 1), (2, 4)],
        1: [(0, 1), (2, 2), (3, 5)],
        2: [(0, 4), (1, 2), (3, 3)],
        3: [(1, 5), (2, 3)]
    }
    print(f"  Prim: вес МОД = {prim(4, prim_g)}")

    # --- Обходы дерева ---
    print("\n[5] Итеративные обходы дерева")
    #        1
    #       / \
    #      2   3
    #     / \
    #    4   5
    root = _build_tree([1, 2, 3, 4, 5])
    print(f"  Inorder:   {inorder_iterative(root)}")
    print(f"  Preorder:  {preorder_iterative(root)}")
    print(f"  Postorder: {postorder_iterative(root)}")
    print(f"  Level:     {level_order(root)}")

    # --- LCA ---
    print("\n[6] Наименьший общий предок")
    root2 = _build_tree([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4])
    p_node = root2.left                   # узел 5
    q_node = root2.right                  # узел 1
    lca = lca_binary_tree(root2, p_node, q_node)
    print(f"  LCA(5, 1) = {lca.val}")     # 3

    # Binary Lifting LCA
    lca_bl = BinaryLiftingLCA(5, [(0, 1), (1, 2), (1, 3), (3, 4)], root=0)
    print(f"  BinaryLifting LCA(2, 4) = {lca_bl.query(2, 4)}")  # 1

    # --- Сериализация ---
    print("\n[7] Сериализация дерева")
    s = serialize(root)
    print(f"  Сериализовано: {s}")
    restored = deserialize(s)
    print(f"  Inorder восстановленного: {inorder_iterative(restored)}")
