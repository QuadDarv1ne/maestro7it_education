#include "../include/game_rules.hpp"
#include "../include/move_generator.hpp"
#include <algorithm>

GameRules::GameRules(Board& board) : board_(board) {}

bool GameRules::isValidMove(const Move& move) const {
    // TODO: реализовать полную проверку легальности хода
    // Пока используем базовую проверку
    
    if (move.from == INVALID_SQUARE || move.to == INVALID_SQUARE) {
        return false;
    }
    
    // Проверяем, что фигура принадлежит текущему игроку
    Piece piece = board_.getPiece(move.from);
    if (piece.isEmpty() || piece.getColor() != board_.getCurrentPlayer()) {
        return false;
    }
    
    // TODO: проверить, не оставляет ли ход короля под шахом
    // TODO: проверить специальные правила для каждого типа фигуры
    
    return true;
}

bool GameRules::isValidMove(const std::string& algebraicNotation) const {
    // TODO: реализовать парсинг алгебраической нотации
    // Пока возвращаем false
    return false;
}

bool GameRules::isCheck(Color color) const {
    // TODO: реализовать проверку шаха
    // Найти короля указанного цвета и проверить, атакован ли он
    return false;
}

bool GameRules::isCheckmate(Color color) const {
    // TODO: реализовать проверку мата
    // Король под шахом и нет легальных ходов для спасения
    return false;
}

bool GameRules::isStalemate(Color color) const {
    // TODO: реализовать проверку пата
    // Король не под шахом, но нет легальных ходов
    return false;
}

bool GameRules::isDrawByRepetition() const {
    // TODO: реализовать правило тройного повторения
    return false;
}

bool GameRules::isDrawByFiftyMoveRule() const {
    // TODO: реализовать правило 50 ходов
    return board_.getHalfMoveClock() >= 100; // 50 полных ходов = 100 полуходов
}

bool GameRules::isInsufficientMaterial() const {
    // TODO: реализовать проверку недостатка материала
    // Только короли, король + слон, король + конь и т.д.
    return false;
}

bool GameRules::makeMove(const Move& move) {
    if (!isValidMove(move)) {
        return false;
    }
    
    // Выполняем ход
    Piece movingPiece = board_.getPiece(move.from);
    Piece capturedPiece = board_.getPiece(move.to);
    
    // Обновляем доску
    board_.setPiece(move.to, movingPiece);
    board_.setPiece(move.from, Piece()); // Очищаем исходную клетку
    
    // TODO: обработать специальные ходы
    // - Рокировка
    // - Взятие на проходе
    // - Превращение пешки
    
    // Обновляем состояние игры
    updateGameStateAfterMove(move);
    
    // Меняем текущего игрока
    Color currentPlayer = board_.getCurrentPlayer();
    board_.setCurrentPlayer(Piece::oppositeColor(currentPlayer));
    
    // Увеличиваем счетчик ходов если ходили черные
    if (currentPlayer == Color::BLACK) {
        board_.setHalfMoveClock(board_.getHalfMoveClock() + 1);
    }
    
    return true;
}

bool GameRules::makeMove(const std::string& algebraicNotation) {
    // TODO: реализовать парсинг и выполнение хода из алгебраической нотации
    return false;
}

bool GameRules::isGameOver() const {
    Color currentPlayer = board_.getCurrentPlayer();
    return isCheckmate(currentPlayer) || 
           isStalemate(currentPlayer) || 
           isDrawByRepetition() || 
           isDrawByFiftyMoveRule() || 
           isInsufficientMaterial();
}

std::string GameRules::getGameResult() const {
    if (isCheckmate(Color::WHITE)) {
        return "0-1"; // Черные выиграли
    } else if (isCheckmate(Color::BLACK)) {
        return "1-0"; // Белые выиграли
    } else if (isStalemate(Color::WHITE) || 
               isStalemate(Color::BLACK) ||
               isDrawByRepetition() ||
               isDrawByFiftyMoveRule() ||
               isInsufficientMaterial()) {
        return "1/2-1/2"; // Ничья
    }
    return "*"; // Игра продолжается
}

Color GameRules::getWinner() const {
    if (isCheckmate(Color::WHITE)) {
        return Color::BLACK;
    } else if (isCheckmate(Color::BLACK)) {
        return Color::WHITE;
    }
    return Color::WHITE; // Нет победителя
}

bool GameRules::isDraw() const {
    return isStalemate(Color::WHITE) || 
           isStalemate(Color::BLACK) ||
           isDrawByRepetition() ||
           isDrawByFiftyMoveRule() ||
           isInsufficientMaterial();
}

// Приватные методы

bool GameRules::wouldLeaveKingInCheck(const Move& move) const {
    // TODO: реализовать проверку, оставляет ли ход короля под шахом
    // Создать временную копию доски, выполнить ход и проверить шах
    return false;
}

void GameRules::updateGameStateAfterMove(const Move& move) {
    // TODO: обновить все игровые состояния после хода
    // - Права рокировки
    // - Возможность взятия на проходе
    // - Счетчик полуходов
    // - Номер хода
    
    // Сбрасываем счетчик полуходов при взятии или ходе пешки
    Piece movingPiece = board_.getPiece(move.to);
    Piece capturedPiece = board_.getPiece(move.from);
    
    if (movingPiece.getType() == PieceType::PAWN || !capturedPiece.isEmpty()) {
        board_.setHalfMoveClock(0);
    }
}

bool GameRules::hasLegalMoves(Color color) const {
    // TODO: проверить, есть ли у игрока легальные ходы
    Board tempBoard = board_; // Создаем копию для проверки
    // Это временная реализация
    return true;
}

int GameRules::countPieces(Color color) const {
    int count = 0;
    for (int square = 0; square < 64; square++) {
        Piece piece = board_.getPiece(square);
        if (!piece.isEmpty() && piece.getColor() == color) {
            count++;
        }
    }
    return count;
}

bool GameRules::onlyKingsRemain() const {
    return countPieces(Color::WHITE) == 1 && countPieces(Color::BLACK) == 1;
}