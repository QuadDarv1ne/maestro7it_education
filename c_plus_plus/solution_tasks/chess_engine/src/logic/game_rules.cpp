#include "../../include/game_rules.hpp"
#include "../../include/move_generator.hpp"
#include <algorithm>

GameRules::GameRules(Board& board) : board_(board) {}

bool GameRules::isValidMove(const Move& move) const {
    if (move.from == INVALID_SQUARE || move.to == INVALID_SQUARE) {
        return false;
    }
    
    // Генерируем все легальные ходы для текущей позиции
    MoveGenerator moveGen(board_);
    std::vector<Move> legalMoves = moveGen.generateLegalMoves();
    
    // Проверяем, есть ли наш ход в списке легальных
    for (const Move& legalMove : legalMoves) {
        if (legalMove.from == move.from && legalMove.to == move.to) {
            // Если это превращение, проверяем тип фигуры
            if (move.promotion != PieceType::EMPTY) {
                if (legalMove.promotion == move.promotion) {
                    return true;
                }
            } else {
                return true;
            }
        }
    }
    
    return false;
}

bool GameRules::isValidMove(const std::string& algebraicNotation) const {
    if (algebraicNotation.length() < 4) return false;
    
    Square from = board_.algebraicToSquare(algebraicNotation.substr(0, 2));
    Square to = board_.algebraicToSquare(algebraicNotation.substr(2, 2));
    
    if (from == INVALID_SQUARE || to == INVALID_SQUARE) return false;
    
    Move move(from, to);
    
    // Проверка на превращение (например e7e8q)
    if (algebraicNotation.length() >= 5) {
        char p = std::tolower(algebraicNotation[4]);
        if (p == 'q') move.promotion = PieceType::QUEEN;
        else if (p == 'r') move.promotion = PieceType::ROOK;
        else if (p == 'b') move.promotion = PieceType::BISHOP;
        else if (p == 'n') move.promotion = PieceType::KNIGHT;
    }
    
    return isValidMove(move);
}

bool GameRules::isCheck(Color color) const {
    // Находим короля указанного цвета
    Square kingSquare = INVALID_SQUARE;
    for (int square = 0; square < 64; square++) {
        Piece piece = board_.getPiece(square);
        if (piece.getType() == PieceType::KING && piece.getColor() == color) {
            kingSquare = square;
            break;
        }
    }
    
    if (kingSquare == INVALID_SQUARE) {
        return false; // Король не найден (некорректная позиция)
    }
    
    // Проверяем, атакована ли клетка короля противником
    MoveGenerator moveGen(board_);
    Color opponentColor = (color == Color::WHITE) ? Color::BLACK : Color::WHITE;
    return moveGen.isSquareAttacked(kingSquare, opponentColor);
}

bool GameRules::isCheckmate(Color color) const {
    // Мат = король под шахом И нет легальных ходов
    if (!isCheck(color)) {
        return false;
    }
    
    return !hasLegalMoves(color);
}

