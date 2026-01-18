class Solution:
    def largestMagicSquare(self, grid):
        """
        Находит размер наибольшего волшебного квадрата в матрице.
        
        Волшебный квадрат - это квадратная подматрица, в которой суммы чисел
        по всем строкам, столбцам и обеим диагоналям равны.
        
        Алгоритм:
        1. Используем префиксные суммы для быстрого вычисления сумм строк и столбцов
        2. Перебираем все возможные квадраты от большего к меньшему
        3. Для каждого квадрата проверяем условия волшебного квадрата
        
        Параметры:
        ----------
        grid : List[List[int]]
            Двумерный массив целых чисел
            
        Возвращает:
        -----------
        int
            Размер наибольшего волшебного квадрата
            
        Пример:
        -------
        >>> solution = Solution()
        >>> grid = [[7,1,4,5,6],
        ...         [2,5,1,6,4],
        ...         [1,5,4,3,2],
        ...         [1,2,7,3,4]]
        >>> solution.largestMagicSquare(grid)
        3
        
        Сложность:
        ----------
        Время: O(k * n * m), где k = min(n, m) - максимальный возможный размер квадрата
        Память: O(n * m) для хранения префиксных сумм
        
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
        
        rows = len(grid)
        cols = len(grid[0])
        
        # Префиксные суммы по строкам
        row_prefix = [[0] * (cols + 1) for _ in range(rows)]
        for i in range(rows):
            for j in range(cols):
                row_prefix[i][j + 1] = row_prefix[i][j] + grid[i][j]
        
        # Префиксные суммы по столбцам
        col_prefix = [[0] * (rows + 1) for _ in range(cols)]
        for j in range(cols):
            for i in range(rows):
                col_prefix[j][i + 1] = col_prefix[j][i] + grid[i][j]
        
        # Проверяем квадраты от максимального до минимального размера
        for size in range(min(rows, cols), 0, -1):
            for i in range(rows - size + 1):
                for j in range(cols - size + 1):
                    if self._isMagicSquare(grid, i, j, size, row_prefix, col_prefix):
                        return size
        
        return 1  # Минимальный волшебный квадрат 1×1
    
    def _isMagicSquare(self, grid, start_i, start_j, size, row_prefix, col_prefix):
        """
        Проверяет, является ли квадрат волшебным.
        
        Параметры:
        ----------
        grid : List[List[int]]
            Исходная матрица
        start_i : int
            Начальная строка квадрата
        start_j : int
            Начальный столбец квадрата
        size : int
            Размер квадрата
        row_prefix : List[List[int]]
            Префиксные суммы по строкам
        col_prefix : List[List[int]]
            Префиксные суммы по столбцам
            
        Возвращает:
        -----------
        bool
            True если квадрат волшебный, иначе False
        """
        
        target_sum = None
        
        # Проверяем суммы строк
        for i in range(start_i, start_i + size):
            row_sum = row_prefix[i][start_j + size] - row_prefix[i][start_j]
            if target_sum is None:
                target_sum = row_sum
            elif row_sum != target_sum:
                return False
        
        # Проверяем суммы столбцов
        for j in range(start_j, start_j + size):
            col_sum = col_prefix[j][start_i + size] - col_prefix[j][start_i]
            if col_sum != target_sum:
                return False
        
        # Проверяем главную диагональ
        diag1_sum = 0
        for k in range(size):
            diag1_sum += grid[start_i + k][start_j + k]
        if diag1_sum != target_sum:
            return False
        
        # Проверяем побочную диагональ
        diag2_sum = 0
        for k in range(size):
            diag2_sum += grid[start_i + k][start_j + size - 1 - k]
        return diag2_sum == target_sum