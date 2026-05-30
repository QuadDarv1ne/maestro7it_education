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

class Solution(object):
    def getResults(self, queries):
        """
        Обрабатывает запросы двух типов в обратном порядке:
        1: [1, x] — установить препятствие в точке x.
        2: [2, x, sz] — проверить, можно ли разместить блок размера sz на отрезке [0, x].
        
        Идея:
        - Сначала добавляем все препятствия из запросов типа 1.
        - Строим дерево Фенвика, хранящее в позиции x максимальную длину промежутка,
          заканчивающегося в точке x.
        - Обрабатываем запросы с конца:
          - Тип 2: находим последнее препятствие <= x (prev).
            Ответ = max(максимальный промежуток заканчивающийся в prev, x - prev) >= sz.
          - Тип 1: удаляем препятствие x, объединяя промежутки prev->x и x->next в prev->next.
            Обновляем дерево Фенвика для next: next - prev.
        
        :type queries: List[List[int]]
        :rtype: List[bool]
        """
        # Дерево Фенвика для хранения максимума на префиксе
        class FenwickTree:
            def __init__(self, n):
                self.vals = [0] * (n + 1)
            
            def maximize(self, i, val):
                """Обновить позицию i значением val (берем максимум)"""
                while i < len(self.vals):
                    if val > self.vals[i]:
                        self.vals[i] = val
                    i += i & -i
            
            def get(self, i):
                """Получить максимум на префиксе [1, i]"""
                res = 0
                while i > 0:
                    if self.vals[i] > res:
                        res = self.vals[i]
                    i -= i & -i
                return res
        
        n = min(50000, len(queries) * 3)
        ans = []
        tree = FenwickTree(n + 1)
        
        # Добавляем sentinel-препятствия
        obstacles = [0, n]
        
        # Сначала добавляем все препятствия из запросов типа 1
        for q in queries:
            if q[0] == 1:
                x = q[1]
                obstacles.append(x)
        
        obstacles.sort()
        
        # Строим начальное состояние дерева Фенвика
        # Для каждого соседнего препятствия: промежуток заканчивается в x2, длина = x2 - x1
        for i in range(1, len(obstacles)):
            x1 = obstacles[i - 1]
            x2 = obstacles[i]
            tree.maximize(x2, x2 - x1)
        
        # Обрабатываем запросы в обратном порядке
        for q in reversed(queries):
            if q[0] == 1:
                x = q[1]
                # Находим соседей x
                import bisect
                idx = bisect.bisect_left(obstacles, x)
                next_obs = obstacles[idx + 1]
                prev = obstacles[idx - 1]
                
                # Удаляем x
                obstacles.pop(idx)
                
                # Обновляем промежуток: теперь prev->next вместо prev->x и x->next
                tree.maximize(next_obs, next_obs - prev)
            else:
                x, sz = q[1], q[2]
                
                # Находим последнее препятствие <= x
                import bisect
                idx = bisect.bisect_right(obstacles, x) - 1
                prev = obstacles[idx]
                
                # Максимальный промежуток в [0, x]:
                # - либо полностью лежащий промежуток, заканчивающийся в prev
                # - либо расстояние от prev до x
                ans.append(tree.get(prev) >= sz or x - prev >= sz)
        
        # Разворачиваем ответ, так как обрабатывали с конца
        return ans[::-1]