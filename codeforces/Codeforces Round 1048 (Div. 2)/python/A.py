'''
https://codeforces.com/contest/2139/problem/A

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
'''

def solve():
    """
    Решение задачи A. Мейпл и Умножение (Codeforces 2139).
    
    Функция читает t тестов. Для каждого теста:
    - Вводит два числа a и b.
    - Выводит минимальное количество операций, чтобы a стало равно b.
    
    Алгоритм:
    1. Если a == b, операций не требуется → 0
    2. Если одно число делится на другое → 1 операция
    3. Иначе → 2 операции
    """
    import sys
    input = sys.stdin.readline

    t = int(input())
    for _ in range(t):
        a, b = map(int, input().split())
        if a == b:
            print(0)
        elif a % b == 0 or b % a == 0:
            print(1)
        else:
            print(2)

''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks