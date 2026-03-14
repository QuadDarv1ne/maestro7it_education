"""
ГРАФОВЫЕ АЛГОРИТМЫ (GRAPH ALGORITHMS)

Граф — это структура данных, состоящая из вершин (узлов) и рёбер (связей между вершинами).
Графы используются для моделирования социальных сетей, дорожных карт, зависимостей задач и многого другого.

Основные представления графа:
1. Матрица смежности — двумерный массив, graph[i][j] = 1 если есть ребро
2. Список смежности — словарь, где ключ — вершина, значение — список соседей

Основные алгоритмы:
1. Поиск в ширину (BFS) — обход по уровням
2. Поиск в глубину (DFS) — обход вглубь
3. Алгоритм Дейкстры — кратчайшие пути от одной вершины
4. Алгоритм Флойда-Уоршелла — кратчайшие пути между всеми парами
5. Топологическая сортировка — порядок для DAG
6. Поиск компонент связности
"""


# ===== ПРЕДСТАВЛЕНИЯ ГРАФА =====

class Graph:
    """
    Класс для представления графа в виде списков смежности.
    
    Атрибуты:
        adj_list: словарь {вершина: [соседи]}
        directed: ориентированный ли граф
    """
    
    def __init__(self, directed=False):
        self.adj_list = {}
        self.directed = directed
    
    def add_edge(self, u, v):
        """Добавить ребро между вершинами u и v."""
        if u not in self.adj_list:
            self.adj_list[u] = []
        if v not in self.adj_list:
            self.adj_list[v] = []
        
        self.adj_list[u].append(v)
        if not self.directed:
            self.adj_list[v].append(u)
    
    def get_neighbors(self, v):
        """Получить список соседей вершины v."""
        return self.adj_list.get(v, [])
    
    def get_vertices(self):
        """Получить список всех вершин."""
        return list(self.adj_list.keys())


# ===== ПОИСК В ШИРИНУ (BFS) =====

from collections import deque

def bfs(graph, start):
    """
    Поиск в ширину (Breadth-First Search).
    
    Обходит граф по уровням: сначала все вершины на расстоянии 1 от start,
    затем все на расстоянии 2, и т.д.
    
    Аргументы:
        graph: объект Graph или словарь списков смежности
        start: начальная вершина
    
    Возвращает:
        list: порядок обхода вершин
    
    Сложность: O(V + E)
    
    Применение:
    - Кратчайший путь в невзвешенном графе
    - Поиск компонент связности
    - Проверка двудольности графа
    
    Пример:
        >>> g = {0: [1, 2], 1: [2], 2: [0, 3], 3: [3]}
        >>> bfs(g, 2)
        [2, 0, 3, 1]
    """
    if isinstance(graph, Graph):
        adj = graph.adj_list
    else:
        adj = graph
    
    visited = set()
    queue = deque([start])
    result = []
    
    while queue:
        v = queue.popleft()
        if v not in visited:
            visited.add(v)
            result.append(v)
            
            for neighbor in adj.get(v, []):
                if neighbor not in visited:
                    queue.append(neighbor)
    
    return result


def bfs_shortest_path(graph, start, end):
    """
    Кратчайший путь между двумя вершинами (невзвешенный граф).
    
    Использует BFS для нахождения пути с минимальным количеством рёбер.
    
    Аргументы:
        graph: словарь списков смежности
        start: начальная вершина
        end: конечная вершина
    
    Возвращает:
        list: путь от start до end или пустой список
    
    Сложность: O(V + E)
    """
    if isinstance(graph, Graph):
        adj = graph.adj_list
    else:
        adj = graph
    
    if start == end:
        return [start]
    
    visited = {start}
    queue = deque([(start, [start])])
    
    while queue:
        v, path = queue.popleft()
        
        for neighbor in adj.get(v, []):
            if neighbor == end:
                return path + [neighbor]
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    
    return []


# ===== ПОИСК В ГЛУБИНУ (DFS) =====

def dfs(graph, start):
    """
    Поиск в глубину (Depth-First Search).
    
    Обходит граф, идя как можно глубже по каждой ветке,
    прежде чем возвращаться назад.
    
    Аргументы:
        graph: объект Graph или словарь списков смежности
        start: начальная вершина
    
    Возвращает:
        list: порядок обхода вершин
    
    Сложность: O(V + E)
    
    Применение:
    - Топологическая сортировка
    - Поиск компонент сильной связности
    - Обнаружение циклов
    
    Пример:
        >>> g = {0: [1, 2], 1: [2], 2: [0, 3], 3: [3]}
        >>> dfs(g, 2)
        [2, 0, 1, 3]
    """
    if isinstance(graph, Graph):
        adj = graph.adj_list
    else:
        adj = graph
    
    visited = set()
    result = []
    
    def dfs_helper(v):
        visited.add(v)
        result.append(v)
        for neighbor in adj.get(v, []):
            if neighbor not in visited:
                dfs_helper(neighbor)
    
    dfs_helper(start)
    return result


