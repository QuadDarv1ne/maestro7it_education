'''
https://codeforces.com/contest/2139/problem/E2

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
'''

def max_lcs(n, k, p):
    """
    Функция для вычисления максимальной длины общей подпоследовательности
    среди всех путей от корня до листьев дерева.

    :param n: Количество вершин в дереве.
    :param k: Количество нулей.
    :param p: Список родителей для вершин 2..n.
    :return: Максимальная длина общей подпоследовательности.
    """
    # Построение дерева
    tree = [[] for _ in range(n)]
    for i in range(1, n):
        tree[p[i-1]-1].append(i)
    
    # Поиск листьев
    leaves = []
    for i in range(n):
        if len(tree[i]) == 0:
            leaves.append(i)
    
    # Динамическое программирование
    dp = [[-1] * (k+1) for _ in range(n)]
    dp[0][0] = 0  # Начинаем с корня
    
    for i in range(1, n):
        for j in range(k+1):
            if dp[i-1][j] != -1:
                dp[i][j] = max(dp[i][j], dp[i-1][j] + 1)
    
    # Ответ
    return dp[n-1][k]

# Чтение входных данных
t = int(input())
for _ in range(t):
    n, k = map(int, input().split())
    p = list(map(int, input().split()))
    print(max_lcs(n, k, p))

''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks