/**
 * https://leetcode.com/problems/sudoku-solver/description/?envType=daily-question&envId=2025-08-31
 */

public class Solution {
    /// <summary>
    /// Решение задачи "Sudoku Solver" (LeetCode #37).
    /// 
    /// Метод: backtracking (поиск с возвратом).
    /// Для каждой пустой клетки '.' пробуем цифры 1–9.
    /// Проверяем строку, столбец и квадрат 3×3.
    /// При успешной подстановке продолжаем рекурсию.
    /// </summary>
    public void SolveSudoku(char[][] board) {
        Backtrack(board);
    }

    private bool Backtrack(char[][] board) {
        for (int i = 0; i < 9; i++) {
            for (int j = 0; j < 9; j++) {
                if (board[i][j] == '.') {
                    for (char ch = '1'; ch <= '9'; ch++) {
                        if (IsValid(board, i, j, ch)) {
                            board[i][j] = ch;
                            if (Backtrack(board)) return true;
                            board[i][j] = '.';
                        }
                    }
                    return false;
                }
            }
        }
        return true;
    }

    private bool IsValid(char[][] board, int r, int c, char ch) {
        for (int i = 0; i < 9; i++) {
            if (board[r][i] == ch || board[i][c] == ch) return false;
        }
        int br = (r / 3) * 3, bc = (c / 3) * 3;
        for (int i = br; i < br + 3; i++) {
            for (int j = bc; j < bc + 3; j++) {
                if (board[i][j] == ch) return false;
            }
        }
        return true;
    }
}

/*
''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
*/