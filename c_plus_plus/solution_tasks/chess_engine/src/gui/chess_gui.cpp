#include "../include/chess_gui.hpp"
#include <cmath>
#include <algorithm>

ChessGUI::ChessGUI() 
    : window(sf::VideoMode(WINDOW_WIDTH, WINDOW_HEIGHT), "Chess Engine GUI"),
      isSelected(false),
      selectedRow(-1), selectedCol(-1),
      showPromotion(false),
      promotionRow(-1), promotionCol(-1) {
    
    // Инициализация цветов
    lightSquareColor = sf::Color(240, 217, 181);  // Светлые клетки
    darkSquareColor = sf::Color(181, 136, 99);    // Темные клетки
    highlightColor = sf::Color(100, 100, 255, 100); // Подсветка ходов
    selectedColor = sf::Color(255, 255, 0, 100);   // Выбранная фигура
    
    // Настройка окна
    window.setFramerateLimit(60);
    
    // Загрузка шрифта
    if (!font.loadFromFile("arial.ttf")) {
        // Если основной шрифт не найден, используем системный
        font = sf::Font();
    }
    
    // Настройка текста статуса
    statusText.setFont(font);
    statusText.setCharacterSize(20);
    statusText.setFillColor(sf::Color::White);
    statusText.setPosition(10, WINDOW_HEIGHT - 30);
    
    // Инициализация доски
    initializeBoard();
}

ChessGUI::~ChessGUI() {
    // Деструктор
}

bool ChessGUI::initialize() {
    try {
        loadPieceTextures();
        setupBoardSprites();
        return true;
    } catch (const std::exception& e) {
        std::cerr << "Ошибка инициализации GUI: " << e.what() << std::endl;
        return false;
    }
}

void ChessGUI::run() {
    while (window.isOpen()) {
        handleEvents();
        update();
        render();
    }
}

void ChessGUI::handleEvents() {
    sf::Event event;
    while (window.pollEvent(event)) {
        if (event.type == sf::Event::Closed) {
            window.close();
        }
        
        if (event.type == sf::Event::MouseButtonPressed) {
            if (event.mouseButton.button == sf::Mouse::Left) {
                int mouseX = event.mouseButton.x;
                int mouseY = event.mouseButton.y;
                
                if (showPromotion) {
                    // Обработка выбора превращения пешки
                    if (mouseX >= 200 && mouseX <= 440 && mouseY >= 250 && mouseY <= 350) {
                        int choice = (mouseX - 200) / 60;
                        if (choice >= 0 && choice <= 3) {
                            promotePawn(promotionRow, promotionCol, choice + 1); // 1=Queen, 2=Rook, 3=Bishop, 4=Knight
                            showPromotion = false;
                        }
                    }
                } else {
                    handleMouseClick(mouseX, mouseY);
                }
            }
        }
        
        if (event.type == sf::Event::KeyPressed) {
            if (event.key.code == sf::Keyboard::Escape) {
                window.close();
            }
            if (event.key.code == sf::Keyboard::R) {
                // Перезапуск игры
                initializeBoard();
                resetSelection();
            }
        }
    }
}

void ChessGUI::update() {
    // Обновление игровой логики
    float deltaTime = clock.restart().asSeconds();
    
    // Обновление статуса
    if (isSelected) {
        statusText.setString("Выбрана фигура. Выберите цель.");
    } else {
        statusText.setString("Выберите фигуру для хода.");
    }
}

void ChessGUI::render() {
    window.clear(sf::Color(50, 50, 50)); // Темно-серый фон
    
    drawBoard();
    drawPieces();
    drawValidMoves();
    drawStatus();
    
    if (showPromotion) {
        drawPromotionPanel();
    }
    
    window.display();
}

void ChessGUI::initializeBoard() {
    // Начальная расстановка фигур (стандартная позиция)
    // Белые фигуры
    board[0][0] = PieceTypes::ROOK | (Colors::WHITE << 3);
    board[0][1] = PieceTypes::KNIGHT | (Colors::WHITE << 3);
    board[0][2] = PieceTypes::BISHOP | (Colors::WHITE << 3);
    board[0][3] = PieceTypes::QUEEN | (Colors::WHITE << 3);
    board[0][4] = PieceTypes::KING | (Colors::WHITE << 3);
    board[0][5] = PieceTypes::BISHOP | (Colors::WHITE << 3);
    board[0][6] = PieceTypes::KNIGHT | (Colors::WHITE << 3);
    board[0][7] = PieceTypes::ROOK | (Colors::WHITE << 3);
    
    for (int i = 0; i < 8; i++) {
        board[1][i] = PieceTypes::PAWN | (Colors::WHITE << 3); // Белые пешки
    }
    
    // Черные фигуры
    board[7][0] = PieceTypes::ROOK | (Colors::BLACK << 3);
    board[7][1] = PieceTypes::KNIGHT | (Colors::BLACK << 3);
    board[7][2] = PieceTypes::BISHOP | (Colors::BLACK << 3);
    board[7][3] = PieceTypes::QUEEN | (Colors::BLACK << 3);
    board[7][4] = PieceTypes::KING | (Colors::BLACK << 3);
    board[7][5] = PieceTypes::BISHOP | (Colors::BLACK << 3);
    board[7][6] = PieceTypes::KNIGHT | (Colors::BLACK << 3);
    board[7][7] = PieceTypes::ROOK | (Colors::BLACK << 3);
    
    for (int i = 0; i < 8; i++) {
        board[6][i] = PieceTypes::PAWN | (Colors::BLACK << 3); // Черные пешки
    }
    
    // Пустые клетки
    for (int row = 2; row < 6; row++) {
        for (int col = 0; col < 8; col++) {
            board[row][col] = -1;
        }
    }
}