def dfs_iterative(graph, start):
    """
    Итеративная версия DFS с использованием стека.
    
    Полезна, когда рекурсия может вызвать переполнение стека.
    """
    if isinstance(graph, Graph):
        adj = graph.adj_list
    else:
        adj = graph
    
    visited = set()
    stack = [start]
    result = []
    
    while stack:
        v = stack.pop()
        if v not in visited:
            visited.add(v)
            result.append(v)
            # Добавляем соседей в обратном порядке для правильного обхода
            for neighbor in reversed(adj.get(v, [])):
                if neighbor not in visited:
                    stack.append(neighbor)
    
    return result


# ===== ТОПОЛОГИЧЕСКАЯ СОРТИРОВКА =====

def topological_sort(graph):
    """
    Топологическая сортировка ориентированного ациклического графа (DAG).
    
    Упорядочивает вершины так, что каждое ребро идёт от более ранней
    вершины к более поздней.
    
    Аргументы:
        graph: словарь списков смежности {вершина: [соседи]}
    
    Возвращает:
        list: топологически упорядоченный список вершин
              или None, если есть цикл
    
    Сложность: O(V + E)
    
    Применение:
    - Порядок выполнения задач с зависимостями
    - Компиляция модулей
    - Расписание курсов
    
    Пример:
        >>> g = {5: [2, 0], 4: [0, 1], 2: [3], 3: [1]}
        >>> topological_sort(g)  # Один из возможных результатов
        [5, 4, 2, 0, 3, 1]
    """
    if isinstance(graph, Graph):
        adj = graph.adj_list
    else:
        adj = graph
    
    visited = set()
    rec_stack = set()  # Стек рекурсии для обнаружения циклов
    result = []
    
    def dfs_topo(v):
        if v in rec_stack:
            return False  # Цикл обнаружен
        if v in visited:
            return True
        
        visited.add(v)
        rec_stack.add(v)
        
        for neighbor in adj.get(v, []):
            if not dfs_topo(neighbor):
                return False
        
        rec_stack.remove(v)
        result.insert(0, v)  # Добавляем в начало
        return True
    
    for v in adj:
        if v not in visited:
            if not dfs_topo(v):
                return None  # Цикл
    
    return result


# ===== КОМПОНЕНТЫ СВЯЗНОСТИ =====

def connected_components(graph):
    """
    Поиск всех компонент связности в неориентированном графе.
    
    Аргументы:
        graph: словарь списков смежности
    
    Возвращает:
        list: список компонент (каждая — список вершин)
    
    Сложность: O(V + E)
    """
    if isinstance(graph, Graph):
        adj = graph.adj_list
    else:
        adj = graph
    
    visited = set()
    components = []
    
    def dfs_component(v, component):
        visited.add(v)
        component.append(v)
        for neighbor in adj.get(v, []):
            if neighbor not in visited:
                dfs_component(neighbor, component)
    
    for v in adj:
        if v not in visited:
            component = []
            dfs_component(v, component)
            components.append(component)
    
    return components


# ===== АЛГОРИТМ ДЕЙКСТРЫ =====

import heapq

def dijkstra(graph, start):
    """
    Алгоритм Дейкстры для поиска кратчайших путей.
    
    Находит кратчайшие расстояния от start до всех остальных вершин
    во взвешенном графе с неотрицательными весами.
    
    Аргументы:
        graph: словарь {вершина: [(сосед, вес), ...]}
        start: начальная вершина
    
    Возвращает:
        dict: {вершина: расстояние от start}
    
    Сложность: O((V + E) log V) с двоичной кучей
    
    Пример:
        >>> g = {0: [(1, 4), (2, 1)], 1: [(3, 1)], 2: [(1, 2), (3, 5)], 3: []}
        >>> dijkstra(g, 0)
        {0: 0, 1: 3, 2: 1, 3: 4}
    """
    distances = {v: float('inf') for v in graph}
    distances[start] = 0
    
    # (расстояние, вершина)
    heap = [(0, start)]
    visited = set()
    
    while heap:
        dist, v = heapq.heappop(heap)
        
        if v in visited:
            continue
        visited.add(v)
        
        for neighbor, weight in graph.get(v, []):
            new_dist = dist + weight
            if new_dist < distances.get(neighbor, float('inf')):
                distances[neighbor] = new_dist
                heapq.heappush(heap, (new_dist, neighbor))
    
    return distances


