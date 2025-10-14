/*
 * ПОМОЩЬ ДЛЯ СТУДЕНТОВ В РЕШЕНИИ ЛАБОРАТОРНЫХ РАБОТ *
 * @file Файл: chess_moves.cpp
 *
 * @brief Лабораторная работа №5, Задача 2
 * Описание: Моделирование шахматной доски и возможных ходов фигур.
 *
 * Программа запрашивает у пользователя позицию фигуры в шахматной нотации (например, "e4")
 * и её тип: король, ферзь, слон, ладья, конь или пешка.
 * Выводит доску 8×8, где:
 *   '@' — текущая позиция фигуры,
 *   'X' — клетки, на которые фигура может пойти,
 *   '0' — остальные клетки.
 * 
 * Реализованы базовые ходы для белых фигур (пешка движется вверх).
 * Ввод проверяется на корректность.
 * 
 * @note Для компиляции: g++ -std=c++11 chess_moves.cpp -o chess_moves
 *       (работает даже без C++17!)
 * 
 * @author Автор: Дуплей Максим Игоревич
 * ORCID: https://orcid.org/0009-0007-7605-539X    
 * GitHub: https://github.com/QuadDarv1ne/    
*/

#include <iostream>
#include <string>
#include <vector>
#include <cctype>
#include <stdexcept>
#include <algorithm>
#include <locale>

#ifdef _WIN32
#include <windows.h>
#endif

using namespace std;

// Преобразует шахматную позицию (например, "e4") в индексы [строка][столбец]
pair<int, int> chessToIndex(const string& pos) {
    if (pos.size() != 2) {
        throw invalid_argument("Неверный формат позиции. Пример: e4");
    }
    char col = static_cast<char>(tolower(static_cast<unsigned char>(pos[0])));
    char row_char = pos[1];
    if (col < 'a' || col > 'h' || row_char < '1' || row_char > '8') {
        throw invalid_argument("Позиция вне пределов доски (a1–h8)");
    }
    int row = row_char - '1'; // '1' → 0, ..., '8' → 7
    return make_pair(7 - row, col - 'a'); // a1 → [7][0], h8 → [0][7]
}

// Выводит доску с текущей позицией фигуры
void printBoard(const vector<vector<char>>& board, int r, int c) {
    cout << "   a b c d e f g h\n";
    for (int i = 0; i < 8; ++i) {
        cout << (8 - i) << "  ";
        for (int j = 0; j < 8; ++j) {
            if (i == r && j == c) {
                cout << "@ ";
            } else {
                cout << board[i][j] << " ";
            }
        }
        cout << "\n";
    }
}

// Удаляет начальные и конечные пробелы
string trim(const string& str) {
    size_t start = str.find_first_not_of(" \t\r\n");
    size_t end = str.find_last_not_of(" \t\r\n");
    return (start == string::npos) ? "" : str.substr(start, end - start + 1);
}

int main() {
#ifdef _WIN32
    // Включаем поддержку UTF-8 в консоли Windows (требуется Windows 10+)
    SetConsoleOutputCP(CP_UTF8);
    SetConsoleCP(CP_UTF8);
#else
    setlocale(LC_ALL, "ru_RU.UTF-8");
#endif

    string input_line;
    string position, figure;

    cout << "Введите позицию фигуры (например, e4): ";
    getline(cin, input_line);
    position = trim(input_line);

    cout << "Введите тип фигуры (король, ферзь, слон, ладья, конь, пешка): ";
    getline(cin, input_line);
    figure = trim(input_line);

    if (position.empty() || figure.empty()) {
        cout << "Ошибка: введены пустые данные.\n";
        return 1;
    }

    // Приведение к нижнему регистру
    transform(figure.begin(), figure.end(), figure.begin(),
        [](unsigned char c) { return tolower(c); });

    try {
        pair<int, int> coords = chessToIndex(position);
        int r = coords.first;
        int c = coords.second;

        vector<vector<char>> board(8, vector<char>(8, '0'));

        if (figure == "король") {
            for (int dr = -1; dr <= 1; ++dr) {
                for (int dc = -1; dc <= 1; ++dc) {
                    if (dr == 0 && dc == 0) continue;
                    int nr = r + dr, nc = c + dc;
                    if (nr >= 0 && nr < 8 && nc >= 0 && nc < 8) {
                        board[nr][nc] = 'X';
                    }
                }
            }
        } else if (figure == "ферзь") {
            for (int i = 0; i < 8; ++i) {
                if (i != r) board[i][c] = 'X';
                if (i != c) board[r][i] = 'X';
            }
            for (int d = 1; d < 8; ++d) {
                if (r + d < 8 && c + d < 8) board[r+d][c+d] = 'X';
                if (r + d < 8 && c - d >= 0) board[r+d][c-d] = 'X';
                if (r - d >= 0 && c + d < 8) board[r-d][c+d] = 'X';
                if (r - d >= 0 && c - d >= 0) board[r-d][c-d] = 'X';
            }
        } else if (figure == "слон") {
            for (int d = 1; d < 8; ++d) {
                if (r + d < 8 && c + d < 8) board[r+d][c+d] = 'X';
                if (r + d < 8 && c - d >= 0) board[r+d][c-d] = 'X';
                if (r - d >= 0 && c + d < 8) board[r-d][c+d] = 'X';
                if (r - d >= 0 && c - d >= 0) board[r-d][c-d] = 'X';
            }
        } else if (figure == "ладья") {
            for (int i = 0; i < 8; ++i) {
                if (i != r) board[i][c] = 'X';
                if (i != c) board[r][i] = 'X';
            }
        } else if (figure == "конь") {
            const vector<pair<int,int>> moves = {{-2,-1}, {-2,1}, {-1,-2}, {-1,2},
                                                 {1,-2}, {1,2}, {2,-1}, {2,1}};
            for (const auto& move : moves) {
                int nr = r + move.first;
                int nc = c + move.second;
                if (nr >= 0 && nr < 8 && nc >= 0 && nc < 8) {
                    board[nr][nc] = 'X';
                }
            }
        } else if (figure == "пешка") {
            if (r > 0) board[r-1][c] = 'X';
            if (r == 6) board[r-2][c] = 'X';
        } else {
            cout << "Неизвестный тип фигуры. Допустимые: король, ферзь, слон, ладья, конь, пешка.\n";
            return 1;
        }

        cout << "\nШахматная доска:\n";
        printBoard(board, r, c);

    } catch (const exception& e) {
        cout << "Ошибка: " << e.what() << "\n";
        return 1;
    }

    return 0;
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