/**
 * https://leetcode.com/problems/design-spreadsheet/description/?envType=daily-question&envId=2025-09-19
 */

#include <string>
#include <vector>
#include <cctype>
using namespace std;

/**
 * Класс Spreadsheet — простая реализация электронной таблицы.
 *
 * Возможности:
 * - setCell(cell, value): установить значение в ячейку (например, "A1" = 5)
 * - resetCell(cell): сбросить значение ячейки (установить 0)
 * - getValue(formula): вычислить выражение вида "=X+Y", где X и Y —
 *   либо ссылки на ячейки, либо целые числа.
 *
 * Размер таблицы фиксируется при создании (rows x 26, столбцы A..Z).
 */
class Spreadsheet {
private:
    int rows;
    vector<vector<int>> grid; // rows x 26

    pair<int,int> parseCell(const string &cell) {
        int col = cell[0] - 'A';
        int row = stoi(cell.substr(1)) - 1; // строки 1-индексированы
        return {row, col};
    }

    int valueFromToken(const string &tok) {
        if (!tok.empty() && isupper(tok[0])) {
            auto [r, c] = parseCell(tok);
            return grid[r][c];
        } else {
            return stoi(tok);
        }
    }

public:
    Spreadsheet(int rows): rows(rows), grid(rows, vector<int>(26, 0)) {}

    /// Установить значение в ячейку
    void setCell(string cell, int value) {
        auto [r, c] = parseCell(cell);
        grid[r][c] = value;
    }

    /// Сбросить ячейку (установить 0)
    void resetCell(string cell) {
        auto [r, c] = parseCell(cell);
        grid[r][c] = 0;
    }

    /// Получить значение формулы вида "=X+Y"
    int getValue(string formula) {
        string expr = formula.substr(1);
        size_t plusPos = expr.find('+');
        string a = expr.substr(0, plusPos);
        string b = expr.substr(plusPos + 1);
        return valueFromToken(a) + valueFromToken(b);
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