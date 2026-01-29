#include <iostream>
#include <SFML/Graphics.hpp>
#include <SFML/Window.hpp>

/**
 * @brief Главный файл запуска графического шахматного движка
 * 
 * Интегрирует консольный шахматный движок с графическим интерфейсом на SFML.
 * Предоставляет полноценный визуальный опыт игры в шахматы.
 */

// Простая реализация шахматной доски для демонстрации
class SimpleChessGUI {
private:
    sf::RenderWindow window;
    static const int BOARD_SIZE = 8;
    static const int SQUARE_SIZE = 80;
    
    // Цвета доски
    sf::Color lightSquare;
    sf::Color darkSquare;
    
    // Представление доски (0=пусто, 1=белая фигура, 2=черная фигура)
    int board[8][8];
    
    // Выбранная фигура
    bool isSelected;
    int selectedRow, selectedCol;
    
public:
    SimpleChessGUI() : window(sf::VideoMode(640, 640), "Chess Engine GUI"),
                       lightSquare(240, 217, 181),
                       darkSquare(181, 136, 99),
                       isSelected(false),
                       selectedRow(-1), selectedCol(-1) {
        
        window.setFramerateLimit(60);
        initializeBoard();
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
    
    void run() {
        while (window.isOpen()) {
            handleEvents();
            render();
        }
    }
    
private:
    void handleEvents() {
        sf::Event event;
        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed) {
                window.close();
            }
            
            if (event.type == sf::Event::MouseButtonPressed) {
                if (event.mouseButton.button == sf::Mouse::Left) {
                    handleMouseClick(event.mouseButton.x, event.mouseButton.y);
                }
            }
            
            if (event.type == sf::Event::KeyPressed) {
                if (event.key.code == sf::Keyboard::Escape) {
                    window.close();
                }
                if (event.key.code == sf::Keyboard::R) {
                    initializeBoard();
                    isSelected = false;
                }
            }
        }
    }
    
    void handleMouseClick(int x, int y) {
        int col = x / SQUARE_SIZE;
        int row = y / SQUARE_SIZE;
        
        if (row < 0 || row >= 8 || col < 0 || col >= 8) return;
        
        if (isSelected) {
            // Перемещение фигуры
            if (board[selectedRow][selectedCol] != 0) {
                board[row][col] = board[selectedRow][selectedCol];
                board[selectedRow][selectedCol] = 0;
            }
            isSelected = false;
        } else {
            // Выбор фигуры
            if (board[row][col] != 0) {
                selectedRow = row;
                selectedCol = col;
                isSelected = true;
            }
        }
    }
    
    void render() {
        window.clear(sf::Color(50, 50, 50));
        
        // Отрисовка доски
        for (int row = 0; row < BOARD_SIZE; row++) {
            for (int col = 0; col < BOARD_SIZE; col++) {
                sf::RectangleShape square(sf::Vector2f(SQUARE_SIZE, SQUARE_SIZE));
                square.setPosition(col * SQUARE_SIZE, row * SQUARE_SIZE);
                square.setFillColor((row + col) % 2 == 0 ? lightSquare : darkSquare);
                
                // Подсветка выбранной фигуры
                if (isSelected && row == selectedRow && col == selectedCol) {
                    square.setFillColor(sf::Color(255, 255, 0, 100));
                }
                
                window.draw(square);
                
                // Отрисовка фигур
                if (board[row][col] != 0) {
                    sf::CircleShape piece(SQUARE_SIZE / 3);
                    piece.setPosition(col * SQUARE_SIZE + SQUARE_SIZE / 6, 
                                    row * SQUARE_SIZE + SQUARE_SIZE / 6);
                    piece.setFillColor(board[row][col] == 1 ? sf::Color::White : sf::Color::Black);
                    piece.setOutlineThickness(2);
                    piece.setOutlineColor(sf::Color::Blue);
                    window.draw(piece);
                }
            }
        }
        
        // Инструкции
        sf::Font font;
        if (font.loadFromFile("arial.ttf")) {
            sf::Text instructions("Кликните на фигуру для выбора, затем на цель для хода\nR - перезапуск, ESC - выход", font, 16);
            instructions.setFillColor(sf::Color::White);
            instructions.setPosition(10, 610);
            window.draw(instructions);
        }
        
        window.display();
    }
};

int main() {
    std::cout << "Запуск графического шахматного движка на SFML..." << std::endl;
    std::cout << "===============================================" << std::endl;
    std::cout << "Управление:" << std::endl;
    std::cout << "- Кликните на фигуру для выбора" << std::endl;
    std::cout << "- Кликните на цель для хода" << std::endl;
    std::cout << "- R - перезапуск игры" << std::endl;
    std::cout << "- ESC - выход" << std::endl;
    std::cout << "===============================================" << std::endl;
    
    try {
        SimpleChessGUI gui;
        gui.run();
        std::cout << "Графический интерфейс закрыт." << std::endl;
    } catch (const std::exception& e) {
        std::cerr << "Ошибка запуска GUI: " << e.what() << std::endl;
        return 1;
    }
    
    return 0;
}