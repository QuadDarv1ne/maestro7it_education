#include <iostream>
#include <windows.h>
#include <conio.h>
#include <vector>
#include <string>

/**
 * @brief Упрощенный графический интерфейс для шахматного движка
 * 
 * Реализует псевдографический интерфейс в консоли Windows
 * с цветной визуализацией шахматной доски
 */

class ConsoleChessGUI {
private:
    // Представление доски (0=пусто, 1=белая фигура, 2=черная фигура)
    int board[8][8];
    
    // Выбранная фигура
    bool isSelected;
    int selectedRow, selectedCol;
    
    // Цвета для консоли
    HANDLE hConsole;
    
public:
    ConsoleChessGUI() : isSelected(false), selectedRow(-1), selectedCol(-1) {
        hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
        initializeBoard();
        setupConsole();
    }
    
    void setupConsole() {
        // Установка размера консоли
        COORD bufferSize = {80, 40};
        SetConsoleScreenBufferSize(hConsole, bufferSize);
        
        SMALL_RECT windowSize = {0, 0, 79, 39};
        SetConsoleWindowInfo(hConsole, TRUE, &windowSize);
        
        // Установка кодировки UTF-8
        SetConsoleOutputCP(CP_UTF8);
        SetConsoleCP(CP_UTF8);
    }
    
    void initializeBoard() {
        // Начальная позиция: 1=белые фигуры, 2=черные фигуры
        // Белые фигуры (ряд 0 и 1)
        for (int col = 0; col < 8; col++) {
            board[0][col] = 1; // Основные фигуры
            board[1][col] = 1; // Пешки
        }
        
        // Черные фигуры (ряд 6 и 7)
        for (int col = 0; col < 8; col++) {
            board[6][col] = 2; // Пешки
            board[7][col] = 2; // Основные фигуры
        }
        
        // Пустые клетки
        for (int row = 2; row < 6; row++) {
            for (int col = 0; col < 8; col++) {
                board[row][col] = 0;
            }
        }
    }
    
    void setColor(int color) {
        SetConsoleTextAttribute(hConsole, color);
    }
    
    void gotoXY(int x, int y) {
        COORD coord;
        coord.X = x;
        coord.Y = y;
        SetConsoleCursorPosition(hConsole, coord);
    }
    
    void drawBoard() {
        system("cls");
        
        // Верхняя граница
        setColor(15); // Белый
        gotoXY(0, 0);
        std::cout << "  ╔═══╤═══╤═══╤═══╤═══╤═══╤═══╤═══╗" << std::endl;
        
        // Доска
        for (int row = 0; row < 8; row++) {
            gotoXY(0, row * 2 + 1);
            setColor(15);
            std::cout << (8 - row) << " ║"; // Номера рядов
            
            for (int col = 0; col < 8; col++) {
                // Подсветка выбранной фигуры
                if (isSelected && row == selectedRow && col == selectedCol) {
                    setColor(14); // Желтый
                } else if ((row + col) % 2 == 0) {
                    setColor(112); // Светло-коричневый фон
                } else {
                    setColor(48);  // Темно-коричневый фон
                }
                
                // Отображение фигур
                if (board[row][col] == 1) {
                    setColor(15); // Белые фигуры
                    std::cout << " ● ";
                } else if (board[row][col] == 2) {
                    setColor(0);  // Черные фигуры
                    std::cout << " ● ";
                } else {
                    if ((row + col) % 2 == 0) {
                        setColor(112);
                        std::cout << "   ";
                    } else {
                        setColor(48);
                        std::cout << "   ";
                    }
                }
                
                setColor(15);
                if (col < 7) std::cout << "│";
            }
            
            setColor(15);
            std::cout << "║" << std::endl;
            
            // Горизонтальные линии
            if (row < 7) {
                gotoXY(0, row * 2 + 2);
                setColor(15);
                std::cout << "  ╟───┼───┼───┼───┼───┼───┼───┼───╢" << std::endl;
            }
        }
        
        // Нижняя граница и буквы колонок
        gotoXY(0, 17);
        setColor(15);
        std::cout << "  ╚═══╧═══╧═══╧═══╧═══╧═══╧═══╧═══╝" << std::endl;
        gotoXY(4, 18);
        std::cout << "a   b   c   d   e   f   g   h" << std::endl;
    }
    
    void drawInterface() {
        gotoXY(0, 20);
        setColor(15);
        std::cout << "УПРАВЛЕНИЕ:" << std::endl;
        std::cout << "WASD - навигация по доске" << std::endl;
        std::cout << "ENTER - выбрать/сделать ход" << std::endl;
        std::cout << "R - перезапуск игры" << std::cout << "ESC - выход" << std::endl;
        std::cout << std::endl;
        
        if (isSelected) {
            std::cout << "Выбрана фигура на " << (char)('a' + selectedCol) << (8 - selectedRow) << std::endl;
            std::cout << "Используйте WASD для выбора цели" << std::endl;
        } else {
            std::cout << "Выберите фигуру для хода" << std::endl;
        }
    }
    
    void run() {
        int cursorRow = 0;
        int cursorCol = 0;
        
        while (true) {
            drawBoard();
            drawInterface();
            
            // Позиция курсора
            gotoXY(cursorCol * 4 + 4, cursorRow * 2 + 1);
            setColor(10); // Зеленый
            std::cout << "█";
            
            int key = _getch();
            
            // Обработка управления
            switch (key) {
                case 27: // ESC
                    return;
                    
                case 'r':
                case 'R':
                    initializeBoard();
                    isSelected = false;
                    cursorRow = 0;
                    cursorCol = 0;
                    break;
                    
                case 'w':
                case 'W':
                    if (cursorRow > 0) cursorRow--;
                    break;
                    
                case 's':
                case 'S':
                    if (cursorRow < 7) cursorRow++;
                    break;
                    
                case 'a':
                case 'A':
                    if (cursorCol > 0) cursorCol--;
                    break;
                    
                case 'd':
                case 'D':
                    if (cursorCol < 7) cursorCol++;
                    break;
                    
                case 13: // ENTER
                    handleMove(cursorRow, cursorCol);
                    break;
            }
        }
    }
    
private:
    void handleMove(int row, int col) {
        if (isSelected) {
            // Перемещение фигуры
            if (board[selectedRow][selectedCol] != 0) {
                board[row][col] = board[selectedRow][selectedCol];
                board[selectedRow][selectedCol] = 0;
            }
            isSelected = false;
            selectedRow = -1;
            selectedCol = -1;
        } else {
            // Выбор фигуры
            if (board[row][col] != 0) {
                selectedRow = row;
                selectedCol = col;
                isSelected = true;
            }
        }
    }
};

int main() {
    SetConsoleTitle(L"Шахматный движок - Графический интерфейс");
    
    std::cout << "Запуск псевдографического шахматного интерфейса..." << std::endl;
    std::cout << "==================================================" << std::endl;
    std::cout << "Инициализация..." << std::endl;
    
    try {
        ConsoleChessGUI gui;
        gui.run();
        std::cout << "Интерфейс закрыт." << std::endl;
    } catch (const std::exception& e) {
        std::cerr << "Ошибка запуска интерфейса: " << e.what() << std::endl;
        return 1;
    }
    
    return 0;
}