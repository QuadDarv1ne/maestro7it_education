'''
https://codeforces.com/contest/2144/problem/B
'''

def solve():
    """
    Решение задачи B: Maximum Cost Permutation
    
    Задача:
    При вычислении стоимости перестановки разрешается сортировать только один
    непрерывный подсегмент (а не несколько). Требуется определить максимальную
    возможную стоимость перестановки после применения одной операции сортировки
    непрерывного подсегмента.
    
    Входные данные:
    - Первая строка: количество тестовых случаев t
    - Для каждого теста:
        * Первая строка: целое число n (длина перестановки)
        * Вторая строка: n целых чисел (перестановка)
    
    Выходные данные:
    - Для каждого теста выводит одно целое число - максимальную стоимость перестановки.
    
    Примечание: Полное условие задачи содержит дополнительные детали,
    которые необходимо учитывать при реализации решения.
    """
    n = int(input().strip())
    p = list(map(int, input().split()))
    
    # Инициализируем массивы для динамического программирования
    dp = [0] * (n + 1)
    prefix_max = [0] * (n + 1)
    
    # Заполняем dp и prefix_max
    for i in range(1, n + 1):
        # dp[i] = максимальная стоимость для префикса длины i
        dp[i] = dp[i-1] + (1 if p[i-1] == i else 0)
        prefix_max[i] = max(prefix_max[i-1], dp[i])
    
    # Ищем максимальную стоимость после применения одной операции сортировки
    max_cost = 0
    for l in range(1, n + 1):
        for r in range(l, n + 1):
            # Считаем стоимость после сортировки подсегмента [l, r]
            cost = prefix_max[l-1]  # стоимость до l
            
            # Сортируем подсегмент и считаем стоимость
            segment = p[l-1:r]
            segment.sort()
            for i in range(l, r + 1):
                if segment[i-l] == i:
                    cost += 1
            
            cost += dp[n] - dp[r]  # стоимость после r
            max_cost = max(max_cost, cost)
    
    print(max_cost)

t = int(input().strip())
for _ in range(t):
    solve()

''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks