'''
https://codeforces.com/contest/2149/problem/E
'''

import sys
from collections import defaultdict

def count_at_most_k_len_le(arr, k, R):
    """
    Возвращает количество подмассивов с <= k различных чисел и длиной <= R.
    Для каждого правого конца r поддерживаем левый указатель L_k такой, что
    [L_k, r] имеет <= k различных, тогда число левых позиций, удовлетворяющих
    длине <= R равно max(0, r - max(L_k, r-R+1) + 1).
    Сложность O(n).
    """
    if R <= 0:
        return 0
    n = len(arr)
    cnt = defaultdict(int)
    distinct = 0
    L = 0
    total = 0
    for r in range(n):
        x = arr[r]
        if cnt[x] == 0:
            distinct += 1
        cnt[x] += 1
        while distinct > k:
            y = arr[L]
            cnt[y] -= 1
            if cnt[y] == 0:
                distinct -= 1
            L += 1
        left_bound = max(L, r - R + 1)
        if left_bound <= r:
            total += (r - left_bound + 1)
    return total

def solve():
    """
    E. Hidden Knowledge of the Ancients

    Идея:
    Количество подмассивов с ровно k различными и длиной в [l, r] =
      (at_most(k, r) - at_most(k, l-1)) - (at_most(k-1, r) - at_most(k-1, l-1))
    Где at_most(x, R) считает подмассивы с <= x различных и длиной <= R.
    Общая сложность: O(n) на тест + логика (используем два раза по k и k-1).
    """
    it = iter(sys.stdin.read().strip().split())
    t = int(next(it))
    out_lines = []
    for _ in range(t):
        n = int(next(it)); k = int(next(it)); l = int(next(it)); r = int(next(it))
        arr = [int(next(it)) for _ in range(n)]
        def at_most_x_R(x, R):
            return count_at_most_k_len_le(arr, x, R)
        ans = (at_most_x_R(k, r) - at_most_x_R(k, l-1)) - (at_most_x_R(k-1, r) - at_most_x_R(k-1, l-1))
        out_lines.append(str(ans))
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