void ChessGUI::loadPieceTextures() {
    // Загрузка текстур фигур (пока используем простые цветные прямоугольники)
    // В реальном проекте здесь будут загружаться изображения PNG/SVG
    
    for (int color = 0; color < 2; color++) {
        for (int piece = 0; piece < 6; piece++) {
            // Создание простых цветных текстур для демонстрации
            sf::Image image;
            image.create(80, 80, color == Colors::WHITE ? sf::Color::White : sf::Color::Black);
            
            // Добавление узоров для различения фигур
            for (int i = 0; i < 80; i += 10) {
                for (int j = 0; j < 80; j += 10) {
                    if ((i/10 + j/10) % 2 == 0) {
                        sf::Color patternColor = (piece % 2 == 0) ? sf::Color::Blue : sf::Color::Red;
                        for (int x = i; x < std::min(i+10, 80); x++) {
                            for (int y = j; y < std::min(j+10, 80); y++) {
                                image.setPixel(x, y, patternColor);
                            }
                        }
                    }
                }
            }
            
            pieceTextures[color][piece].loadFromImage(image);
        }
    }
}

void ChessGUI::setupBoardSprites() {
    for (int row = 0; row < BOARD_SIZE; row++) {
        for (int col = 0; col < BOARD_SIZE; col++) {
            boardSprites[row][col].setPosition(boardToScreen(row, col));
            boardSprites[row][col].setSize(sf::Vector2f(SQUARE_SIZE, SQUARE_SIZE));
        }
    }
}

void ChessGUI::handleMouseClick(int x, int y) {
    auto [row, col] = screenToBoard(x, y);
    
    if (row < 0 || row >= BOARD_SIZE || col < 0 || col >= BOARD_SIZE) {
        return;
    }
    
    if (isSelected) {
        // Проверка, является ли это допустимым ходом
        auto it = std::find(validMoves.begin(), validMoves.end(), std::make_pair(row, col));
        if (it != validMoves.end()) {
            makeMove(selectedRow, selectedCol, row, col);
            
            // Проверка на превращение пешки
            if (abs(row - selectedRow) == 1 && 
                (row == 0 || row == 7) && 
                (board[selectedRow][selectedCol] & 7) == PieceTypes::PAWN) {
                showPromotion = true;
                promotionRow = row;
                promotionCol = col;
            }
        }
        resetSelection();
    } else {
        // Выбор фигуры
        if (board[row][col] != -1) {
            selectedRow = row;
            selectedCol = col;
            isSelected = true;
            validMoves = getValidMoves(row, col);
        }
    }
}

std::vector<std::pair<int, int>> ChessGUI::getValidMoves(int row, int col) {
    std::vector<std::pair<int, int>> moves;
    int piece = board[row][col] & 7;
    int color = (board[row][col] >> 3) & 1;
    
    // Пока реализуем простую логику для демонстрации
    switch (piece) {
        case PieceTypes::PAWN:
            // Пешка может двигаться вперед на одну клетку
            int direction = (color == Colors::WHITE) ? -1 : 1;
            int newRow = row + direction;
            if (newRow >= 0 && newRow < BOARD_SIZE && board[newRow][col] == -1) {
                moves.push_back({newRow, col});
            }
            break;
            
        case PieceTypes::ROOK:
            // Ладья может двигаться по горизонтали и вертикали
            for (int i = row + 1; i < BOARD_SIZE; i++) {
                if (board[i][col] == -1) moves.push_back({i, col});
                else break;
            }
            for (int i = row - 1; i >= 0; i--) {
                if (board[i][col] == -1) moves.push_back({i, col});
                else break;
            }
            for (int j = col + 1; j < BOARD_SIZE; j++) {
                if (board[row][j] == -1) moves.push_back({row, j});
                else break;
            }
            for (int j = col - 1; j >= 0; j--) {
                if (board[row][j] == -1) moves.push_back({row, j});
                else break;
            }
            break;
            
        case PieceTypes::KING:
            // Король может двигаться на одну клетку во всех направлениях
            for (int i = -1; i <= 1; i++) {
                for (int j = -1; j <= 1; j++) {
                    if (i == 0 && j == 0) continue;
                    int newRow = row + i;
                    int newCol = col + j;
                    if (newRow >= 0 && newRow < BOARD_SIZE && newCol >= 0 && newCol < BOARD_SIZE) {
                        moves.push_back({newRow, newCol});
                    }
                }
            }
            break;
            
        default:
            // Для остальных фигур - базовая реализация
            break;
    }
    
    return moves;
}

