/**
 * https://leetcode.com/problems/n-queens-ii/description/
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "N-Queens II" на Java
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

import java.util.*;

class Solution {
    public int totalNQueens(int n) {
        Set<Integer> cols = new HashSet<>();
        Set<Integer> diagonals = new HashSet<>();
        Set<Integer> antiDiagonals = new HashSet<>();
        return backtrack(0, cols, diagonals, antiDiagonals, n);
    }
    
    private int backtrack(int row, Set<Integer> cols, Set<Integer> diagonals, 
                         Set<Integer> antiDiagonals, int n) {
        if (row == n) {
            return 1;
        }
        
        int count = 0;
        for (int col = 0; col < n; col++) {
            int currDiagonal = row - col;
            int currAntiDiagonal = row + col;
            
            if (cols.contains(col) || diagonals.contains(currDiagonal) || 
                antiDiagonals.contains(currAntiDiagonal)) {
                continue;
            }
            
            cols.add(col);
            diagonals.add(currDiagonal);
            antiDiagonals.add(currAntiDiagonal);
            
            count += backtrack(row + 1, cols, diagonals, antiDiagonals, n);
            
            cols.remove(col);
            diagonals.remove(currDiagonal);
            antiDiagonals.remove(currAntiDiagonal);
        }
        
        return count;
    }
}