/*
 * LeetCode 79. Word Search
 * https://leetcode.com/problems/word-search/description/
 * 
 * Автор: Дуплей Максим Игоревич
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Полезные ссылки:
 * 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
 * 2. Telegram №1 @quadd4rv1n7
 * 3. Telegram №2 @dupley_maxim_1999
 * 4. Rutube канал: https://rutube.ru/channel/4218729/
 * 5. YouTube канал: https://www.youtube.com/@it-coders
 * 6. ВК группа: https://vk.com/science_geeks
 */

class Solution {
    public boolean exist(char[][] board, String word) {
        int m = board.length, n = board[0].length;
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (dfs(board, word, i, j, 0))
                    return true;
            }
        }
        return false;
    }
    
    private boolean dfs(char[][] board, String word, int i, int j, int idx) {
        if (idx == word.length()) return true;
        if (i < 0 || i >= board.length || j < 0 || j >= board[0].length || board[i][j] != word.charAt(idx))
            return false;
        
        char temp = board[i][j];
        board[i][j] = '#'; // Помечаем как посещённую
        
        boolean found = dfs(board, word, i + 1, j, idx + 1)
                     || dfs(board, word, i - 1, j, idx + 1)
                     || dfs(board, word, i, j + 1, idx + 1)
                     || dfs(board, word, i, j - 1, idx + 1);
        
        board[i][j] = temp; // Восстанавливаем
        return found;
    }
}