def dijkstra_path(graph, start, end):
    """
    Кратчайший путь между двумя вершинами (алгоритм Дейкстры).
    
    Возвращает:
        tuple: (расстояние, путь) или (inf, []) если путь не существует
    """
    distances = {v: float('inf') for v in graph}
    distances[start] = 0
    predecessors = {start: None}
    
    heap = [(0, start)]
    visited = set()
    
    while heap:
        dist, v = heapq.heappop(heap)
        
        if v == end:
            # Восстанавливаем путь
            path = []
            current = end
            while current is not None:
                path.append(current)
                current = predecessors[current]
            return dist, path[::-1]
        
        if v in visited:
            continue
        visited.add(v)
        
        for neighbor, weight in graph.get(v, []):
            new_dist = dist + weight
            if new_dist < distances.get(neighbor, float('inf')):
                distances[neighbor] = new_dist
                predecessors[neighbor] = v
                heapq.heappush(heap, (new_dist, neighbor))
    
    return float('inf'), []


# ===== АЛГОРИТМ ФЛОЙДА-УОРШЕЛЛА =====

def floyd_warshall(graph, n):
    """
    Алгоритм Флойда-Уоршелла для кратчайших путей между всеми парами.
    
    Аргументы:
        graph: словарь {(u, v): вес} или матрица смежности
        n: количество вершин
    
    Возвращает:
        list[list]: матрица расстояний distance[i][j] = кратчайшее расстояние
    
    Сложность: O(V³)
    
    Применение:
    - Кратчайшие пути между всеми парами
    - Обнаружение отрицательных циклов
    - Транзитивное замыкание
    """
    # Инициализация матрицы расстояний
    dist = [[float('inf')] * n for _ in range(n)]
    
    for i in range(n):
        dist[i][i] = 0
    
    if isinstance(graph, dict):
        for (u, v), w in graph.items():
            dist[u][v] = w
    else:
        for i in range(n):
            for j in range(n):
                if graph[i][j] != 0:
                    dist[i][j] = graph[i][j]
    
    # Основной алгоритм
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    
    return dist


# ===== ОБНАРУЖЕНИЕ ЦИКЛОВ =====

def has_cycle(graph):
    """
    Проверка наличия цикла в ориентированном графе.
    
    Аргументы:
        graph: словарь списков смежности
    
    Возвращает:
        bool: True если есть цикл
    
    Сложность: O(V + E)
    """
    if isinstance(graph, Graph):
        adj = graph.adj_list
    else:
        adj = graph
    
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {v: WHITE for v in adj}
    
    def dfs_cycle(v):
        color[v] = GRAY
        for neighbor in adj.get(v, []):
            if color.get(neighbor, WHITE) == GRAY:
                return True
            if color.get(neighbor, WHITE) == WHITE and dfs_cycle(neighbor):
                return True
        color[v] = BLACK
        return False
    
    for v in adj:
        if color[v] == WHITE:
            if dfs_cycle(v):
                return True
    
    return False


if __name__ == "__main__":
    print(__doc__)
    print("\n" + "="*60)
    
    # Создаём граф
    g = Graph()
    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(1, 2)
    g.add_edge(2, 0)
    g.add_edge(2, 3)
    g.add_edge(3, 3)
    
    print("Обходы графа:")
    print(f"  BFS от 2: {bfs(g, 2)}")
    print(f"  DFS от 2: {dfs(g, 2)}")
    
    # Взвешенный граф для Дейкстры
    weighted = {
        0: [(1, 4), (2, 1)],
        1: [(3, 1)],
        2: [(1, 2), (3, 5)],
        3: []
    }
    
    print("\nАлгоритм Дейкстры от вершины 0:")
    distances = dijkstra(weighted, 0)
    for v, d in sorted(distances.items()):
        print(f"  До {v}: {d}")
    
    # Топологическая сортировка
    dag = {5: [2, 0], 4: [0, 1], 2: [3], 3: [1], 0: [], 1: []}
    print(f"\nТопологическая сортировка: {topological_sort(dag)}")
    
    # Компоненты связности
    components_graph = {0: [1], 1: [0, 2], 2: [1], 3: [4], 4: [3], 5: []}
    print(f"\nКомпоненты связности: {connected_components(components_graph)}")
