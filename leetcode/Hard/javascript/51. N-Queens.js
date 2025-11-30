/**
 * https://leetcode.com/problems/n-queens/description/
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "N-Queens" на JavaScript
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

var solveNQueens = function(n) {
    const result = [];
    const board = Array.from({length: n}, () => Array(n).fill('.'));
    const cols = new Set();
    const diagonals = new Set();
    const antiDiagonals = new Set();
    
    function backtrack(row) {
        if (row === n) {
            result.push(board.map(row => row.join('')));
            return;
        }
        
        for (let col = 0; col < n; col++) {
            const currDiagonal = row - col;
            const currAntiDiagonal = row + col;
            
            if (cols.has(col) || diagonals.has(currDiagonal) || antiDiagonals.has(currAntiDiagonal)) {
                continue;
            }
            
            cols.add(col);
            diagonals.add(currDiagonal);
            antiDiagonals.add(currAntiDiagonal);
            board[row][col] = 'Q';
            
            backtrack(row + 1);
            
            cols.delete(col);
            diagonals.delete(currDiagonal);
            antiDiagonals.delete(currAntiDiagonal);
            board[row][col] = '.';
        }
    }
    
    backtrack(0);
    return result;
};