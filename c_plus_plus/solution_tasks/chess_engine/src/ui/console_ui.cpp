#include "../../include/console_ui.hpp"
#include <iostream>
#include <string>
#include <algorithm>
#include <locale>
#include <codecvt>

#ifdef _WIN32
#include <windows.h>
#endif

// Function to set console encoding
void setConsoleEncoding() {
#ifdef _WIN32
    // Set console to UTF-8
    SetConsoleOutputCP(CP_UTF8);
    SetConsoleCP(CP_UTF8);
#endif
}

ConsoleUI::ConsoleUI() : board_(), rules_(board_), aiEngine_(board_, 3), 
                         gameMode_(GameMode::HUMAN_VS_HUMAN),
                         whitePlayer_(PlayerType::HUMAN),
                         blackPlayer_(PlayerType::HUMAN),
                         aiDifficulty_(3) {
    setConsoleEncoding();
}

// Rest of the implementation remains the same

void ConsoleUI::run() {
    showMainMenu();
}

void ConsoleUI::showMainMenu() {
    while (true) {
        clearScreen();
        std::cout << "========================================\n";
        std::cout << "           ШАХМАТНЫЙ ДВИЖОК           \n";
        std::cout << "========================================\n\n";
        
        std::cout << "Главное меню:\n";
        std::cout << "1. Играть партию\n";
        std::cout << "2. Настройки\n";
        std::cout << "3. Помощь\n";
        std::cout << "4. Выход\n\n";
        
        std::cout << "Выберите пункт меню (1-4): ";
        
        std::string choice;
        std::getline(std::cin, choice);
        
        if (choice == "1") {
            startNewGame();
        } else if (choice == "2") {
            showGameSettings();
        } else if (choice == "3") {
            showHelp();
        } else if (choice == "4") {
            std::cout << "Спасибо за игру!\n";
            break;
        } else {
            std::cout << "Некорректный выбор. Нажмите Enter для продолжения...";
            std::cin.get();
        }
    }
}

void ConsoleUI::showGameSettings() {
    while (true) {
        clearScreen();
        std::cout << "=== Настройки ===\n\n";
        
        std::cout << "Текущие настройки:\n";
        std::cout << "Режим игры: ";
        switch (gameMode_) {
            case GameMode::HUMAN_VS_HUMAN:
                std::cout << "Человек против человека\n";
                break;
            case GameMode::HUMAN_VS_AI:
                std::cout << "Человек против компьютера\n";
                break;
            case GameMode::AI_VS_AI:
                std::cout << "Компьютер против компьютера\n";
                break;
        }
        
        std::cout << "Уровень сложности ИИ: " << aiDifficulty_ << "\n\n";
        
        std::cout << "1. Изменить режим игры\n";
        std::cout << "2. Изменить уровень сложности ИИ\n";
        std::cout << "3. Назад в главное меню\n\n";
        
        std::cout << "Выберите пункт (1-3): ";
        
        std::string choice;
        std::getline(std::cin, choice);
        
        if (choice == "1") {
            std::cout << "\nВыберите режим игры:\n";
            std::cout << "1. Человек против человека\n";
            std::cout << "2. Человек против компьютера\n";
            std::cout << "3. Компьютер против компьютера\n";
            std::cout << "Ваш выбор: ";
            
            std::string modeChoice;
            std::getline(std::cin, modeChoice);
            
            if (modeChoice == "1") {
                setGameMode(GameMode::HUMAN_VS_HUMAN);
                setPlayerTypes(PlayerType::HUMAN, PlayerType::HUMAN);
            } else if (modeChoice == "2") {
                setGameMode(GameMode::HUMAN_VS_AI);
                setPlayerTypes(PlayerType::HUMAN, PlayerType::AI);
            } else if (modeChoice == "3") {
                setGameMode(GameMode::AI_VS_AI);
                setPlayerTypes(PlayerType::AI, PlayerType::AI);
            }
            
        } else if (choice == "2") {
            std::cout << "\nВведите уровень сложности (1-6): ";
            std::string difficulty;
            std::getline(std::cin, difficulty);
            
            try {
                int level = std::stoi(difficulty);
                if (level >= 1 && level <= 6) {
                    setAIDifficulty(level);
                    aiEngine_.setMaxDepth(level);
                } else {
                    std::cout << "Уровень должен быть от 1 до 6!\n";
                }
            } catch (...) {
                std::cout << "Некорректный ввод!\n";
            }
            
            std::cout << "Нажмите Enter для продолжения...";
            std::cin.get();
            
        } else if (choice == "3") {
            break;
        }
    }
}

void ConsoleUI::startNewGame() {
    initializeGame();
    playGame();
}

void ConsoleUI::playGame() {
    while (!rules_.isGameOver()) {
        showBoard();
        showGameStatus();
        
        Color currentPlayer = board_.getCurrentPlayer();
        PlayerType currentPlayerType = (currentPlayer == Color::WHITE) ? 
                                       whitePlayer_ : blackPlayer_;
        
        Move move;
        if (currentPlayerType == PlayerType::HUMAN) {
            move = getPlayerMove(currentPlayer);
        } else {
            move = getAIMove(currentPlayer);
        }
        
        if (move.from == INVALID_SQUARE) {
            // Игрок хочет выйти или вернуться в меню
            break;
        }
        
        if (rules_.makeMove(move)) {
            std::cout << "Ход выполнен: " << move.toString() << "\n";
        } else {
            std::cout << "Некорректный ход!\n";
        }
        
        std::cout << "Нажмите Enter для продолжения...";
        std::cin.get();
    }
    
    // Показываем результат игры
    showBoard();
    std::cout << "\n=== Игра окончена ===\n";
    std::cout << "Результат: " << rules_.getGameResult() << "\n";
    
    if (rules_.isCheckmate(Color::WHITE)) {
        std::cout << "Черные выиграли!\n";
    } else if (rules_.isCheckmate(Color::BLACK)) {
        std::cout << "Белые выиграли!\n";
    } else if (rules_.isDraw()) {
        std::cout << "Ничья!\n";
    }
    
    std::cout << "\nНажмите Enter для возврата в меню...";
    std::cin.get();
}

