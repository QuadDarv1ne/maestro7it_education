/***
 * https://leetcode.com/problems/valid-sudoku/description/?envType=daily-question&envId=2025-08-30
 */

/**
 * Проверяет, является ли Sudoku-доска корректной.
 *
 * Условия:
 * 1. В каждой строке цифры 1–9 не должны повторяться.
 * 2. В каждом столбце цифры 1–9 не должны повторяться.
 * 3. В каждом квадрате 3x3 цифры 1–9 не должны повторяться.
 * Символ '.' считается пустой клеткой и игнорируется.
 *
 * @param {character[][]} board - массив 9x9
 * @return {boolean} true, если доска корректна, иначе false
 */
var isValidSudoku = function(board) {
    const rows = Array.from({ length: 9 }, () => new Array(9).fill(false));
    const cols = Array.from({ length: 9 }, () => new Array(9).fill(false));
    const boxes = Array.from({ length: 9 }, () => new Array(9).fill(false));
    
    for (let i = 0; i < 9; i++) {
        for (let j = 0; j < 9; j++) {
            const c = board[i][j];
            if (c === '.') continue;
            const num = c.charCodeAt(0) - '1'.charCodeAt(0);
            const boxIdx = Math.floor(i / 3) * 3 + Math.floor(j / 3);
            if (rows[i][num] || cols[j][num] || boxes[boxIdx][num]) {
                return false;
            }
            rows[i][num] = cols[j][num] = boxes[boxIdx][num] = true;
        }
    }
    return true;
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