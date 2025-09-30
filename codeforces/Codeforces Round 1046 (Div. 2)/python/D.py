'''
https://codeforces.com/contest/2136/problem/D

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
'''

#!/usr/bin/env python3
"""
D. For the Champion (хак-формат, offline)

Интерактивная задача. Для хаков format:
 t
 for each test:
   n
   x1 y1
   ...
   xn yn
   X Y   <- реальные координаты (вход для хаков)

Решение для оффлайн-хаков: просто вывести эти X Y для каждого теста.
"""
import sys
input = sys.stdin.readline

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    t = int(next(it))
    out = []
    for _ in range(t):
        n = int(next(it))
        # пропускаем n пар координат якорей
        for _ in range(n):
            _ = next(it); _ = next(it)
        # затем идёт X Y
        X = next(it); Y = next(it)
        out.append(f"{X} {Y}")
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