'''
https://codeforces.com/contest/2132/problem/C1
'''

def solve():
    """
    Решение лёгкой версии задачи «The Cunning Seller». Для покупки n арбузов нужно минимальное
    число сделок. Сделки дают арбузы 3^i за стоимость (3^(i+1) + i*3^(i-1)). 
    Чтобы минимизировать число сделок, представляем n в троичной системе (каждая цифра d_i дает d_i сделок по 3^i).
    Число сделок = сумма цифр троичного представления n.
    Стоимость = сумма по i: d_i * cost_i. Для i=0 cost=3, иначе cost = 3^(i+1) + i*3^(i-1).
    """
    import sys
    input = sys.stdin.readline
    t = int(input())
    for _ in range(t):
        n = int(input())
        # Получаем цифры n в троичной системе (младшие вперед)
        tr = []
        x = n
        while x > 0:
            tr.append(x % 3)
            x //= 3
        # Вычисляем стоимость
        cost = 0
        pow3 = [1]  # предварительно 3^i
        for i in range(1, len(tr)+2):
            pow3.append(pow3[-1] * 3)
        for i, d in enumerate(tr):
            if d == 0:
                continue
            if i == 0:
                cost_i = 3
            else:
                # 3^(i+1) + i*3^(i-1)
                cost_i = pow3[i+1] + i * pow3[i-1]
            cost += d * cost_i
        print(cost)

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