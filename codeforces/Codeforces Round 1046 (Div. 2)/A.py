'''
https://codeforces.com/contest/2136/problem/A
'''

#!/usr/bin/env python3
"""
A. In the Dream

Проверяет, может ли сон осуществиться:
в каждой половине матча запрещено иметь три подряд голов одной команды.
Вход:
    t
    a b c d   (для каждого теста; 0 <= a <= c <= 100, 0 <= b <= d <= 100)
Выход:
    для каждого теста "YES" или "NO".
"""
import sys
input = sys.stdin.readline

def max_allowed(L: int) -> int:
    # ceil(2L / 3)
    return (2 * L + 2) // 3

def solve():
    t = int(input().strip())
    res = []
    for _ in range(t):
        a,b,c,d = map(int, input().split())
        ok = True
        L1 = a + b
        if max(a, b) > max_allowed(L1):
            ok = False
        L2 = (c - a) + (d - b)
        if max(c - a, d - b) > max_allowed(L2):
            ok = False
        res.append("YES" if ok else "NO")
    print("\n".join(res))

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