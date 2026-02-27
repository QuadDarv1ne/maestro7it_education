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
    def minOperations(self, s, k):
        """
        Возвращает минимальное количество операций, необходимых для превращения
        всех символов бинарной строки s в '1'. За одну операцию можно выбрать
        ровно k различных индексов и инвертировать каждый бит.
        Если это невозможно, возвращает -1.

        Алгоритм: BFS по состояниям (количество нулей) с оптимизацией на основе
        DSU (структура данных "пересекающиеся множества") для быстрого перебора
        непосещённых состояний в непрерывном диапазоне.
        """
        n = len(s)
        z0 = s.count('0')
        if z0 == 0:
            return 0

        # DSU для чётных и нечётных состояний (индексы от 0 до n+2)
        parent_even = list(range(n + 3))
        parent_odd = list(range(n + 3))

        def find(parent, x):
            if parent[x] != x:
                parent[x] = find(parent, parent[x])
            return parent[x]

        def mark_visited(z):
            if z % 2 == 0:
                parent_even[z] = find(parent_even, z + 2)
            else:
                parent_odd[z] = find(parent_odd, z + 2)

        from collections import deque
        q = deque()
        q.append((z0, 0))
        mark_visited(z0)

        while q:
            z, dist = q.popleft()

            # Вычисляем диапазон возможных новых количеств нулей
            max_i = min(k, z)
            min_i = max(0, k - (n - z))
            low = z + k - 2 * max_i
            high = z + k - 2 * min_i
            if low > high:
                continue

            target_parity = (z + k) % 2
            parent = parent_even if target_parity == 0 else parent_odd

            # Корректируем low до нужной чётности
            if low % 2 != target_parity:
                low += 1
            if low > high:
                continue

            # Перебираем все непосещённые состояния в [low, high] с нужной чётностью
            x = find(parent, low)
            while x <= high and x <= n:
                if x == 0:
                    return dist + 1
                q.append((x, dist + 1))
                parent[x] = find(parent, x + 2)  # помечаем как посещённое
                x = find(parent, x)

        return -1