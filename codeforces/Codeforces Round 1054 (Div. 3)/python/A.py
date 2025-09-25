'''
https://codeforces.com/contest/2149/problem/A
'''

import sys

def solve():
    """
    A. Be Positive

    Задача: минимальное число операций (+1 к элементу) чтобы произведение всех элементов стало строго положительным.
    Замечания:
    - элементы принадлежат {-1,0,1}.
    - нужно убрать все нули (каждый ноль -> 1 требует 1 операцию).
    - после этого количество -1 должно быть чётным; если нечётно — нужно превратить один -1 в 1 (это стоит 2 операции: -1->0->1).
    Формула:
      ответ = (#zeros) + (negatives % 2) * 2
    Сложность: O(n) на тест.
    """
    it = iter(sys.stdin.read().strip().split())
    t = int(next(it))
    out = []
    for _ in range(t):
        n = int(next(it))
        neg = 0
        zeros = 0
        for _ in range(n):
            a = int(next(it))
            if a == 0:
                zeros += 1
            elif a == -1:
                neg += 1
        ans = zeros + (neg % 2) * 2
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