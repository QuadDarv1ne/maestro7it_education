'''
https://codeforces.com/contest/2136/problem/F1
'''

#!/usr/bin/env python3
"""
F1/F2. From the Unknown (хак-формат)

Хак-формат (как в условии):
t manual
W1
W2
...
Для каждого теста просто вывести W.
"""
import sys
input = sys.stdin.readline

def solve():
    first = input().split()
    if not first:
        return
    # Ожидаем: t [maybe 'manual']
    t = int(first[0])
    # если в той же строке есть слово manual, оно уже прочитано
    if len(first) > 1:
        # осталось ничего
        pass
    out = []
    for _ in range(t):
        line = input().strip()
        # иногда в разных вариациях ввод выглядит как пустая строка между тестами
        while line == "":
            line = input().strip()
        W = line.split()[0]
        out.append(W)
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