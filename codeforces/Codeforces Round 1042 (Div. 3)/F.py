'''
https://codeforces.com/contest/2131/problem/F
'''

import sys
import bisect

input = sys.stdin.readline

"""
Задача F. Несправедливая бинарная жизнь

Вам даны две бинарные строки a и b длины n. Они динамически определяют сетку размером n × n. Пусть (i, j) — это ячейка в i-й строке и j-м столбце. Начальное значение ячейки (i, j) равно a_i ⊕ b_j, где ⊕ — это побитовая операция XOR.

Путешествие Юрия всегда начинается с ячейки (1, 1). Из ячейки (i, j) она может двигаться только вниз в (i + 1, j) или вправо в (i, j + 1). Её путешествие возможно, если существует допустимый путь, такой что все ячейки на пути, включая (1, 1), имеют значение 0.

До начала путешествия она может выполнить следующие операции любое количество раз:

    Выбрать индекс 1 ≤ i ≤ n и инвертировать значение либо a_i, либо b_i (0 становится 1, а 1 становится 0). Сетка также изменится соответственно.

Необходимо определить сумму минимальных операций, которые требуются для того, чтобы Юрий могла добраться до каждой ячейки (x, y) для всех 1 ≤ x, y ≤ n.

Входные данные:
- t — количество тестов.
Для каждого теста:
- n — длина строк.
- a, b — бинарные строки длины n.

Выходные данные:
Для каждого теста выведите одно число — искомую сумму.

Пример:

Вход:
3
2
11
00
2
01
01
4
1010
1101

Выход:
5
4
24
"""

t = int(input())

for _ in range(t):
    n = int(input())
    a = input().strip()
    b = input().strip()

    prefix_a_ones = [0] * (n + 1)
    prefix_b_ones = [0] * (n + 1)

    for i in range(1, n + 1):
        prefix_a_ones[i] = prefix_a_ones[i - 1] + (a[i - 1] == '1')
        prefix_b_ones[i] = prefix_b_ones[i - 1] + (b[i - 1] == '1')

    f = [0] * n
    for i in range(n):
        f[i] = 2 * prefix_b_ones[i + 1] - (i + 1)
    g = [-x for x in f]
    g.sort()

    prefix_g = [0]
    for x in g:
        prefix_g.append(prefix_g[-1] + x)

    S = 0
    for y in range(1, n + 1):
        S += y - prefix_b_ones[y]

    res = 0
    for x in range(1, n + 1):
        A0_x = x - prefix_a_ones[x]
        D_x = 2 * prefix_a_ones[x] - x
        pos = bisect.bisect_right(g, D_x)
        k = n - pos
        sum_g = prefix_g[-1] - prefix_g[pos]
        sum_min = -(sum_g - D_x * k)
        res += n * A0_x + S + sum_min

    print(res)

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks