/**
 * https://leetcode.com/problems/sudoku-solver/description/?envType=daily-question&envId=2025-08-31
 */

#include <bits/stdc++.h>
using namespace std;

bool row_used[9][10], col_used[9][10], box_used[9][10];

bool dfs(vector<vector<char>>& board, int r, int c) {
    if (r == 9) return true;
    int nr = (c == 8 ? r + 1 : r);
    int nc = (c + 1) % 9;
    if (board[r][c] != '.') return dfs(board, nr, nc);
    for (int d = 1; d <= 9; d++) {
        int b = (r / 3) * 3 + (c / 3);
        if (!row_used[r][d] && !col_used[c][d] && !box_used[b][d]) {
            board[r][c] = char('0' + d);
            row_used[r][d] = col_used[c][d] = box_used[b][d] = true;
            if (dfs(board, nr, nc)) return true;
            board[r][c] = '.';
            row_used[r][d] = col_used[c][d] = box_used[b][d] = false;
        }
    }
    return false;
}

class Solution {
public:
    /**
     * Решение задачи "Sudoku Solver" (LeetCode #37).
     *
     * Алгоритм:
     * Используется метод поиска с возвратом (backtracking).
     * Для каждой пустой клетки пробуем цифры от 1 до 9.
     * Проверка допустимости выполняется через вспомогательные массивы:
     *   - row_used[i][d] — цифра d уже есть в строке i
     *   - col_used[j][d] — цифра d уже есть в столбце j
     *   - box_used[b][d] — цифра d уже есть в блоке b (3×3)
     *
     * При успешной подстановке продолжаем рекурсию.
     * Если решение найдено — возвращаем true, иначе откатываем шаг.
     *
     * Параметры:
     *   board — доска 9×9 ('.' означает пустую клетку).
     *
     * Возвращает:
     *   void (решение модифицирует board на месте).
     */
    void solveSudoku(vector<vector<char>>& board) {
        memset(row_used, 0, sizeof(row_used));
        memset(col_used, 0, sizeof(col_used));
        memset(box_used, 0, sizeof(box_used));
        for (int i = 0; i < 9; i++) {
            for (int j = 0; j < 9; j++) {
                if (board[i][j] != '.') {
                    int d = board[i][j] - '0';
                    row_used[i][d] = col_used[j][d] = box_used[(i/3)*3 + (j/3)][d] = true;
                }
            }
        }
        dfs(board, 0, 0);
    }
};

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