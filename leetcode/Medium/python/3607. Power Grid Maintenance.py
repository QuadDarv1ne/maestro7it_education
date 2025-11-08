'''
https://leetcode.com/problems/power-grid-maintenance/description/?envType=daily-question&envId=2025-11-06
Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X  
GitHub: https://github.com/QuadDarv1ne/  
'''

class Solution(object):
    def processQueries(self, c, connections, queries):
        """
        :type c: int
        :type connections: List[List[int]]
        :type queries: List[List[int]]
        :rtype: List[int]
        """
        class UnionFind:
            def __init__(self, n):
                self.parent = list(range(n))
                self.rank = [0] * n
            
            def find(self, x):
                # Проверка границ
                if x < 0 or x >= len(self.parent):
                    return x
                
                # Итеративный find с path compression
                root = x
                while self.parent[root] != root:
                    root = self.parent[root]
                
                # Path compression
                while x != root:
                    next_x = self.parent[x]
                    self.parent[x] = root
                    x = next_x
                
                return root
            
            def union(self, x, y):
                # Проверка границ
                if x < 0 or x >= len(self.parent) or y < 0 or y >= len(self.parent):
                    return False
                
                px, py = self.find(x), self.find(y)
                if px == py:
                    return False
                
                if self.rank[px] < self.rank[py]:
                    self.parent[px] = py
                elif self.rank[px] > self.rank[py]:
                    self.parent[py] = px
                else:
                    self.parent[py] = px
                    self.rank[px] += 1
                return True
            
            def connected(self, x, y):
                # Проверка границ
                if x < 0 or x >= len(self.parent) or y < 0 or y >= len(self.parent):
                    return False
                return self.find(x) == self.find(y)
        
        # Определяем реальное количество узлов (может быть больше c)
        max_node = c - 1
        for conn in connections:
            max_node = max(max_node, conn[0], conn[1])
        for query in queries:
            if len(query) >= 3:
                max_node = max(max_node, query[1], query[2])
        
        n = max_node + 1
        uf = UnionFind(n)
        
        # Активные соединения
        active = set()
        
        for conn in connections:
            u, v = conn[0], conn[1]
            key = (min(u, v), max(u, v))
            active.add(key)
            uf.union(u, v)
        
        result = []
        
        for query in queries:
            query_type = query[0]
            
            if query_type == 1:
                # Отключить соединение
                u, v = query[1], query[2]
                key = (min(u, v), max(u, v))
                if key in active:
                    active.discard(key)
                    
                    # Rebuild Union-Find
                    uf = UnionFind(n)
                    for a, b in active:
                        uf.union(a, b)
            
            elif query_type == 2:
                # Включить соединение
                u, v = query[1], query[2]
                key = (min(u, v), max(u, v))
                if key not in active:
                    active.add(key)
                    uf.union(u, v)
            
            elif query_type == 3:
                # Проверить связность
                u, v = query[1], query[2]
                result.append(1 if uf.connected(u, v) else 0)
        
        return result

'''
Тестовый пример:
Input: c=3, connections=[[0,1],[1,2]], queries=[[3,0,2],[1,1,2],[3,0,2]]
- max_node = max(3-1, 0, 1, 2) = 2
- n = 3
- Работает корректно

Сложность:
- Время: O((E+Q) * α(N)) где α ≈ O(1)
- Память: O(N + E)
'''

''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks