/**
 * https://leetcode.com/problems/sudoku-solver/description/?envType=daily-question&envId=2025-08-31
 */

/**
 * Решение задачи "Sudoku Solver" (LeetCode #37).
 *
 * Метод: backtracking (поиск с возвратом).
 * Пустые клетки ('.') последовательно заполняются цифрами 1–9.
 * Проверяется строка, столбец и блок 3×3.
 * При успехе идем дальше, при ошибке — откатываемся.
 */
var solveSudoku = function(board) {
    function isValid(r, c, ch) {
        for (let i = 0; i < 9; i++) {
            if (board[r][i] === ch || board[i][c] === ch) return false;
        }
        let br = Math.floor(r / 3) * 3, bc = Math.floor(c / 3) * 3;
        for (let i = br; i < br + 3; i++) {
            for (let j = bc; j < bc + 3; j++) {
                if (board[i][j] === ch) return false;
            }
        }
        return true;
    }

    function backtrack() {
        for (let i = 0; i < 9; i++) {
            for (let j = 0; j < 9; j++) {
                if (board[i][j] === ".") {
                    for (let d = 1; d <= 9; d++) {
                        let ch = d.toString();
                        if (isValid(i, j, ch)) {
                            board[i][j] = ch;
                            if (backtrack()) return true;
                            board[i][j] = ".";
                        }
                    }
                    return false;
                }
            }
        }
        return true;
    }

    backtrack();
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