bool GameRules::isStalemate(Color color) const {
    // Пат = король НЕ под шахом И нет легальных ходов
    if (isCheck(color)) {
        return false;
    }
    
    return !hasLegalMoves(color);
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
    // Подсчитываем материал на доске
    int whiteKnights = 0, blackKnights = 0;
    int whiteBishops = 0, blackBishops = 0;
    int whitePawns = 0, blackPawns = 0;
    int whiteRooks = 0, blackRooks = 0;
    int whiteQueens = 0, blackQueens = 0;
    
    for (int square = 0; square < 64; square++) {
        Piece piece = board_.getPiece(square);
        if (piece.isEmpty()) continue;
        
        Color color = piece.getColor();
        PieceType type = piece.getType();
        
        if (type == PieceType::PAWN) {
            color == Color::WHITE ? whitePawns++ : blackPawns++;
        } else if (type == PieceType::KNIGHT) {
            color == Color::WHITE ? whiteKnights++ : blackKnights++;
        } else if (type == PieceType::BISHOP) {
            color == Color::WHITE ? whiteBishops++ : blackBishops++;
        } else if (type == PieceType::ROOK) {
            color == Color::WHITE ? whiteRooks++ : blackRooks++;
        } else if (type == PieceType::QUEEN) {
            color == Color::WHITE ? whiteQueens++ : blackQueens++;
        }
    }
    
    // Случаи недостаточного материала:
    // 1. Только короли
    if (whiteKnights == 0 && blackKnights == 0 &&
        whiteBishops == 0 && blackBishops == 0 &&
        whitePawns == 0 && blackPawns == 0 &&
        whiteRooks == 0 && blackRooks == 0 &&
        whiteQueens == 0 && blackQueens == 0) {
        return true;
    }
    
    // 2. Король + конь против короля
    if ((whiteKnights == 1 && blackKnights == 0 && 
         whiteBishops == 0 && blackBishops == 0) ||
        (blackKnights == 1 && whiteKnights == 0 && 
         whiteBishops == 0 && blackBishops == 0)) {
        if (whitePawns == 0 && blackPawns == 0 &&
            whiteRooks == 0 && blackRooks == 0 &&
            whiteQueens == 0 && blackQueens == 0) {
            return true;
        }
    }
    
    // 3. Король + слон против короля
    if ((whiteBishops == 1 && blackBishops == 0 && 
         whiteKnights == 0 && blackKnights == 0) ||
        (blackBishops == 1 && whiteBishops == 0 && 
         whiteKnights == 0 && blackKnights == 0)) {
        if (whitePawns == 0 && blackPawns == 0 &&
            whiteRooks == 0 && blackRooks == 0 &&
            whiteQueens == 0 && blackQueens == 0) {
            return true;
        }
    }
    
    // 4. Король + слон против короля + слон (одноцветные слоны)
    if (whiteBishops == 1 && blackBishops == 1 &&
        whiteKnights == 0 && blackKnights == 0 &&
        whitePawns == 0 && blackPawns == 0 &&
        whiteRooks == 0 && blackRooks == 0 &&
        whiteQueens == 0 && blackQueens == 0) {
        // TODO: проверить что слоны на одноцветных полях
        // Упрощенная версия - считаем что это недостаточный материал
        return true;
    }
    
    return false;
}

