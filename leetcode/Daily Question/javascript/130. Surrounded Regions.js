/**
 * @param {character[][]} board
 * @return {void} Do not return anything, modify board in-place instead.
 */
var solve = function(board) {
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
    
    if (!board || board.length === 0 || board[0].length === 0) {
        return;
    }
    
    const rows = board.length;
    const cols = board[0].length;
    
    const dfs = (r, c) => {
        if (r < 0 || r >= rows || c < 0 || c >= cols || board[r][c] !== 'O') {
            return;
        }
        
        // Помечаем как защищенный
        board[r][c] = 'T';
        
        // Рекурсивно проверяем соседей
        dfs(r + 1, c);
        dfs(r - 1, c);
        dfs(r, c + 1);
        dfs(r, c - 1);
    };
    
    // 1. Проверяем граничные строки
    for (let r = 0; r < rows; r++) {
        if (board[r][0] === 'O') {
            dfs(r, 0);
        }
        if (board[r][cols-1] === 'O') {
            dfs(r, cols-1);
        }
    }
    
    // 2. Проверяем граничные столбцы
    for (let c = 0; c < cols; c++) {
        if (board[0][c] === 'O') {
            dfs(0, c);
        }
        if (board[rows-1][c] === 'O') {
            dfs(rows-1, c);
        }
    }
    
    // 3. Преобразуем доску
    for (let r = 0; r < rows; r++) {
        for (let c = 0; c < cols; c++) {
            if (board[r][c] === 'O') {
                board[r][c] = 'X';  // Не защищенные
            } else if (board[r][c] === 'T') {
                board[r][c] = 'O';  // Защищенные
            }
        }
    }
};