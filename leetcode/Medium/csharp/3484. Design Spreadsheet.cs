/**
 * https://leetcode.com/problems/design-spreadsheet/description/?envType=daily-question&envId=2025-09-19
 */

using System;

/// <summary>
/// Класс Spreadsheet — реализация упрощённой электронной таблицы.
/// 
/// Возможности:
/// - SetCell(cell, value): установить значение в указанную ячейку (например, "A1").
/// - ResetCell(cell): сбросить значение ячейки (установить 0).
/// - GetValue(formula): вычислить выражение вида "=X+Y", где X и Y —
///   либо ссылки на ячейки, либо числа.
/// 
/// Таблица имеет фиксированный размер: rows строк и 26 столбцов (A..Z).
/// </summary>
public class Spreadsheet {
    private int rows;
    private int[,] grid; // rows x 26

    public Spreadsheet(int rows) {
        this.rows = rows;
        grid = new int[rows, 26];
    }

    private (int r, int c) ParseCell(string cell) {
        int col = cell[0] - 'A';
        int row = Int32.Parse(cell.Substring(1)) - 1;
        return (row, col);
    }

    private int ValueFromToken(string tok) {
        if (!string.IsNullOrEmpty(tok) && char.IsUpper(tok[0])) {
            var rc = ParseCell(tok);
            return grid[rc.r, rc.c];
        } else {
            return Int32.Parse(tok);
        }
    }

    /// <summary> Установить значение в ячейку </summary>
    public void SetCell(string cell, int value) {
        var rc = ParseCell(cell);
        grid[rc.r, rc.c] = value;
    }

    /// <summary> Сбросить значение ячейки (0) </summary>
    public void ResetCell(string cell) {
        var rc = ParseCell(cell);
        grid[rc.r, rc.c] = 0;
    }

    /// <summary> Вычислить формулу "=X+Y" </summary>
    public int GetValue(string formula) {
        string expr = formula.Substring(1);
        int plus = expr.IndexOf('+');
        string a = expr.Substring(0, plus);
        string b = expr.Substring(plus + 1);
        return ValueFromToken(a) + ValueFromToken(b);
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