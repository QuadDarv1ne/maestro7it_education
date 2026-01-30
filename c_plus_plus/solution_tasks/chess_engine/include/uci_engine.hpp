#ifndef UCI_ENGINE_HPP
#define UCI_ENGINE_HPP

#include "board.hpp"
#include "game_rules.hpp"
#include "minimax.hpp"
#include <string>
#include <vector>
#include <map>
#include <thread>
#include <atomic>
#include <iostream>
#include <sstream>
#include <functional>

/**
 * @brief UCI (Universal Chess Interface) протокол
 */
class UCIEngine {
private:
    // Игровые компоненты
    Board board_;
    GameRules gameRules_;
    Minimax minimax_;

    // Состояние двигателя
    std::atomic<bool> running_;
    std::atomic<bool> searching_;
    std::thread searchThread_;
    
    // Параметры поиска
    int searchDepth_;
    int searchTimeMs_;
    bool infiniteSearch_;
    
    // Опции двигателя
    std::map<std::string, std::string> options_;
    
    // Внутренние методы обработки
    void processCommand(const std::string& command);
    void handleUCI();
    void handleIsReady();
    void handleUCINewGame();
    void handlePosition(const std::vector<std::string>& tokens);
    void handleGo(const std::vector<std::string>& tokens);
    void handleStop();
    void handleQuit();
    void handleSetOption(const std::vector<std::string>& tokens);
    
    // Методы вывода
    void sendInfo(const std::string& info);
    void sendBestMove(const std::string& move);
    
    // Поиск
    void startSearch();
    
    // Утилиты
    std::vector<std::string> tokenize(const std::string& input);
    std::string trim(const std::string& str);

public:
    UCIEngine();
    ~UCIEngine();
    
    // Запуск цикла протокола
    void run();
};

#endif // UCI_ENGINE_HPP