'''
https://codeforces.com/contest/2149/problem/B
'''

import sys

def solve():
    """
    B. Unconventional Pairs

    Идея:
    - Чтобы минимизировать максимальную разницу в парах, отсортируем массив и будем паровать соседей:
      (a0,a1),(a2,a3),...
    - Ответ — максимум по a[2*i+1] - a[2*i].
    Обоснование: для минимакс-задач такого рода оптимально паровать соседей в отсортированном порядке.
    Сложность: O(n log n) на тест.
    """
    it = iter(sys.stdin.read().strip().split())
    t = int(next(it))
    out = []
    for _ in range(t):
        n = int(next(it))
        arr = [int(next(it)) for _ in range(n)]
        arr.sort()
        ans = 0
        for i in range(0, n, 2):
            ans = max(ans, arr[i+1] - arr[i])
        out.append(str(ans))
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