bool GameRules::makeMove(const Move& move) {
    if (!isValidMove(move)) {
        return false;
    }
    
    // Выполняем ход
    Piece movingPiece = board_.getPiece(move.from);
    Piece capturedPiece = board_.getPiece(move.to);
    
    // Сохраняем историю для отмены
    board_.pushHistory(move.from, move.to, capturedPiece, move.isCastling, move.isEnPassant, move.promotion);
    
    // 1. Обработка рокировки
    if (move.isCastling) {
        int rank = board_.rank(move.from);
        int fromFile = board_.file(move.from);
        int toFile = board_.file(move.to);
        
        // Перемещаем ладью
        if (toFile == 6) { // Короткая рокировка
            Square rookFrom = board_.square(7, rank);
            Square rookTo = board_.square(5, rank);
            board_.setPiece(rookTo, board_.getPiece(rookFrom));
            board_.setPiece(rookFrom, Piece());
        } else if (toFile == 2) { // Длинная рокировка
            Square rookFrom = board_.square(0, rank);
            Square rookTo = board_.square(3, rank);
            board_.setPiece(rookTo, board_.getPiece(rookFrom));
            board_.setPiece(rookFrom, Piece());
        }
    }
    
    // 2. Обработка взятия на проходе
    if (move.isEnPassant) {
        int fromFile = board_.file(move.from);
        int toFile = board_.file(move.to);
        int fromRank = board_.rank(move.from);
        Square capturedPawnSquare = board_.square(toFile, fromRank);
        board_.setPiece(capturedPawnSquare, Piece());
    }
    
    // 3. Обработка превращения пешки
    if (move.promotion != PieceType::EMPTY) {
        movingPiece = Piece(move.promotion, movingPiece.getColor());
    }
    
    // Стандартное перемещение фигуры
    board_.setPiece(move.to, movingPiece);
    board_.setPiece(move.from, Piece());
    
    // Обновляем состояние игры (права рокировки, en passant и т.д.)
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
    if (algebraicNotation.length() < 4) return false;
    
    Square from = board_.algebraicToSquare(algebraicNotation.substr(0, 2));
    Square to = board_.algebraicToSquare(algebraicNotation.substr(2, 2));
    
    if (from == INVALID_SQUARE || to == INVALID_SQUARE) return false;
    
    // Нам нужно найти Move с правильными флагами (isCastling, isEnPassant)
    MoveGenerator moveGen(board_);
    std::vector<Move> legalMoves = moveGen.generateLegalMoves();
    
    for (const Move& move : legalMoves) {
        if (move.from == from && move.to == to) {
            // Если есть превращение
            if (algebraicNotation.length() >= 5) {
                char p = std::tolower(algebraicNotation[4]);
                PieceType promo = PieceType::EMPTY;
                if (p == 'q') promo = PieceType::QUEEN;
                else if (p == 'r') promo = PieceType::ROOK;
                else if (p == 'b') promo = PieceType::BISHOP;
                else if (p == 'n') promo = PieceType::KNIGHT;
                
                if (move.promotion == promo) {
                    return makeMove(move);
                }
            } else {
                return makeMove(move);
            }
        }
    }
    
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
    Piece movingPiece = board_.getPiece(move.to);
    Color color = movingPiece.getColor();
    int fromRank = board_.rank(move.from);
    int fromFile = board_.file(move.from);
    int toRank = board_.rank(move.to);
    int toFile = board_.file(move.to);

    // 1. Обновление прав на рокировку
    bool whiteKS = board_.canCastleKingSide(Color::WHITE);
    bool whiteQS = board_.canCastleQueenSide(Color::WHITE);
    bool blackKS = board_.canCastleKingSide(Color::BLACK);
    bool blackQS = board_.canCastleQueenSide(Color::BLACK);

    // Если пошел король
    if (movingPiece.getType() == PieceType::KING) {
        if (color == Color::WHITE) {
            whiteKS = whiteQS = false;
        } else {
            blackKS = blackQS = false;
        }
    }

    // Если пошла ладья или ее съели
    if (move.from == board_.square(0, 0) || move.to == board_.square(0, 0)) whiteQS = false;
    if (move.from == board_.square(7, 0) || move.to == board_.square(7, 0)) whiteKS = false;
    if (move.from == board_.square(0, 7) || move.to == board_.square(0, 7)) blackQS = false;
    if (move.from == board_.square(7, 7) || move.to == board_.square(7, 7)) blackKS = false;

    board_.setCastlingRights(whiteKS, whiteQS, blackKS, blackQS);

    // 2. Обновление en passant square
    if (movingPiece.getType() == PieceType::PAWN && std::abs(toRank - fromRank) == 2) {
        board_.setEnPassantSquare(board_.square(fromFile, (fromRank + toRank) / 2));
    } else {
        board_.setEnPassantSquare(INVALID_SQUARE);
    }

    // 3. Обновление счетчика полуходов
    // Сбрасываем счетчик полуходов при взятии или ходе пешки
    // (capturedPiece мы не получили явно в makeMove, но мы можем проверить до выполнения хода или передать инфо)
    // В текущей реализации makeMove мы уже переместили фигуру.
    // Нужно было проверить до board_.setPiece. 
    // Исправим makeMove чуть позже или добавим проверку здесь.
    // Пока считаем что если move.isCapture установлена в MoveGenerator
    if (movingPiece.getType() == PieceType::PAWN || move.isCapture) {
        board_.setHalfMoveClock(0);
    } else {
        board_.setHalfMoveClock(board_.getHalfMoveClock() + 1);
    }
}

bool GameRules::hasLegalMoves(Color color) const {
    // Генерируем все легальные ходы для данного цвета
    MoveGenerator moveGen(board_);
    std::vector<Move> legalMoves = moveGen.generateLegalMoves();
    
    // Фильтруем ходы, оставляя только ходы текущего игрока
    for (const Move& move : legalMoves) {
        Piece piece = board_.getPiece(move.from);
        if (piece.getColor() == color) {
            return true; // Найден хотя бы один легальный ход
        }
    }
    
    return false; // Нет легальных ходов
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