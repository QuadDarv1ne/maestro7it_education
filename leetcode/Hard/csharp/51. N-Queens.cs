/**
 * https://leetcode.com/problems/n-queens/description/
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "N-Queens" на C#
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

using System;
using System.Collections.Generic;

public class Solution {
    public IList<IList<string>> SolveNQueens(int n) {
        var result = new List<IList<string>>();
        var board = new char[n][];
        for (int i = 0; i < n; i++) {
            board[i] = new char[n];
            Array.Fill(board[i], '.');
        }
        
        var cols = new HashSet<int>();
        var diagonals = new HashSet<int>();
        var antiDiagonals = new HashSet<int>();
        
        Backtrack(0, cols, diagonals, antiDiagonals, board, result, n);
        return result;
    }
    
    private void Backtrack(int row, HashSet<int> cols, HashSet<int> diagonals, 
                          HashSet<int> antiDiagonals, char[][] board, 
                          List<IList<string>> result, int n) {
        if (row == n) {
            var solution = new List<string>();
            foreach (var r in board) {
                solution.Add(new string(r));
            }
            result.Add(solution);
            return;
        }
        
        for (int col = 0; col < n; col++) {
            int currDiagonal = row - col;
            int currAntiDiagonal = row + col;
            
            if (cols.Contains(col) || diagonals.Contains(currDiagonal) || 
                antiDiagonals.Contains(currAntiDiagonal)) {
                continue;
            }
            
            cols.Add(col);
            diagonals.Add(currDiagonal);
            antiDiagonals.Add(currAntiDiagonal);
            board[row][col] = 'Q';
            
            Backtrack(row + 1, cols, diagonals, antiDiagonals, board, result, n);
            
            cols.Remove(col);
            diagonals.Remove(currDiagonal);
            antiDiagonals.Remove(currAntiDiagonal);
            board[row][col] = '.';
        }
    }
}