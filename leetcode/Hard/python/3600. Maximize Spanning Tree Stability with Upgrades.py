"""
Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Полезные ссылки:
1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
2. Telegram №1 @quadd4rv1n7
3. Telegram №2 @dupley_maxim_1999
4. Rutube канал: https://rutube.ru/channel/4218729/
5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
6. YouTube канал: https://www.youtube.com/@it-coders
7. ВК группа: https://vk.com/science_geeks
"""

class Solution:
    def maxStability(self, n, edges, k):
        """
        Находит максимально возможную стабильность остовного дерева.

        Стабильность дерева равна минимальной прочности среди всех его рёбер.
        Можно выполнить не более k улучшений, каждое из которых удваивает прочность
        одного необязательного ребра (musti == 0). Обязательные рёбра (musti == 1)
        должны быть включены в дерево и не могут быть улучшены.

        Args:
            n: Количество узлов в графе (от 0 до n-1).
            edges: Список рёбер, где каждое ребро представлено как
                   [ui, vi, si, musti]:
                   - ui, vi: вершины, соединяемые ребром (неориентированное).
                   - si: прочность ребра (целое число >= 1).
                   - musti: флаг обязательности (1 - обязательно, 0 - опционально).
            k: Максимальное количество улучшений, которое можно применить
               к опциональным рёбрам.

        Returns:
            Максимально возможную стабильность (целое число).
            Если невозможно построить остовное дерево, возвращается -1.
        """
        # Собираем все возможные значения стабильности для бинарного поиска
        strengths = set()
        for u, v, s, must in edges:
            strengths.add(s)
            if must == 0:
                strengths.add(s * 2)  # Улучшенная прочность
        
        # Сортируем уникальные значения
        strengths = sorted(strengths)
        
        # Бинарный поиск по ответу
        left, right = 0, len(strengths) - 1
        result = -1
        
        while left <= right:
            mid = (left + right) // 2
            target = strengths[mid]
            
            if self._can_achieve(n, edges, k, target):
                result = target
                left = mid + 1  # Пробуем найти большее значение
            else:
                right = mid - 1
        
        return result
    
    def _can_achieve(self, n, edges, k, target):
        """
        Проверяет, можно ли построить остовное дерево со стабильностью не ниже target.
        
        Args:
            n: Количество узлов
            edges: Список всех рёбер
            k: Доступное количество улучшений
            target: Целевая минимальная прочность
            
        Returns:
            True если возможно, иначе False
        """
        # Инициализируем DSU (Systema nepieriekajemnych množestv)
        parent = list(range(n))
        rank = [0] * n
        
        def find(x):
            # Поиск с сжатием пути
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]
        
        def union(x, y):
            # Объединение по рангу
            x, y = find(x), find(y)
            if x == y:
                return False
            
            if rank[x] < rank[y]:
                parent[x] = y
            elif rank[x] > rank[y]:
                parent[y] = x
            else:
                parent[y] = x
                rank[x] += 1
            return True
        
        # Разделяем рёбра на обязательные и опциональные
        mandatory_edges = []
        optional_edges = []
        
        for u, v, s, must in edges:
            if must == 1:
                mandatory_edges.append((u, v, s))
            else:
                optional_edges.append((u, v, s))
        
        # Сначала обрабатываем обязательные рёбра
        edges_used = 0
        for u, v, s in mandatory_edges:
            if s < target:
                # Обязательное ребро слабее целевой стабильности
                return False
            if union(u, v):
                edges_used += 1
        
        # Проверяем, не создали ли обязательные рёбра циклы
        # Если количество успешных union меньше количества обязательных рёбер,
        # значит есть циклы - это недопустимо для дерева
        if edges_used < len(mandatory_edges):
            return False
        
        # Подсчитываем, сколько рёбер нам ещё нужно добавить
        # Находим количество компонент связности
        components = len(set(find(i) for i in range(n)))
        edges_needed = components - 1  # Нужно добавить, чтобы соединить компоненты
        
        # Если уже всё соединено, проверяем, что это действительно остовное дерево
        if edges_needed == 0:
            # Проверяем, что использовано ровно n-1 рёбер
            return edges_used == n - 1
        
        # Сортируем опциональные рёбра: сначала те, что дают наибольшую прочность
        # Приоритет: рёбра, которые можно использовать без улучшения
        def edge_key(edge):
            u, v, s = edge
            if s >= target:
                return (float('inf'), s)  # Не требуют улучшения - высший приоритет
            else:
                return (s * 2, s)  # Требуют улучшения - сортируем по улучшенной прочности
        
        optional_edges.sort(key=edge_key, reverse=True)
        
        upgrades_used = 0
        
        # Добавляем опциональные рёбра
        for u, v, s in optional_edges:
            if edges_needed == 0:
                break
            
            # Определяем, нужно ли улучшать ребро
            need_upgrade = s < target
            
            if need_upgrade:
                # Проверяем, можем ли улучшить
                if upgrades_used >= k or s * 2 < target:
                    continue
                # Пробуем добавить после улучшения
                if union(u, v):
                    upgrades_used += 1
                    edges_needed -= 1
            else:
                # Можно добавить без улучшения
                if union(u, v):
                    edges_needed -= 1
        
        # Проверяем, что все компоненты соединены
        if edges_needed > 0:
            return False
        
        # Финальная проверка связности
        root = find(0)
        for i in range(1, n):
            if find(i) != root:
                return False
        
        return True