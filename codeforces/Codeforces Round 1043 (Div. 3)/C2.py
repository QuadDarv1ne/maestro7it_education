'''
https://codeforces.com/contest/2132/problem/C2

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
'''

def solve():
    """
    Решение сложной версии задачи «The Cunning Seller». Аналогично C1 находим троичные цифры n.
    Если минимальное число сделок min_k (сумма цифр) больше k, то вывести -1.
    Иначе используем «свободные» сделки: extra = (k - min_k) // 2. Идем с самой старшей цифры вниз:
    если tr[i] <= extra, то мы можем «расщепить» все tr[i] сделок на уровень i-1: tr[i-1]+=3*tr[i], tr[i]=0, extra-=tr[i].
    Иначе - делаем частичное расщепление: tr[i-1]+=extra*3, tr[i]-=extra, break.
    Затем снова вычисляем стоимость по формуле (аналогично C1).
    """
    import sys
    input = sys.stdin.readline
    t = int(input())
    pow3 = [1]
    for _ in range(60):
        pow3.append(pow3[-1] * 3)
    # Предвычислим стоимость сделок для индексов (до необходимого, скажем до 60)
    cost_table = [0]*61
    cost_table[0] = 3
    for i in range(1, 61):
        cost_table[i] = pow3[i+1] + i * pow3[i-1]
    for _ in range(t):
        n,k = map(int, input().split())
        tr = []
        x = n
        while x > 0:
            tr.append(x % 3)
            x //= 3
        min_k = sum(tr)
        if min_k > k:
            print(-1)
            continue
        # Используем свободные сделки
        extra = (k - min_k) // 2
        # Расщепляем с самых больших степеней вниз
        for i in range(len(tr)-1, 0, -1):
            if tr[i] == 0:
                continue
            if tr[i] <= extra:
                # полностью переносим
                tr[i-1] += 3 * tr[i]
                extra -= tr[i]
                tr[i] = 0
            else:
                # частично переносим
                tr[i-1] += extra * 3
                tr[i] -= extra
                extra = 0
                break
        # Считаем стоимость
        ans = 0
        for i, d in enumerate(tr):
            if d:
                ans += d * cost_table[i]
        print(ans)

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