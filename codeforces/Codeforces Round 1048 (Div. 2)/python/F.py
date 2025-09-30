'''
https://codeforces.com/contest/2139/problem/F

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
'''

MOD = 10**9 + 7

def process_operations(n, m, q, a, operations):
    """
    Функция для обработки операций перемещения ползунков и вычисления
    суммы позиций каждого ползунка по всем возможным перестановкам операций.

    :param n: Количество ползунков.
    :param m: Длина дорожки.
    :param q: Количество операций.
    :param a: Список начальных позиций ползунков.
    :param operations: Список операций, каждая из которых является
                       кортежем (i, x), где i — индекс ползунка,
                       x — целевая позиция.
    :return: Список сумм позиций каждого ползунка по всем возможным
             перестановкам операций, взятых по модулю MOD.
    """
    # Инициализация списка позиций ползунков
    positions = a[:]
    
    # Обработка операций
    for op in operations:
        i, x = op
        i -= 1  # Преобразуем индекс в 0-based
        # Перемещаем ползунок i в позицию x, с учётом возможных сдвигов
        while positions[i] != x:
            if positions[i] < x:
                positions[i] += 1
            else:
                positions[i] -= 1
    
    # Вычисление суммы позиций
    total_sum = sum(positions) % MOD
    return [total_sum] * n

# Чтение входных данных
t = int(input())
for _ in range(t):
    n, m, q = map(int, input().split())
    a = list(map(int, input().split()))
    operations = [tuple(map(int, input().split())) for _ in range(q)]
    result = process_operations(n, m, q, a, operations)
    print(*result)

''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks