/**
 * @file sudoku_1.cpp
 * @brief Реализация консольной игры "Судоку" для курса «C++ и C# разработка» — Maestro7IT.
 *
 * Программа генерирует валидную головоломку судоку заданной сложности,
 * позволяет пользователю вводить числа, проверяет корректность ходов
 * и отображает итоговую статистику (ходы, ошибки).
 *
 * @note Требуется компилятор с поддержкой C++17.
 * @see https://school-maestro7it.ru/
 * @author Дуплей М.И. — Maestro7IT
 *
 * Компиляция: g++ -std=c++17 -O2 -Wall -Wextra -o sudoku sudoku_1.cpp
 * Запуск: ./sudoku
 */

#include <iostream>
#include <vector>
#include <random>
#include <algorithm>
#include <limits>
#include <array>

#ifdef _WIN32
    #include <windows.h>
    void clearScreen() { system("cls"); }
#else
    void clearScreen() { std::cout << "\033[2J\033[H"; }
#endif

/**
 * @class Sudoku
 * @brief Класс, реализующий логику игры Судоку.
 */
class Sudoku {
private:
    static constexpr int N = 9;
    static constexpr int EMPTY = 0;

    std::vector<std::vector<int>> board;      ///< Текущее состояние доски
    std::vector<std::vector<int>> solution;   ///< Полное решение

    void fillBaseSolution();
    void shuffle();
    bool isValidMove(int row, int col, int num) const;

public:
    explicit Sudoku(int difficulty = 40);
    void printBoard() const;
    bool makeMove(int row, int col, int num);
    [[nodiscard]] bool isSolved() const;
    [[nodiscard]] int countEmptyCells() const;
};

void Sudoku::fillBaseSolution() {
    for (int i = 0; i < N; ++i)
        for (int j = 0; j < N; ++j)
            solution[i][j] = (i * 3 + i / 3 + j) % N + 1;
}

void Sudoku::shuffle() {
    std::random_device rd;
    std::mt19937 g(rd());

    for (int band = 0; band < 3; ++band) {
        std::array<int, 3> rows = {band * 3, band * 3 + 1, band * 3 + 2};
        std::shuffle(rows.begin(), rows.end(), g);
        auto temp = solution;
        for (int i = 0; i < 3; ++i)
            solution[band * 3 + i] = std::move(temp[rows[i]]);
    }

    for (int stack = 0; stack < 3; ++stack) {
        std::array<int, 3> cols = {stack * 3, stack * 3 + 1, stack * 3 + 2};
        std::shuffle(cols.begin(), cols.end(), g);
        for (auto& row : solution) {
            auto temp_row = row;
            for (int j = 0; j < 3; ++j)
                row[stack * 3 + j] = temp_row[cols[j]];
        }
    }
}

bool Sudoku::isValidMove(int row, int col, int num) const {
    return solution[row][col] == num;
}

Sudoku::Sudoku(int difficulty)
    : board(N, std::vector<int>(N, EMPTY)),
      solution(N, std::vector<int>(N, EMPTY)) {
    fillBaseSolution();
    shuffle();
    board = solution;

    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dis(0, N * N - 1);

    int removed = 0;
    int attempts = 0;
    const int maxAttempts = difficulty * 3;

    while (removed < difficulty && attempts < maxAttempts) {
        int pos = dis(gen);
        int row = pos / N;
        int col = pos % N;
        if (board[row][col] != EMPTY) {
            board[row][col] = EMPTY;
            ++removed;
        }
        ++attempts;
    }
}

void Sudoku::printBoard() const {
    std::cout << "+-------+-------+-------+\n";
    for (int i = 0; i < N; ++i) {
        std::cout << "| ";
        for (int j = 0; j < N; ++j) {
            char ch = (board[i][j] == EMPTY) ? '.' : '0' + board[i][j];
            std::cout << ch << ' ';
            if (j % 3 == 2) std::cout << "| ";
        }
        std::cout << '\n';
        if (i % 3 == 2)
            std::cout << "+-------+-------+-------+\n";
    }
}

bool Sudoku::makeMove(int row, int col, int num) {
    if (row < 0 || row >= N || col < 0 || col >= N || num < 1 || num > N) {
        std::cout << "[Ошибка] Некорректные координаты или число (должно быть 1–9).\n";
        return false;
    }
    if (board[row][col] != EMPTY) {
        std::cout << "[Внимание] Клетка уже заполнена.\n";
        return false;
    }
    if (!isValidMove(row, col, num)) {
        std::cout << "[Ошибка] Неверное число для этой клетки.\n";
        return false;
    }
    board[row][col] = num;
    return true;
}

bool Sudoku::isSolved() const {
    return board == solution;
}

int Sudoku::countEmptyCells() const {
    int count = 0;
    for (const auto& row : board)
        for (int cell : row)
            if (cell == EMPTY) ++count;
    return count;
}

/**
 * @brief Безопасное чтение целого числа из стандартного ввода.
 */
int readInt() {
    int x;
    while (!(std::cin >> x)) {
        std::cin.clear();
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        std::cout << "Введите целое число: ";
    }
    return x;
}

/**
 * @brief Точка входа в программу.
 */
int main() {
#ifdef _WIN32
    SetConsoleOutputCP(CP_UTF8);
    SetConsoleCP(CP_UTF8);
#endif

    std::cout << "Добро пожаловать в Судоку 😊\n";
    std::cout << "Уровень сложности (20–60 пустых клеток, рекомендуется 40): ";
    int diff = readInt();
    diff = std::clamp(diff, 20, 60);

    Sudoku game(diff);
    clearScreen();
    game.printBoard();

    const int initialEmpty = game.countEmptyCells();
    int totalMoves = 0;
    int invalidMoves = 0;

    while (!game.isSolved()) {
        std::cout << "\nВведите: строка столбец число (1–9): ";
        int r = readInt();
        int c = readInt();
        int n = readInt();

        ++totalMoves;
        if (!game.makeMove(r - 1, c - 1, n)) {
            ++invalidMoves;
        } else {
            clearScreen();
            game.printBoard();
        }
    }

    // === Финальное сообщение с эмодзи и статистикой ===
    std::cout << "\n🎉 Поздравляем ... Вы решили судоку 🏆\n";
    std::cout << "📊 Статистика:\n";
    std::cout << "   Всего ходов: " << totalMoves << "\n";
    std::cout << "   Ошибок: " << invalidMoves << "\n";
    std::cout << "   Успешных ходов: " << (totalMoves - invalidMoves) << "\n";
    std::cout << "   Заполнено клеток: " << initialEmpty << "\n";

    return 0;
}