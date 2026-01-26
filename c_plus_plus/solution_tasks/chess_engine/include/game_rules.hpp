#ifndef GAME_RULES_HPP
#define GAME_RULES_HPP

#include "board.hpp"
#include "move_generator.hpp"
#include <string>

/**
 * @brief Класс, реализующий правила игры в шахматы
 * 
 * Отвечает за проверку корректности ходов, определение состояния игры,
 * выполнение ходов и проверку условий окончания игры
 */
class GameRules {
private:
    Board& board_;  ///< Ссылка на текущую игровую доску
    
public:
    GameRules(Board& board);
    
    // Проверка ходов
    bool isValidMove(const Move& move) const;  ///< Проверяет корректность хода
    bool isValidMove(const std::string& algebraicNotation) const;  ///< Проверяет корректность хода в алгебраической нотации
    
    // Проверка состояния игры
    bool isCheck(Color color) const;        ///< Проверяет, находится ли король под шахом
    bool isCheckmate(Color color) const;    ///< Проверяет, является ли позиция матом
    bool isStalemate(Color color) const;    ///< Проверяет, является ли позиция патом
    bool isDrawByRepetition() const;        ///< Проверяет ничью по троекратному повторению
    bool isDrawByFiftyMoveRule() const;     ///< Проверяет ничью по правилу 50 ходов
    bool isInsufficientMaterial() const;    ///< Проверяет ничью из-за недостатка материала
    
    // Выполнение ходов
    bool makeMove(const Move& move);  ///< Выполняет ход, если он корректен
    bool makeMove(const std::string& algebraicNotation);  ///< Выполняет ход из алгебраической нотации
    
    // Завершение игры
    bool isGameOver() const;           ///< Проверяет, завершена ли игра
    std::string getGameResult() const; ///< Возвращает результат игры в виде строки
    
    // Вспомогательные методы
    Color getWinner() const;  ///< Возвращает победителя (если игра завершена)
    bool isDraw() const;      ///< Проверяет, завершилась ли игра ничьей
    
private:
    // Вспомогательные методы
    bool wouldLeaveKingInCheck(const Move& move) const;  ///< Проверяет, оставляет ли ход короля под шахом
    void updateGameStateAfterMove(const Move& move);     ///< Обновляет состояние игры после хода
    bool hasLegalMoves(Color color) const;               ///< Проверяет наличие легальных ходов
    int countPieces(Color color) const;                  ///< Подсчитывает количество фигур
    bool onlyKingsRemain() const;                        ///< Проверяет, остались ли на доске только короли
};

#endif // GAME_RULES_HPP