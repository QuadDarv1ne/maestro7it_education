'''
https://codeforces.com/contest/2132/problem/B

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
'''

def solve():
    """
    Решение задачи «The Secret Number». Для каждого числа n ищем все x такие, что
    при добавлении некоторого количества нулей к x получается y = x * 10^k,
    и n = x + y. Это означает n = x * (10^k + 1). Перебираем k от 1 до ~18,
    вычисляем div = 10^k + 1 и проверяем, делится ли n на div. Если делится,
    то x = n // div подходит. Собираем такие x в список, сортируем и выводим.
    """
    import sys
    input = sys.stdin.readline
    t = int(input())
    for _ in range(t):
        n = int(input())
        results = []
        power10 = 1
        # Перебираем k от 1 до 18 (10^18 примерно 1e18)
        for k in range(1, 19):
            power10 *= 10
            div = power10 + 1
            if div > n:
                break
            if n % div == 0:
                x = n // div
                if x > 0:
                    results.append(x)
        if not results:
            print(0)
        else:
            results.sort()
            print(len(results), *results)

if __name__ == "__main__":
    solve()
    
''' Полезные ссылки: '''
# 1. Telegram ❃Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks