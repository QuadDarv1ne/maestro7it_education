'''
https://codeforces.com/contest/2139/problem/D

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
'''

def is_perfect_subarray(a, l, r):
    """
    Проверяет, является ли подмассив a[l..r] совершенным.

    :param a: Исходный массив.
    :param l: Левая граница подмассива (1-based).
    :param r: Правая граница подмассива (1-based).
    :return: "YES", если подмассив совершенный, иначе "NO".
    """
    odd = sorted(a[l-1:r:2])  # Элементы на нечётных позициях
    even = sorted(a[l:r:2])   # Элементы на чётных позициях

    # Восстанавливаем отсортированные элементы в подмассив
    b = a[:]
    b[l-1:r:2] = odd
    b[l:r:2] = even

    # Проверяем, отсортирован ли подмассив
    return "YES" if b[l-1:r] == sorted(b[l-1:r]) else "NO"

# Чтение входных данных и обработка запросов
t = int(input())  # Количество тестов
for _ in range(t):
    n, q = map(int, input().split())  # Длина массива и количество запросов
    a = list(map(int, input().split()))  # Массив a
    for _ in range(q):
        l, r = map(int, input().split())  # Запрос: подмассив a[l..r]
        print(is_perfect_subarray(a, l, r))

''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks