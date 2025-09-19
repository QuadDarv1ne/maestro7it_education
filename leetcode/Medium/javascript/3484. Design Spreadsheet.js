/**
 * https://leetcode.com/problems/design-spreadsheet/description/?envType=daily-question&envId=2025-09-19
 */

/**
 * Класс Spreadsheet — упрощённая модель электронной таблицы.
 *
 * Методы:
 * - setCell(cell, value): устанавливает значение в указанной ячейке ("A1" и т.п.)
 * - resetCell(cell): сбрасывает значение ячейки (устанавливает 0)
 * - getValue(formula): вычисляет выражение вида "=X+Y", где X и Y —
 *   либо числа, либо ссылки на ячейки.
 *
 * Размер таблицы фиксирован: rows строк и 26 столбцов (A..Z).
 */
class Spreadsheet {
  constructor(rows) {
    this.rows = rows;
    this.grid = Array.from({length: rows}, () => Array(26).fill(0));
  }

  parseCell(cell) {
    const col = cell.charCodeAt(0) - 'A'.charCodeAt(0);
    const row = parseInt(cell.slice(1), 10) - 1;
    return [row, col];
  }

  valueFromToken(tok) {
    if (tok && tok[0] >= 'A' && tok[0] <= 'Z') {
      const [r, c] = this.parseCell(tok);
      return this.grid[r][c];
    } else {
      return parseInt(tok, 10);
    }
  }

  /** Установить значение в ячейку */
  setCell(cell, value) {
    const [r, c] = this.parseCell(cell);
    this.grid[r][c] = value;
  }

  /** Сбросить значение ячейки (0) */
  resetCell(cell) {
    const [r, c] = this.parseCell(cell);
    this.grid[r][c] = 0;
  }

  /** Вычислить значение формулы "=X+Y" */
  getValue(formula) {
    const expr = formula.slice(1);
    const parts = expr.split('+');
    return this.valueFromToken(parts[0]) + this.valueFromToken(parts[1]);
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