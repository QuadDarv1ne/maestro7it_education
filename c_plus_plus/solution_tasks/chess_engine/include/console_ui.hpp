#ifndef CONSOLE_UI_HPP
#define CONSOLE_UI_HPP

#include "board.hpp"
#include "game_rules.hpp"
#include "minimax.hpp"
#include <string>
#include <vector>

/**
 * Режим игры
 */
enum class GameMode {
    HUMAN_VS_HUMAN,  ///< Человек против человека
    HUMAN_VS_AI,     ///< Человек против ИИ
    AI_VS_AI         ///< ИИ против ИИ
};

/**
 * Тип игрока
 */
enum class PlayerType {
    HUMAN,  ///< Человеческий игрок
    AI      ///< Искусственный интеллект
};

/**
 * @brief Класс, реализующий консольный пользовательский интерфейс для шахмат
 * 
 * Управляет игровым процессом, отображением доски, взаимодействием с пользователем
 * и запуском ИИ-противников
 */
class ConsoleUI {
private:
    Board board_;             ///< Игровая доска
    GameRules rules_;         ///< Правила игры
    Minimax aiEngine_;        ///< ИИ-движок для вычисления ходов
    
    GameMode gameMode_;       ///< Текущий режим игры
    PlayerType whitePlayer_;  ///< Тип игрока за белых
    PlayerType blackPlayer_;  ///< Тип игрока за черных
    
    int aiDifficulty_;        ///< Уровень сложности ИИ (глубина поиска)
    
public:
    ConsoleUI();
    
    // Основной игровой цикл
    void run();                             ///< Запускает главный игровой цикл
    
    // Система меню
    void showMainMenu();                    ///< Отображает главное меню
    void showGameSettings();                ///< Показывает настройки игры
    void startNewGame();                    ///< Начинает новую игру
    
    // Игровой процесс
    void playGame();                        ///< Управляет процессом игры
    Move getPlayerMove(Color playerColor);  ///< Получает ход от игрока-человека
    Move getAIMove(Color playerColor);      ///< Получает ход от ИИ
    
    // Обработка ввода
    Move parseMoveInput(const std::string& input) const;     ///< Парсит строку с ходом
    bool isValidMoveFormat(const std::string& input) const;  ///< Проверяет формат хода
    
    // Методы отображения
    void showBoard() const;                                         ///< Отображает текущее состояние доски
    void showGameStatus() const;                                    ///< Показывает статус игры
    void showAvailableMoves(const std::vector<Move>& moves) const;  ///< Показывает доступные ходы
    void showMessage(const std::string& message) const;             ///< Выводит сообщение
    
    // Настройки
    void configureGameSettings();                             ///< Конфигурирует настройки игры
    void setGameMode(GameMode mode);                          ///< Устанавливает режим игры
    void setPlayerTypes(PlayerType white, PlayerType black);  ///< Устанавливает типы игроков
    void setAIDifficulty(int difficulty);                     ///< Устанавливает сложность ИИ
    
    // Вспомогательные методы
    std::string getColorName(Color color) const;        ///< Возвращает название цвета
    std::string getMoveString(const Move& move) const;  ///< Преобразует ход в строку
    void clearScreen() const;                           ///< Очищает экран консоли
    
private:
    // Вспомогательные методы
    void initializeGame();                                 ///< Инициализирует новую игру
    bool handleSpecialCommands(const std::string& input);  ///< Обрабатывает специальные команды
    void showHelp() const;                                 ///< Показывает справку по командам
};

#endif // CONSOLE_UI_HPP