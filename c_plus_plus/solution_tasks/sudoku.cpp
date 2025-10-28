#include <iostream>
#include <vector>
#include <random>
#include <algorithm>

/**
 * g++ -std=c++17 -O2 -Wall -Wextra -o sudoku sudoku.cpp
 * ./sudoku
 */

class Sudoku {
private:
    static constexpr int N = 9;
    std::vector<std::vector<int>> board;
    std::vector<std::vector<int>> solution;

    // Базовое заполнение по шаблону (валидное решение)
    void fillBaseSolution() {
        for (int i = 0; i < N; ++i)
            for (int j = 0; j < N; ++j)
                solution[i][j] = (i * 3 + i / 3 + j) % N + 1;
    }

    // Перемешивание строк/столбцов внутри групп для разнообразия
    void shuffle() {
        std::random_device rd;
        std::mt19937 g(rd());

        // Перемешиваем группы строк (0-2, 3-5, 6-8)
        for (int band = 0; band < 3; ++band) {
            std::vector<int> rows = {band * 3, band * 3 + 1, band * 3 + 2};
            std::shuffle(rows.begin(), rows.end(), g);
            std::vector<std::vector<int>> temp = solution;
            for (int i = 0; i < 3; ++i)
                solution[band * 3 + i] = temp[rows[i]];
        }

        // Перемешиваем группы столбцов
        for (int stack = 0; stack < 3; ++stack) {
            std::vector<int> cols = {stack * 3, stack * 3 + 1, stack * 3 + 2};
            std::shuffle(cols.begin(), cols.end(), g);
            for (int i = 0; i < N; ++i) {
                std::vector<int> temp_row = solution[i];
                for (int j = 0; j < 3; ++j)
                    solution[i][stack * 3 + j] = temp_row[cols[j]];
            }
        }
    }

    bool canPlace(int row, int col, int num) const {
        // Проверка строки
        for (int j = 0; j < N; ++j)
            if (board[row][j] == num) return false;

        // Проверка столбца
        for (int i = 0; i < N; ++i)
            if (board[i][col] == num) return false;

        // Проверка блока 3x3
        int startRow = row - row % 3;
        int startCol = col - col % 3;
        for (int i = 0; i < 3; ++i)
            for (int j = 0; j < 3; ++j)
                if (board[startRow + i][startCol + j] == num)
                    return false;

        return true;
    }

public:
    Sudoku(int difficulty = 40) : board(N, std::vector<int>(N, 0)), solution(N, std::vector<int>(N, 0)) {
        fillBaseSolution();
        shuffle();

        // Копируем решение
        board = solution;

        // Удаляем случайные клетки
        std::random_device rd;
        std::mt19937 gen(rd());
        std::uniform_int_distribution<> dis(0, N * N - 1);

        int removed = 0;
        while (removed < difficulty) {
            int pos = dis(gen);
            int row = pos / N;
            int col = pos % N;
            if (board[row][col] != 0) {
                board[row][col] = 0;
                ++removed;
            }
        }
    }

    void printBoard() const {
        std::cout << "+-------+-------+-------+\n";
        for (int i = 0; i < N; ++i) {
            std::cout << "| ";
            for (int j = 0; j < N; ++j) {
                if (board[i][j] == 0)
                    std::cout << ". ";
                else
                    std::cout << board[i][j] << " ";
                if (j % 3 == 2) std::cout << "| ";
            }
            std::cout << "\n";
            if (i % 3 == 2)
                std::cout << "+-------+-------+-------+\n";
        }
    }

    bool makeMove(int row, int col, int num) {
        if (row < 0 || row >= N || col < 0 || col >= N || num < 1 || num > 9) {
            std::cout << "Некорректные координаты или число!\n";
            return false;
        }
        if (board[row][col] != 0) {
            std::cout << "Клетка уже заполнена!\n";
            return false;
        }
        if (!canPlace(row, col, num)) {
            std::cout << "Ход нарушает правила судоку!\n";
            return false;
        }
        board[row][col] = num;
        return true;
    }

    bool isSolved() const {
        for (int i = 0; i < N; ++i)
            for (int j = 0; j < N; ++j)
                if (board[i][j] != solution[i][j])
                    return false;
        return true;
    }
};

int main() {
    std::cout << "Добро пожаловать в Судоку!\n";
    std::cout << "Введите сложность (количество пустых клеток, например: 40): ";
    int diff;
    std::cin >> diff;
    if (diff < 20) diff = 20;
    if (diff > 60) diff = 60;

    Sudoku game(diff);
    game.printBoard();

    while (!game.isSolved()) {
        int r, c, n;
        std::cout << "\nВведите строку (1-9), столбец (1-9) и число (1-9): ";
        std::cin >> r >> c >> n;
        if (!std::cin) {
            std::cout << "Ошибка ввода. Завершение.\n";
            return 1;
        }
        game.makeMove(r - 1, c - 1, n);
        game.printBoard();
    }

    std::cout << "\nПоздравляем ... Судоку решено ...\n";
    return 0;
}