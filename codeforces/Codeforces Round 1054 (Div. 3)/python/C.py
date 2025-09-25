'''
https://codeforces.com/contest/2149/problem/C
'''

import sys

def solve():
    """
    C. MEX rose

    Находит минимальное число операций (замен элементов на числа из [0,n]), чтобы получить MEX(a) = k.

    Исправление:
    - Если текущий mex == k -> 0 операций.
    - Если mex > k -> нужно убрать все вхождения числа k -> ответ = count_k.
    - Если mex < k -> необходимо добавить все отсутствующие числа из [0..k-1], но одновременно можно
      превращать существующие элементы, равные k, в недостающие значения. Поэтому минимум операций
      равен max(количество отсутствующих в [0..k-1], количество вхождений числа k).
    Сложность: O(n) на тест.
    """
    it = iter(sys.stdin.read().strip().split())
    t = int(next(it))
    out = []
    for _ in range(t):
        n = int(next(it)); k = int(next(it))
        arr = [int(next(it)) for _ in range(n)]
        present = [0] * (n + 1)
        for v in arr:
            if 0 <= v <= n:
                present[v] += 1
        # compute mex
        mex = 0
        while mex <= n and present[mex] > 0:
            mex += 1
        count_k = present[k] if 0 <= k <= n else 0
        if mex == k:
            out.append("0")
        elif mex > k:
            out.append(str(count_k))
        else:  # mex < k
            missing = sum(1 for x in range(0, k) if present[x] == 0)
            out.append(str(max(missing, count_k)))
    print("\n".join(out))

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