/**
 * https://leetcode.com/problems/n-queens-ii/description/
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "N-Queens II" на JavaScript
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

var totalNQueens = function(n) {
    function backtrack(row, cols, diagonals, antiDiagonals) {
        if (row === n) {
            return 1;
        }
        
        let count = 0;
        for (let col = 0; col < n; col++) {
            const currDiagonal = row - col;
            const currAntiDiagonal = row + col;
            
            if (cols.has(col) || diagonals.has(currDiagonal) || antiDiagonals.has(currAntiDiagonal)) {
                continue;
            }
            
            cols.add(col);
            diagonals.add(currDiagonal);
            antiDiagonals.add(currAntiDiagonal);
            
            count += backtrack(row + 1, cols, diagonals, antiDiagonals);
            
            cols.delete(col);
            diagonals.delete(currDiagonal);
            antiDiagonals.delete(currAntiDiagonal);
        }
        
        return count;
    }
    
    return backtrack(0, new Set(), new Set(), new Set());
};