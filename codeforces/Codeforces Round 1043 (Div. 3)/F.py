'''
https://codeforces.com/contest/2132/problem/F
'''

def solve():
    """
    Решение задачи «Rada and the Chamomile Valley». Находим рёбра, через которые обязательно пройдут все пути от 1 до n.
    Алгоритм:
    1) Строим список смежности графа, помечая номера рёбер.
    2) С помощью DFS находим мосты (считаем глубины и low-link).
    3) Удаляем мосты (или помечаем) и строим компоненты двусвязности (2-EDGE-компоненты).
    4) Если вершины 1 и n в одной компоненте, то нет обязательных рёбер — отвечаем -1 на все запросы.
       Иначе строим дерево компонентов по мостам и находим путь между компонентами 1 и n, получаем список обязательных рёбер.
    5) Делаем мульти-источник BFS (с приоритетом по расстоянию и индексу ребра) от всех концов этих обязательных рёбер,
       чтобы для каждой вершины найти ближайшее обязательное ребро.
    6) На каждый запрос выводим соответствующий индекс ребра или -1, если таких нет.
    """
    import sys
    sys.setrecursionlimit(1000000)
    input = sys.stdin.readline
    t = int(input())
    for _ in range(t):
        n,m = map(int, input().split())
        adj = [[] for _ in range(n+1)]
        edges = []
        for idx in range(1, m+1):
            u,v = map(int, input().split())
            adj[u].append((v,idx))
            adj[v].append((u,idx))
            edges.append((u,v))
        # Находим мосты: DFS для discovery and low
        visited = [False]*(n+1)
        tin = [0]*(n+1)
        low = [0]*(n+1)
        timer = 0
        is_bridge = [False]*(m+1)
        def dfs(u, pe):
            nonlocal timer
            visited[u] = True
            timer += 1
            tin[u] = low[u] = timer
            for v, ei in adj[u]:
                if ei == pe: 
                    continue
                if visited[v]:
                    low[u] = min(low[u], tin[v])
                else:
                    dfs(v, ei)
                    low[u] = min(low[u], low[v])
                    if low[v] > tin[u]:
                        # ребро u-v является мостом
                        is_bridge[ei] = True
        dfs(1, -1)
        # Построим компоненты 2-edge-connected: удаляем мосты из графа
        comp = [0]*(n+1)
        comp_id = 0
        for i in range(1, n+1):
            if not comp[i]:
                comp_id += 1
                stack = [i]
                comp[i] = comp_id
                while stack:
                    u = stack.pop()
                    for v, ei in adj[u]:
                        if comp[v] == 0 and not is_bridge[ei]:
                            comp[v] = comp_id
                            stack.append(v)
        c1 = comp[1]
        cN = comp[n]
        if c1 == cN:
            # Нет обязательных ребер
            q = int(input())
            for _ in range(q):
                input()
                print(-1)
            continue
        # Строим дерево компонент и находим путь компонентов c1 -> cN
        comp_adj = [[] for _ in range(comp_id+1)]
        for ei in range(1, m+1):
            if is_bridge[ei]:
                u,v = edges[ei-1]
                cu, cv = comp[u], comp[v]
                comp_adj[cu].append((cv, ei))
                comp_adj[cv].append((cu, ei))
        # Находим путь через BFS
        parent = [-1]*(comp_id+1)
        pedge = [0]*(comp_id+1)
        queue = [c1]
        parent[c1] = c1
        for u in queue:
            for v, ei in comp_adj[u]:
                if parent[v] == -1:
                    parent[v] = u
                    pedge[v] = ei
                    queue.append(v)
        # Восстанавливаем путь
        path_edges = []
        cur = cN
        while cur != c1:
            path_edges.append(pedge[cur])
            cur = parent[cur]
        # Мульти-источник BFS от концов обязательных рёбер
        import heapq
        best = [(10**18, 10**18)] * (n+1)  # (dist, edge_index)
        hq = []
        for ei in path_edges:
            u,v = edges[ei-1]
            # Добавляем концы как источники (расстояние 0)
            if best[u] > (0, ei):
                best[u] = (0, ei)
                heapq.heappush(hq, (0, ei, u))
            if best[v] > (0, ei):
                best[v] = (0, ei)
                heapq.heappush(hq, (0, ei, v))
        # Стандартный Dijkstra-like BFS на графе (вес ребра =1, но храним приоритет по (dist, edge_index))
        while hq:
            dist, ei, u = heapq.heappop(hq)
            if best[u] < (dist, ei):
                continue
            for w, _ in adj[u]:
                nd = dist + 1
                if (nd, ei) < best[w]:
                    best[w] = (nd, ei)
                    heapq.heappush(hq, (nd, ei, w))
        # Отвечаем на запросы
        q = int(input())
        for _ in range(q):
            c = int(input())
            if best[c][0] == 10**18:
                print(-1)
            else:
                print(best[c][1])

if __name__ == "__main__":
    solve()

''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks