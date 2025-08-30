/***
 * https://leetcode.com/problems/valid-sudoku/description/?envType=daily-question&envId=2025-08-30
 */

public class Solution {
    /// <summary>
    /// Проверяет, является ли Sudoku-доска (9x9) корректной.
    ///
    /// Условия:
    /// 1. В каждой строке цифры 1–9 встречаются не более одного раза.
    /// 2. В каждом столбце цифры 1–9 встречаются не более одного раза.
    /// 3. В каждом блоке 3x3 цифры 1–9 встречаются не более одного раза.
    /// Символ '.' обозначает пустую клетку и игнорируется.
    ///
    /// :param board: двумерный массив символов (9x9).
    /// :return: true, если доска корректна, иначе false.
    /// </summary>
    public bool IsValidSudoku(char[][] board) {
        bool[,] rows = new bool[9, 9];
        bool[,] cols = new bool[9, 9];
        bool[,] boxes = new bool[9, 9];
        
        for (int i = 0; i < 9; i++) {
            for (int j = 0; j < 9; j++) {
                char c = board[i][j];
                if (c == '.') continue;
                int num = c - '1';
                int boxIdx = (i / 3) * 3 + (j / 3);
                if (rows[i, num] || cols[j, num] || boxes[boxIdx, num]) {
                    return false;
                }
                rows[i, num] = cols[j, num] = boxes[boxIdx, num] = true;
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