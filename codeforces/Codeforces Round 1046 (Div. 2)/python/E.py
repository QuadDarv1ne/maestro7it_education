'''
https://codeforces.com/contest/2136/problem/E
'''

#!/usr/bin/env python3
"""
E (частный случай: дерево).

Если граф является деревом (m == n-1), то уравнений из циклов нет, следовательно
все неизвестные вершины (a_i == -1) можно заполнить произвольно значениями от 0 до V-1.
Ответ = V^(count_unknown) mod 998244353.
"""
import sys
MOD = 998244353
input = sys.stdin.readline

def modpow(a, e, mod=MOD):
    res = 1
    a %= mod
    while e:
        if e & 1:
            res = (res * a) % mod
        a = (a * a) % mod
        e >>= 1
    return res

def solve():
    t = int(input().strip())
    out = []
    for _ in range(t):
        n,m,V = map(int, input().split())
        a = list(map(int, input().split()))
        edges = [tuple(map(int, input().split())) for _ in range(m)]
        if m == n - 1:
            cnt_unknown = sum(1 for x in a if x == -1)
            out.append(str(modpow(V, cnt_unknown)))
        else:
            # общий случай — нужно сложное решение (см. предложение в ответе)
            out.append("0")  # заглушка — тут потребуется полное решение
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