bool ChessGUI::isValidMove(int fromRow, int fromCol, int toRow, int toCol) {
    auto moves = getValidMoves(fromRow, fromCol);
    return std::find(moves.begin(), moves.end(), std::make_pair(toRow, toCol)) != moves.end();
}

void ChessGUI::makeMove(int fromRow, int fromCol, int toRow, int toCol) {
    board[toRow][toCol] = board[fromRow][fromCol];
    board[fromRow][fromCol] = -1;
}

void ChessGUI::promotePawn(int row, int col, int pieceType) {
    int color = (board[row][col] >> 3) & 1;
    board[row][col] = pieceType | (color << 3);
}

void ChessGUI::drawBoard() {
    for (int row = 0; row < BOARD_SIZE; row++) {
        for (int col = 0; col < BOARD_SIZE; col++) {
            sf::RectangleShape square = createSquare(row, col);
            window.draw(square);
        }
    }
}

void ChessGUI::drawPieces() {
    for (int row = 0; row < BOARD_SIZE; row++) {
        for (int col = 0; col < BOARD_SIZE; col++) {
            if (board[row][col] != -1) {
                int piece = board[row][col] & 7;
                int color = (board[row][col] >> 3) & 1;
                
                sf::RectangleShape pieceShape(sf::Vector2f(SQUARE_SIZE - 10, SQUARE_SIZE - 10));
                pieceShape.setPosition(boardToScreen(row, col).x + 5, boardToScreen(row, col).y + 5);
                
                // Цвет фигуры
                pieceShape.setFillColor(color == Colors::WHITE ? sf::Color::White : sf::Color::Black);
                pieceShape.setOutlineThickness(2);
                pieceShape.setOutlineColor(sf::Color::Blue);
                
                window.draw(pieceShape);
            }
        }
    }
}

void ChessGUI::drawValidMoves() {
    if (isSelected) {
        // Подсветка выбранной фигуры
        sf::RectangleShape selectedSquare(sf::Vector2f(SQUARE_SIZE, SQUARE_SIZE));
        selectedSquare.setPosition(boardToScreen(selectedRow, selectedCol));
        selectedSquare.setFillColor(selectedColor);
        window.draw(selectedSquare);
        
        // Подсветка допустимых ходов
        for (const auto& move : validMoves) {
            sf::CircleShape circle(SQUARE_SIZE / 6);
            circle.setPosition(
                boardToScreen(move.first, move.second).x + SQUARE_SIZE / 3,
                boardToScreen(move.first, move.second).y + SQUARE_SIZE / 3
            );
            circle.setFillColor(highlightColor);
            window.draw(circle);
        }
    }
}

void ChessGUI::drawStatus() {
    window.draw(statusText);
}

void ChessGUI::drawPromotionPanel() {
    // Панель выбора превращения
    sf::RectangleShape panel(sf::Vector2f(240, 100));
    panel.setPosition(200, 250);
    panel.setFillColor(sf::Color(200, 200, 200, 230));
    panel.setOutlineThickness(2);
    panel.setOutlineColor(sf::Color::Black);
    window.draw(panel);
    
    // Текст
    sf::Text prompt("Выберите фигуру:", font, 16);
    prompt.setPosition(220, 260);
    prompt.setFillColor(sf::Color::Black);
    window.draw(prompt);
    
    // Варианты превращения
    std::string pieces[] = {"♛", "♜", "♝", "♞"};
    for (int i = 0; i < 4; i++) {
        sf::Text pieceText(pieces[i], font, 24);
        pieceText.setPosition(220 + i * 60, 290);
        pieceText.setFillColor(sf::Color::Black);
        window.draw(pieceText);
    }
}

sf::Vector2f ChessGUI::boardToScreen(int row, int col) {
    return sf::Vector2f(col * SQUARE_SIZE, row * SQUARE_SIZE);
}

std::pair<int, int> ChessGUI::screenToBoard(int x, int y) {
    return {y / SQUARE_SIZE, x / SQUARE_SIZE};
}

sf::RectangleShape ChessGUI::createSquare(int row, int col) {
    sf::RectangleShape square(sf::Vector2f(SQUARE_SIZE, SQUARE_SIZE));
    square.setPosition(boardToScreen(row, col));
    square.setFillColor(isLightSquare(row, col) ? lightSquareColor : darkSquareColor);
    return square;
}

bool ChessGUI::isLightSquare(int row, int col) {
    return (row + col) % 2 == 0;
}

void ChessGUI::resetSelection() {
    isSelected = false;
    selectedRow = -1;
    selectedCol = -1;
    validMoves.clear();
}