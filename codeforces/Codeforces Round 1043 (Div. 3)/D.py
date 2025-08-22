'''
https://codeforces.com/contest/2132/problem/D
'''

def solve():
    """
    Решение задачи «From 1 to Infinity». Для каждого k находим номер последнего числа n, 
    после которого обрезается последовательность конкатенации чисел 1,2,3...
    Сначала отнимаем блоки цифр: сначала 1..9 (9 чисел *1 цифра), затем 10..99 (90*2 цифры) и т.д.
    Как только k попадает в блок длины len, находим конкретное число s = cur/9 + (k-1)//len,
    и берем первые (k-1)%len+1 цифр этого числа в сумму. Остальное — сумма цифр всех чисел до s-1.
    Для суммы цифр до s-1 используем формулу: раскладываем s в цифры s[i], 
    и добавляем вклады по разрядам (см. код из редакции).
    """
    import sys
    input = sys.stdin.readline
    t = int(input())
    for _ in range(t):
        k = int(input())
        # Определяем длину чисел, в которой находится k-й символ
        cur = 9
        length = 1
        while k - cur * length > 0:
            k -= cur * length
            cur *= 10
            length += 1
        # Найдена длина length, текущий первый номер = cur/9, количество цифр смещения
        start = cur // 9  # это 10^(length-1)
        offset = (k - 1) // length
        n_str = str(start + offset)
        # Сумма цифр первых ((k-1)%length+1) цифр числа n
        take = (k - 1) % length + 1
        ans = sum(int(d) for d in n_str[:take])
        # Добавляем сумму цифр всех чисел до этого числа:
        # Формула по цифрам:
        pr_sum = 0
        cur_pow = cur  # cur = 9 * 10^(length-1)
        cur_len = length
        for ch in n_str:
            d = int(ch)
            if d:
                # сумма внесённая цифрой d на текущей позиции:
                ans += d * (cur_len - 1) * cur_pow // 2
                ans += d * (2 * pr_sum + d - 1) // 2 * (cur_pow // 9)
            pr_sum += d
            cur_pow //= 10
            cur_len -= 1
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