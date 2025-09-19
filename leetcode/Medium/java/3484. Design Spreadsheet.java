/**
 * https://leetcode.com/problems/design-spreadsheet/description/?envType=daily-question&envId=2025-09-19
 */

// Java 11+
import java.util.*;

/**
 * Класс Spreadsheet — реализация простой электронной таблицы.
 *
 * Функционал:
 * - setCell(cell, value): задать значение ячейки (например, "B2" = 10)
 * - resetCell(cell): обнулить указанную ячейку
 * - getValue(formula): вычислить формулу в формате "=X+Y", где X и Y —
 *   либо ссылки на ячейки, либо числа.
 *
 * Размер таблицы задаётся при создании, колонки фиксированы (A..Z).
 */
public class Spreadsheet {
    private int rows;
    private int[][] grid; // rows x 26

    public Spreadsheet(int rows) {
        this.rows = rows;
        this.grid = new int[rows][26];
    }

    private int[] parseCell(String cell) {
        int col = cell.charAt(0) - 'A';
        int row = Integer.parseInt(cell.substring(1)) - 1;
        return new int[]{row, col};
    }

    private int valueFromToken(String tok) {
        if (!tok.isEmpty() && Character.isUpperCase(tok.charAt(0))) {
            int[] rc = parseCell(tok);
            return grid[rc[0]][rc[1]];
        } else {
            return Integer.parseInt(tok);
        }
    }

    /** Установить значение в ячейку */
    public void setCell(String cell, int value) {
        int[] rc = parseCell(cell);
        grid[rc[0]][rc[1]] = value;
    }

    /** Сбросить значение ячейки (0) */
    public void resetCell(String cell) {
        int[] rc = parseCell(cell);
        grid[rc[0]][rc[1]] = 0;
    }

    /** Вычислить значение формулы вида "=X+Y" */
    public int getValue(String formula) {
        String expr = formula.substring(1);
        int plus = expr.indexOf('+');
        String a = expr.substring(0, plus);
        String b = expr.substring(plus + 1);
        return valueFromToken(a) + valueFromToken(b);
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