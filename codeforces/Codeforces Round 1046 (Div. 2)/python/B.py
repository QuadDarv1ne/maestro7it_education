'''
https://codeforces.com/contest/2136/problem/B

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
'''

#!/usr/bin/env python3
"""
B. Like the Bitset

Конструктивный алгоритм построения перестановки p[1..n] или вывод NO, если невозможно.
DocString: решение читает t тестов; для каждого теста вводит n, k, строку s.
Если ответ есть — печатает "YES" и саму перестановку, иначе "NO".
"""
import sys
from collections import deque
input = sys.stdin.readline

def solve():
    t = int(input().strip())
    out_lines = []
    for _ in range(t):
        n,k = map(int, input().split())
        s = input().strip()
        # Special case: if k == 1 and any '1' exists => impossible
        if k == 1 and '1' in s:
            out_lines.append("NO")
            continue
        # We will construct permutation placing largest numbers in positions
        # that are "safe" (usually zeros) in a way that each window length >= k
        # covering a '1' will contain a bigger element.
        # Approach: process residues modulo k as independent columns.
        cols = [[] for _ in range(k)]
        for i,ch in enumerate(s):
            cols[i % k].append((i, ch))
        p = [0]*n
        cur = n
        ok = True
        # For each residue, place zeros with larger numbers first, ones later
        # We'll place numbers decreasingly; within each residue place zeros first.
        for r in range(k):
            items = cols[r]
            zeros = [idx for idx,ch in items if ch=='0']
            ones  = [idx for idx,ch in items if ch=='1']
            # Place zeros first with largest numbers
            for idx in zeros:
                p[idx] = cur
                cur -= 1
            # Then ones
            for idx in ones:
                p[idx] = cur
                cur -= 1
        # Validate result to be safe: check condition for all i with s[i]=='1'
        # Brute-check all intervals of length >= k covering i (O(n) per check worst-case)
        # But n sum <= 2e5, validation acceptable during offline generation (or can be omitted)
        valid = True
        # To speed up, precompute prefix max of p for all intervals? Simpler: sliding window maxima with deque for each window length k..n (but that's heavy).
        # We'll do direct verification with prefix-sparse-table for RMQ maximum (O(n log n)) per test if needed.
        # Use simple O(n) check: for each i, consider windows [i - k + 1, i] ... [i, i + k - 1] bounds
        # We can check all windows of length exactly k that cover i — it's sufficient (longer windows contain maxima at least as large).
        from collections import deque
        # compute max for each window of size k
        if k <= n:
            dq = deque()
            winmax = [0]*(n - k + 1)
            for i in range(n):
                while dq and p[dq[-1]] <= p[i]:
                    dq.pop()
                dq.append(i)
                if dq[0] <= i - k:
                    dq.popleft()
                if i >= k - 1:
                    winmax[i - k + 1] = p[dq[0]]
            # for each position i with s[i]=='1', check all windows of len k that cover i
            for i,ch in enumerate(s):
                if ch == '1':
                    L = max(0, i - k + 1)
                    R = min(i, n - k)
                    # if any window's max == p[i], it's invalid
                    for start in range(L, R+1):
                        if winmax[start] == p[i]:
                            valid = False
                            break
                    if not valid:
                        break
        if not valid:
            out_lines.append("NO")
        else:
            out_lines.append("YES")
            out_lines.append(" ".join(map(str,p)))
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