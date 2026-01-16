class Solution:
    def solve(self, board):
        """
        Захватывает регионы, окруженные 'X', превращая 'O' в 'X'.
        
        Алгоритм:
        1. Находим все 'O' на границах доски
        2. С помощью DFS/BFS помечаем все связанные 'O' как защищенные
        3. Проходим по всей доске: непомеченные 'O' -> 'X', помеченные -> 'O'
        
        Сложность: O(m*n) время, O(m*n) память (для рекурсии/стека)
        
        Пример:
        Вход: [["X","X","X","X"],
               ["X","O","O","X"],
               ["X","X","O","X"],
               ["X","O","X","X"]]
        Выход: [["X","X","X","X"],
                ["X","X","X","X"],
                ["X","X","X","X"],
                ["X","O","X","X"]]
        
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
        
        if not board or not board[0]:
            return
        
        rows, cols = len(board), len(board[0])
        
        def dfs(r, c):
            """Помечает все связанные 'O' как защищенные."""
            if r < 0 or r >= rows or c < 0 or c >= cols or board[r][c] != 'O':
                return
            
            # Помечаем как защищенный
            board[r][c] = 'T'
            
            # Рекурсивно проверяем соседей
            dfs(r + 1, c)
            dfs(r - 1, c)
            dfs(r, c + 1)
            dfs(r, c - 1)
        
        # 1. Проверяем граничные строки (первая и последняя)
        for r in range(rows):
            if board[r][0] == 'O':
                dfs(r, 0)
            if board[r][cols-1] == 'O':
                dfs(r, cols-1)
        
        # 2. Проверяем граничные столбцы (первый и последний)
        for c in range(cols):
            if board[0][c] == 'O':
                dfs(0, c)
            if board[rows-1][c] == 'O':
                dfs(rows-1, c)
        
        # 3. Преобразуем доску
        for r in range(rows):
            for c in range(cols):
                if board[r][c] == 'O':
                    board[r][c] = 'X'  # Не защищенные 'O' -> 'X'
                elif board[r][c] == 'T':
                    board[r][c] = 'O'  # Защищенные -> 'O'