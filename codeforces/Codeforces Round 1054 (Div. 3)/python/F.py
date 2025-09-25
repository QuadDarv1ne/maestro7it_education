'''
https://codeforces.com/contest/2149/problem/F
'''

import sys

def can_reach_in(T, h, d):
    """
    Проверка: за T ходов можно ли пройти расстояние d, начиная с здоровья h.
    Идея:
    - Симулируем максимально выгодную стратегию: выполняем максимально возможную последовательность шагов,
      затем, если нельзя двигаться — отдыхаем 1 ход, и т.д.
    - Для блока последовательных шагов вычисляем бинарным поиском максимальное m такое, что
        cost = m*consec + m*(m+1)//2 <= H-1
      (после m шагов здоровье >= 1).
    - Если m==0 — отдыхаем 1 ход (H += 1, consec = 0). Иначе выполняем k = min(m, оставшиеся шаги).
    Это даёт корректную и быструю проверку для бинарного поиска по общему числу ходов T.
    """
    t = T
    H = h
    consec = 0
    moved = 0
    while t > 0 and moved < d:
        # Find max m (<= t) such that cost <= H-1
        lo, hi = 1, t
        best = 0
        while lo <= hi:
            mid = (lo + hi) // 2
            cost = mid * consec + mid * (mid + 1) // 2
            if cost <= H - 1:
                best = mid
                lo = mid + 1
            else:
                hi = mid - 1
        m = best
        if m == 0:
            # can't move now -> rest 1 turn
            H += 1
            consec = 0
            t -= 1
        else:
            k = min(m, d - moved)
            costk = k * consec + k * (k + 1) // 2
            H -= costk
            moved += k
            consec += k
            t -= k
    return moved >= d

def solve():
    """
    F. Nezuko in the Clearing

    Бинарный поиск по минимальному числу ходов T: на каждой проверке используем can_reach_in.
    Сложность: O(log(MAX_T) * cost_check). cost_check выполняет не слишком много итераций,
    так как блоки движений группируются.
    """
    it = iter(sys.stdin.read().strip().split())
    t = int(next(it))
    out = []
    for _ in range(t):
        h = int(next(it)); d = int(next(it))
        lo, hi = 0, 2 * 10**9
        while lo < hi:
            mid = (lo + hi) // 2
            if can_reach_in(mid, h, d):
                hi = mid
            else:
                lo = mid + 1
        out.append(str(lo))
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