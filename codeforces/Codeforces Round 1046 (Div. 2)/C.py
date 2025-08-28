'''
https://codeforces.com/contest/2136/problem/C
'''

#!/usr/bin/env python3
"""
C. Against the Difference

Находит длину наибольшей "neat" подпоследовательности.
DocString: читает t тестов; для каждого теста читает n и массив a.
Идея: для каждого значения v добавляем v * (cnt[v] // v) к ответу.
"""
import sys
from collections import Counter
input = sys.stdin.readline

def solve():
    t = int(input().strip())
    out = []
    for _ in range(t):
        n = int(input().strip())
        a = list(map(int, input().split()))
        cnt = Counter(a)
        ans = 0
        for v, c in cnt.items():
            ans += v * (c // v)
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