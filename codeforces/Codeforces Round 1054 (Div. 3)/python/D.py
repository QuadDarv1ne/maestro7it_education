'''
https://codeforces.com/contest/2149/problem/D
'''

import sys

def min_swaps_to_group(positions):
    """
    Для массива позиций (индексы символов одного типа), найти минимальное количество
    соседних перестановок, чтобы они стали подряд.
    Трансформация: пусть pos[i] — позиции, 0-based. Для блока длины m минимум равен
      sum |pos[i] - (start + i)|
    Минимизируется при выборе start = медиана(pos[i] - i).
    """
    m = len(positions)
    if m <= 1:
        return 0
    b = [positions[i] - i for i in range(m)]
    b.sort()
    med = b[m//2]
    res = sum(abs(x - med) for x in b)
    return res

def solve():
    """
    D. A and B

    Подсказка:
    - Рассчитать минимальные перестановки, чтобы все 'a' были в одном блоке,
      и отдельно — чтобы все 'b' были в одном блоке. Ответ — минимум из двух.
    - Вычисляем для каждой буквы список позиций и используем вышеописанную формулу.
    Сложность: O(n) на тест.
    """
    it = iter(sys.stdin.read().strip().split())
    t = int(next(it))
    out = []
    for _ in range(t):
        n = int(next(it))
        s = next(it).strip()
        pos_a = []
        pos_b = []
        for i, ch in enumerate(s):
            if ch == 'a':
                pos_a.append(i)
            else:
                pos_b.append(i)
        ans = min(min_swaps_to_group(pos_a), min_swaps_to_group(pos_b))
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