'''
https://codeforces.com/contest/2149/problem/G
'''

import sys
from bisect import bisect_left, bisect_right
from collections import defaultdict

class SegTree:
    def __init__(self, a):
        self.n = len(a)
        self.size = 1
        while self.size < self.n:
            self.size <<= 1
        # tree nodes: list of (val,count) candidates (dict-like but small)
        self.tree = [dict() for _ in range(2*self.size)]
        for i in range(self.n):
            self.tree[self.size + i] = {a[i]: 1}
        for i in range(self.size - 1, 0, -1):
            self.tree[i] = self._merge(self.tree[2*i], self.tree[2*i+1])

    def _merge(self, A, B):
        # A and B are dicts val->count (approx votes)
        res = dict(A)  # shallow copy
        for v, c in B.items():
            res[v] = res.get(v, 0) + c
        # если более 2 кандидатов — уменьшаем голоса на min_count, удаляя нулевые
        while len(res) > 2:
            m = min(res.values())
            keys = list(res.keys())
            for k in keys:
                res[k] -= m
                if res[k] == 0:
                    del res[k]
        return res

    def query(self, l, r):
        # возвращает dict кандидатов (<=2) для отрезка [l,r] (0-based)
        l += self.size; r += self.size
        left_nodes = {}
        right_nodes = {}
        while l <= r:
            if (l & 1) == 1:
                left_nodes = self._merge(left_nodes, self.tree[l])
                l += 1
            if (r & 1) == 0:
                right_nodes = self._merge(self.tree[r], right_nodes)
                r -= 1
            l >>= 1; r >>= 1
        res = self._merge(left_nodes, right_nodes)
        return list(res.keys())

def solve():
    """
    G. Buratsuta 3

    Подход:
    - Строим сегментное дерево, где в каждом узле храним до двух "кандидатов" (алгоритм обобщённого majority).
    - Для запроса получаем <=2 кандидатов, затем для каждого считаем реальную частоту на отрезке
      используя предварительно карту позиций (списки индексов и бинарный поиск).
    - Выводим найденные элементы (в отсортированном порядке) или -1.
    Сложность: O((n+q) log n), память O(n).
    """
    it = iter(sys.stdin.read().strip().split())
    t = int(next(it))
    out_lines = []
    for _ in range(t):
        n = int(next(it)); q = int(next(it))
        arr = [int(next(it)) for _ in range(n)]
        pos = defaultdict(list)
        for i, v in enumerate(arr):
            pos[v].append(i)
        st = SegTree(arr)
        for _q in range(q):
            l = int(next(it)) - 1; r = int(next(it)) - 1
            cand = st.query(l, r)
            ans = []
            threshold = (r - l + 1) // 3  # strictly more than floor(len/3) => > threshold
            for v in cand:
                indices = pos[v]
                cnt = bisect_right(indices, r) - bisect_left(indices, l)
                if cnt > threshold:
                    ans.append(v)
            if not ans:
                out_lines.append("-1")
            else:
                ans.sort()
                out_lines.append(" ".join(map(str, ans)))
    print("\n".join(out_lines))

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