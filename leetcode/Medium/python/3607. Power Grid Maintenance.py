# Python
import heapq
from collections import defaultdict

class Solution:
    """
    Обрабатывает запросы обслуживания энергосети.
    Использует Union-Find для группировки станций и min-heap для поиска минимальной онлайн станции.
    
    Сложность по времени: O((c + n + q) * α(c))
    Сложность по памяти: O(c)
    """
    
    def processQueries(self, c, connections, queries):
        parent = list(range(c + 1))
        
        # Функция поиска корня с path compression
        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]
        
        # Объединение двух компонент
        def unite(x, y):
            parent[find(x)] = find(y)
        
        # Строим граф связей
        for u, v in connections:
            unite(u, v)
        
        # Создаем min-heap для каждой компоненты
        comp = defaultdict(list)
        for i in range(1, c + 1):
            heapq.heappush(comp[find(i)], i)
        
        offline = [False] * (c + 1)
        result = []
        
        # Обрабатываем запросы
        for query in queries:
            query_type, x = query[0], query[1]
            
            if query_type == 2:
                # Запрос типа 2: станция переходит в оффлайн
                offline[x] = True
            else:
                # Запрос типа 1: поиск онлайн станции для обслуживания
                if not offline[x]:
                    result.append(x)
                else:
                    root = find(x)
                    heap = comp[root]
                    
                    # Lazy deletion: удаляем оффлайн станции из heap
                    while heap and offline[heap[0]]:
                        heapq.heappop(heap)
                    
                    result.append(heap[0] if heap else -1)
        
        return result