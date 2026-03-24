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

Строит матрицу произведений, где каждый элемент p[i][j] равен произведению
всех элементов исходной матрицы, кроме grid[i][j], по модулю 12345.

Параметры:
    grid (List[List[int]]): исходная матрица целых чисел размером n x m

Возвращает:
    List[List[int]]: матрицу произведений по модулю 12345

Примечания:
    - Модуль 12345 = 3 * 5 * 823 (составное число)
    - Нельзя использовать деление или обратные элементы
    - Используется метод префиксных и суффиксных произведений
    - Сложность: O(n*m) по времени и O(n*m) по памяти

Пример:
    >>> grid = [[1,2],[3,4]]
    >>> constructProductMatrix(grid)
    [[24,12],[8,6]]
"""

class Solution(object):
    def constructProductMatrix(self, grid):
        MOD = 12345
        n, m = len(grid), len(grid[0])
        total = n * m
        
        # Преобразуем 2D матрицу в 1D массив для удобства
        arr = [0] * total
        for i in range(n):
            for j in range(m):
                arr[i * m + j] = grid[i][j] % MOD
        
        # Префиксные произведения
        prefix = [1] * total
        for i in range(1, total):
            prefix[i] = (prefix[i - 1] * arr[i - 1]) % MOD
        
        # Суффиксные произведения
        suffix = [1] * total
        for i in range(total - 2, -1, -1):
            suffix[i] = (suffix[i + 1] * arr[i + 1]) % MOD
        
        # Результат для каждого элемента
        result = [[0] * m for _ in range(n)]
        for i in range(total):
            row, col = divmod(i, m)
            result[row][col] = (prefix[i] * suffix[i]) % MOD
        
        return result