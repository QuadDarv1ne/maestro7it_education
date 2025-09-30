'''
https://codeforces.com/contest/2139/problem/B

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
'''

import sys

def solve():
    """
    Решение задачи B. Сбор тортов (Codeforces 2139).

    Алгоритм:
    1. cur[i] — текущее количество тортов на печи i.
    2. На каждой секунде:
       - увеличиваем cur[i] += a[i] для всех печей,
       - выбираем печь с максимальным cur[i],
       - добавляем её торты к total и обнуляем cur[i].
    3. Повторяем m секунд.
    """
    input = sys.stdin.readline
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        a = list(map(int, input().split()))
        # Используем max-heap: (-текущие торты, производительность)
        heap = [(-val, val) for val in a]
        heapq.heapify(heap)
        total = 0
        for _ in range(m):
            neg_cur, prod = heapq.heappop(heap)
            cur = -neg_cur
            total += cur
            # После сбора печь производит новые торты
            heapq.heappush(heap, (-(cur + prod), prod))
        print(total)

# Запуск решения
solve()

''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks