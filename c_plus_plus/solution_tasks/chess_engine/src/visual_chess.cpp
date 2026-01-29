#include <iostream>
#include <windows.h>
#include <vector>
#include <string>

class ChessVisualizer {
private:
    HANDLE hConsole;
    std::vector<std::vector<char>> board;
    
public:
    ChessVisualizer() {
        hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
        initializeBoard();
    }
    
    void initializeBoard() {
        board = {
            {'r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'},
            {'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'},
            {'.', '.', '.', '.', '.', '.', '.', '.'},
            {'.', '.', '.', '.', '.', '.', '.', '.'},
            {'.', '.', '.', '.', '.', '.', '.', '.'},
            {'.', '.', '.', '.', '.', '.', '.', '.'},
            {'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'},
            {'R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'}
        };
    }
    
    void setColor(int color) {
        SetConsoleTextAttribute(hConsole, color);
    }
    
    void drawBoard() {
        system("cls");
        setColor(15);
        std::cout << "    ШАХМАТНАЯ ДОСКА" << std::endl;
        std::cout << "  ====================" << std::endl;
        
        for (int row = 0; row < 8; row++) {
            setColor(15);
            std::cout << (8 - row) << " |";
            
            for (int col = 0; col < 8; col++) {
                if ((row + col) % 2 == 0) {
                    setColor(112); // светлые клетки
                } else {
                    setColor(48);  // темные клетки
                }
                
                char piece = board[row][col];
                if (piece != '.') {
                    if (isupper(piece)) {
                        setColor(15); // белые фигуры
                    } else {
                        setColor(0);  // черные фигуры
                    }
                    std::cout << " " << piece << " ";
                } else {
                    if ((row + col) % 2 == 0) {
                        setColor(112);
                    } else {
                        setColor(48);
                    }
                    std::cout << "   ";
                }
            }
            
            setColor(15);
            std::cout << "| " << (8 - row) << std::endl;
        }
        
        setColor(15);
        std::cout << "  ====================" << std::endl;
        std::cout << "    a  b  c  d  e  f  g  h" << std::endl;
        std::cout << std::endl;
    }
    
    void showInterface() {
        setColor(10);
        std::cout << "УПРАВЛЕНИЕ:" << std::endl;
        std::cout << "WASD - навигация" << std::endl;
        std::cout << "ENTER - сделать ход" << std::endl;
        std::cout << "R - перезапуск" << std::endl;
        std::cout << "ESC - выход" << std::endl;
        std::cout << std::endl;
        setColor(14);
        std::cout << "Текущий ход: Белые" << std::endl;
    }
    
    void run() {
        drawBoard();
        showInterface();
        
        while (true) {
            if (GetAsyncKeyState(VK_ESCAPE)) break;
            if (GetAsyncKeyState('R')) {
                initializeBoard();
                drawBoard();
                showInterface();
            }
            
            Sleep(50);
        }
    }
};

int main() {
    SetConsoleTitle(L"Шахматы - Графический интерфейс");
    
    ChessVisualizer visualizer;
    visualizer.run();
    
    return 0;
}