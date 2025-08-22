'''
https://codeforces.com/contest/2132/problem/E
'''

def solve():
    """
    Решение задачи «Arithmetics Competition». Сортируем массивы a и b в невозрастающем порядке
    и строим префиксные суммы pa и pb. Далее предвычисляем для каждого z до n+m оптимальное 
    распределение количества взятых карт из a и b (ans[z] = (l, r), где l+r=z).
    Для этого мы «собираем» наибольшие карты двумя указателями. Затем для каждого запроса (x,y,z)
    проверяем ans[z]. Если ans[z].l > x (то больше карт требует взял Vadim, чем он может),
    делаем корректировку: берём x из a и z-x из b. Аналогично для ans[z].r > y.
    Иначе отвечаем pa[l] + pb[r].
    """
    import sys
    input = sys.stdin.readline
    t = int(input())
    for _ in range(t):
        n,m,q = map(int, input().split())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))
        a.sort(reverse=True)
        b.sort(reverse=True)
        # Префиксные суммы
        pa = [0]*(n+1)
        pb = [0]*(m+1)
        for i in range(n):
            pa[i+1] = pa[i] + a[i]
        for i in range(m):
            pb[i+1] = pb[i] + b[i]
        # Предвычисляем распределение l,r для суммарных размеров
        max_count = n + m
        ans_lr = [(0,0)]*(max_count+1)
        l = r = 0
        ans_lr = [(0,0)]*(max_count+1)
        ans_lr[0] = (0,0)
        for i in range(1, max_count+1):
            if l < n and r < m:
                # добавляем больший элемент
                if a[l] >= b[r]:
                    l += 1
                else:
                    r += 1
            elif l < n:
                l += 1
            else:
                r += 1
            ans_lr[i] = (l, r)
        # Обрабатываем запросы
        for _ in range(q):
            x,y,z = map(int, input().split())
            l,z_l = ans_lr[z]
            r = z - l
            # Проверяем ограничения x и y
            if l > x:
                # берём x из a, остальные из b
                res = pa[x] + pb[z-x]
            elif r > y:
                # берём y из b, остальные из a
                res = pa[z-y] + pb[y]
            else:
                res = pa[l] + pb[r]
            print(res)

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