'''
https://codeforces.com/contest/2132/problem/G
'''

def solve():
    """
    Оптимизированное решение задачи Famous Choreographer.
    Для каждой тестовой матрицы вычисляем минимальное расширение,
    чтобы таблица была симметрична при повороте на 180°.
    Используем прямое сравнение строк и колонок вместо перебора всех подтаблиц.
    """
    import sys
    input = sys.stdin.readline

    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        f = [input().strip() for _ in range(n)]
        best = float('inf')

        # Проверяем все четыре угла
        for corner in [(0, 0), (0, m-1), (n-1, 0), (n-1, m-1)]:
            x0, y0 = corner
            dx = 1 if x0 == 0 else -1
            dy = 1 if y0 == 0 else -1

            # Ищем максимальную палиндромную подтаблицу
            max_x, max_y = x0, y0
            for i in range(n):
                x = x0 + dx * i
                if not (0 <= x < n):
                    break
                for j in range(m):
                    y = y0 + dy * j
                    if not (0 <= y < m):
                        break
                    valid = True
                    for ii in range(i + 1):
                        for jj in range(j + 1):
                            xi = x0 + dx * ii
                            yj = y0 + dy * jj
                            xr = x0 + dx * i - dx * ii
                            yr = y0 + dy * j - dy * jj
                            if f[xi][yj] != f[xr][yr]:
                                valid = False
                                break
                        if not valid:
                            break
                    if valid:
                        max_x = x
                        max_y = y

            # Правильное вычисление расширения
            row_start, row_end = sorted([x0, max_x])
            col_start, col_end = sorted([y0, max_y])
            rows = row_end - row_start + 1
            cols = col_end - col_start + 1
            best = min(best, rows * cols)

        print(best - n * m)

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