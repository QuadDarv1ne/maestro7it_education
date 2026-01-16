class Solution {
    public void solve(char[][] board) {
        /**
         * Захватывает регионы, окруженные 'X', превращая 'O' в 'X'.
         * 
         * Алгоритм:
         * 1. Находим 'O' на границах и помечаем все связанные 'O'
         * 2. Преобразуем непомеченные 'O' в 'X'
         * 3. Восстанавливаем помеченные 'O'
         * 
         * Автор: Дуплей Максим Игоревич - AGLA
         * ORCID: https://orcid.org/0009-0007-7605-539X
         * GitHub: https://github.com/QuadDarv1ne/
         * 
         * Полезные ссылки:
         * 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
         * 2. Telegram №1 @quadd4rv1n7
         * 3. Telegram №2 @dupley_maxim_1999
         * 4. Rutube канал: https://rutube.ru/channel/4218729/
         * 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
         * 6. YouTube канал: https://www.youtube.com/@it-coders
         * 7. ВК группа: https://vk.com/science_geeks
         */
        
        if (board == null || board.length == 0 || board[0].length == 0) {
            return;
        }
        
        int rows = board.length;
        int cols = board[0].length;
        
        // 1. Проверяем граничные строки
        for (int r = 0; r < rows; r++) {
            if (board[r][0] == 'O') {
                dfs(board, r, 0);
            }
            if (board[r][cols-1] == 'O') {
                dfs(board, r, cols-1);
            }
        }
        
        // 2. Проверяем граничные столбцы
        for (int c = 0; c < cols; c++) {
            if (board[0][c] == 'O') {
                dfs(board, 0, c);
            }
            if (board[rows-1][c] == 'O') {
                dfs(board, rows-1, c);
            }
        }
        
        // 3. Преобразуем доску
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                if (board[r][c] == 'O') {
                    board[r][c] = 'X';  // Не защищенные
                } else if (board[r][c] == 'T') {
                    board[r][c] = 'O';  // Защищенные
                }
            }
        }
    }
    
    private void dfs(char[][] board, int r, int c) {
        if (r < 0 || r >= board.length || c < 0 || c >= board[0].length || board[r][c] != 'O') {
            return;
        }
        
        // Помечаем как защищенный
        board[r][c] = 'T';
        
        // Рекурсивно проверяем соседей
        dfs(board, r + 1, c);
        dfs(board, r - 1, c);
        dfs(board, r, c + 1);
        dfs(board, r, c - 1);
    }
}