"""
Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Полезные ссылки:
1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
2. Telegram №1 @quadd4rv1n7
3. Telegram №2 @dupley_maxim_1999
4. Rutube канал: https://rutube.ru/channel/4218729/
5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
6. YouTube канал: https://www.youtube.com/@it-coders
7. ВК группа: https://vk.com/science_geeks
"""

class Solution:
    def minSwaps(self, grid):
        """
        Возвращает минимальное количество обменов соседних строк,
        чтобы все элементы выше главной диагонали стали нулями.
        Если это невозможно, возвращает -1.

        Алгоритм:
        1. Для каждой строки считаем количество нулей в её конце (trailing zeros).
        2. Идём по строкам сверху вниз (индекс i). Для строки i требуется,
           чтобы количество нулей в конце было не меньше n-1-i.
        3. Находим ближайшую снизу строку j (j >= i), удовлетворяющую требованию.
        4. Добавляем к ответу (j - i) — количество обменов, чтобы поднять строку j на позицию i.
        5. Сдвигаем все строки между i и j-1 вниз на одну позицию (имитируем swap).
        6. Если для какого-то i подходящая строка не найдена, возвращаем -1.
        """
        n = len(grid)
        # Вычисляем количество нулей в конце каждой строки
        trailing = []
        for i in range(n):
            cnt = 0
            for j in range(n - 1, -1, -1):
                if grid[i][j] == 0:
                    cnt += 1
                else:
                    break
            trailing.append(cnt)

        ans = 0
        for i in range(n):
            required = n - 1 - i
            # ищем строку с требуемым количеством нулей, начиная с i
            j = i
            while j < n and trailing[j] < required:
                j += 1
            if j == n:
                return -1
            # добавляем количество свопов
            ans += j - i
            # перемещаем найденную строку на позицию i (сдвигаем массив)
            val = trailing.pop(j)
            trailing.insert(i, val)
        return ans