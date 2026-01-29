#ifndef CHESS_GUI_HPP
#define CHESS_GUI_HPP

#include <SFML/Graphics.hpp>
#include <SFML/Window.hpp>
#include <SFML/System.hpp>
#include <iostream>
#include <vector>
#include <string>

/**
 * @brief Графический интерфейс для шахматного движка на SFML
 * 
 * Реализует визуальное представление шахматной доски, фигур и игрового процесса.
 * Интегрируется с консольным шахматным движком.
 */
class ChessGUI {
private:
    // Основные компоненты SFML
    sf::RenderWindow window;
    sf::Clock clock;
    sf::Font font;
    
    // Размеры и координаты
    static const int BOARD_SIZE = 8;
    static const int SQUARE_SIZE = 80;
    static const int WINDOW_WIDTH = 640;
    static const int WINDOW_HEIGHT = 640;
    
    // Цвета
    sf::Color lightSquareColor;
    sf::Color darkSquareColor;
    sf::Color highlightColor;
    sf::Color selectedColor;
    
    // Текстуры и спрайты
    sf::Texture pieceTextures[2][6]; // [цвет][тип фигуры]
    sf::Sprite boardSprites[BOARD_SIZE][BOARD_SIZE];
    
    // Игровое состояние
    int board[8][8]; // Представление доски
    bool isSelected;
    int selectedRow, selectedCol;
    std::vector<std::pair<int, int>> validMoves;
    
    // Тексты и интерфейс
    sf::Text statusText;
    sf::RectangleShape promotionPanel;
    bool showPromotion;
    int promotionRow, promotionCol;
    
public:
    ChessGUI();
    ~ChessGUI();
    
    // Основные методы
    bool initialize();
    void run();
    void handleEvents();
    void update();
    void render();
    
    // Игровая логика
    void initializeBoard();
    void loadPieceTextures();
    void setupBoardSprites();
    void handleMouseClick(int x, int y);
    std::vector<std::pair<int, int>> getValidMoves(int row, int col);
    bool isValidMove(int fromRow, int fromCol, int toRow, int toCol);
    void makeMove(int fromRow, int fromCol, int toRow, int toCol);
    void promotePawn(int row, int col, int pieceType);
    
    // Рендеринг
    void drawBoard();
    void drawPieces();
    void drawValidMoves();
    void drawStatus();
    void drawPromotionPanel();
    
    // Вспомогательные методы
    sf::Vector2f boardToScreen(int row, int col);
    std::pair<int, int> screenToBoard(int x, int y);
    int getPieceType(char piece);
    sf::Color getPlayerColor(char piece);
    
private:
    // Внутренние вспомогательные функции
    void loadTexture(sf::Texture& texture, const std::string& filename);
    sf::RectangleShape createSquare(int row, int col);
    bool isLightSquare(int row, int col);
    void resetSelection();
};

// Константы для фигур
namespace PieceTypes {
    enum {
        PAWN = 0,
        ROOK = 1,
        KNIGHT = 2,
        BISHOP = 3,
        QUEEN = 4,
        KING = 5
    };
}

// Константы для цветов
namespace Colors {
    enum {
        WHITE = 0,
        BLACK = 1
    };
}

#endif // CHESS_GUI_HPP