Move ConsoleUI::getPlayerMove(Color playerColor) {
    while (true) {
        std::cout << "\nХодит " << getColorName(playerColor) << "\n";
        std::cout << "Введите ход (например: e2-e4) или 'menu' для выхода: ";
        
        std::string input;
        std::getline(std::cin, input);
        
        if (handleSpecialCommands(input)) {
            return Move(); // Возвращаем невалидный ход для выхода
        }
        
        Move move = parseMoveInput(input);
        if (move.from != INVALID_SQUARE && rules_.isValidMove(move)) {
            return move;
        } else {
            std::cout << "Некорректный ход! Попробуйте еще раз.\n";
        }
    }
}

Move ConsoleUI::getAIMove(Color playerColor) {
    std::cout << "\n" << getColorName(playerColor) << " (компьютер) думает...\n";
    
    Move bestMove = aiEngine_.findBestMove(playerColor);
    
    if (bestMove.from != INVALID_SQUARE) {
        std::cout << getColorName(playerColor) << " делает ход: " 
                  << board_.squareToAlgebraic(bestMove.from) << "-" 
                  << board_.squareToAlgebraic(bestMove.to) << "\n";
    }
    
    return bestMove;
}

Move ConsoleUI::parseMoveInput(const std::string& input) const {
    // TODO: реализовать полноценный парсинг ходов
    // Пока простая реализация для базовых ходов
    
    if (input.length() < 4) {
        return Move();
    }
    
    // Формат: e2-e4 или e2e4
    std::string fromStr, toStr;
    
    if (input[2] == '-') {
        fromStr = input.substr(0, 2);
        toStr = input.substr(3, 2);
    } else {
        fromStr = input.substr(0, 2);
        toStr = input.substr(2, 2);
    }
    
    Square from = board_.algebraicToSquare(fromStr);
    Square to = board_.algebraicToSquare(toStr);
    
    return Move(from, to);
}

bool ConsoleUI::isValidMoveFormat(const std::string& input) const {
    // TODO: реализовать проверку формата хода
    return input.length() >= 4;
}

void ConsoleUI::showBoard() const {
    board_.printBoard();
}

void ConsoleUI::showGameStatus() const {
    std::cout << "\nТекущий статус:\n";
    std::cout << "Ход: " << board_.getMoveCount() << "\n";
    std::cout << "Полуходов без взятий/пешечных ходов: " << board_.getHalfMoveClock() << "\n";
    
    if (rules_.isCheck(Color::WHITE)) {
        std::cout << "Белый король под шахом!\n";
    }
    if (rules_.isCheck(Color::BLACK)) {
        std::cout << "Черный король под шахом!\n";
    }
}

void ConsoleUI::showAvailableMoves(const std::vector<Move>& moves) const {
    std::cout << "Доступные ходы:\n";
    for (size_t i = 0; i < moves.size() && i < 10; i++) {
        std::cout << i + 1 << ". " << moves[i].toString() << "\n";
    }
    if (moves.size() > 10) {
        std::cout << "... и еще " << (moves.size() - 10) << " ходов\n";
    }
}

void ConsoleUI::showMessage(const std::string& message) const {
    std::cout << message << "\n";
}

void ConsoleUI::setGameMode(GameMode mode) {
    gameMode_ = mode;
}

void ConsoleUI::setPlayerTypes(PlayerType white, PlayerType black) {
    whitePlayer_ = white;
    blackPlayer_ = black;
}

void ConsoleUI::setAIDifficulty(int difficulty) {
    aiDifficulty_ = difficulty;
}

std::string ConsoleUI::getColorName(Color color) const {
    return (color == Color::WHITE) ? "Белые" : "Черные";
}

std::string ConsoleUI::getMoveString(const Move& move) const {
    if (move.from == INVALID_SQUARE) {
        return "Невалидный ход";
    }
    return board_.squareToAlgebraic(move.from) + "-" + board_.squareToAlgebraic(move.to);
}

void ConsoleUI::clearScreen() const {
#ifdef _WIN32
    system("cls");
#else
    system("clear");
#endif
}

// Приватные методы

void ConsoleUI::initializeGame() {
    board_.setupStartPosition();
}

bool ConsoleUI::handleSpecialCommands(const std::string& input) {
    std::string lowerInput = input;
    std::transform(lowerInput.begin(), lowerInput.end(), lowerInput.begin(), ::tolower);
    
    if (lowerInput == "quit" || lowerInput == "exit" || lowerInput == "menu") {
        return true;
    }
    return false;
}

void ConsoleUI::showHelp() const {
    clearScreen();
    std::cout << "=== Помощь ===\n\n";
    std::cout << "Формат ввода ходов:\n";
    std::cout << "- e2-e4 (ход пешки с e2 на e4)\n";
    std::cout << "- Ng1-f3 (ход коня с g1 на f3)\n";
    std::cout << "- O-O (короткая рокировка)\n";
    std::cout << "- O-O-O (длинная рокировка)\n\n";
    
    std::cout << "Специальные команды:\n";
    std::cout << "- menu (возврат в главное меню)\n";
    std::cout << "- quit (выход из программы)\n\n";
    
    std::cout << "Нажмите Enter для продолжения...";
    std::cin.get();
}