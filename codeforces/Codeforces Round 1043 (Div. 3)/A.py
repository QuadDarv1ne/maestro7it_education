'''
https://codeforces.com/contest/2132/problem/A
'''

def solve():
    """
    Решение задачи «Homework». Читаем количество тестов и для каждого теста:
    сначала читаем исходную строку `a`, строку символов `b` и строку распределения `c`.
    Мы должны по символам строки `b` (в данном порядке) добавлять каждый символ либо
    в начало результата (если соответствующий символ `c[i] == 'V'`), либо в конец (если 'D').
    Для этого ведём две строковые части: `prefix` и `suffix`. Если `c[i] == 'V'`, то добавляем `b[i]` в `prefix`;
    иначе — в `suffix`. В конце объединяем: результат = prefix + a + suffix и выводим его.
    """
    import sys
    input = sys.stdin.readline
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = input().strip()
        m = int(input())
        b = input().strip()
        c = input().strip()
        prefix = ""
        suffix = ""
        # Проходим по символам b и распределяем в начало или в конец
        for i in range(m):
            if c[i] == 'V':  # Влад добавляет в начало
                prefix = b[i] + prefix
            else:            # Dima добавляет в конец
                suffix = suffix + b[i]
        # Выводим итоговую строку
        print(prefix + a + suffix)
 
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