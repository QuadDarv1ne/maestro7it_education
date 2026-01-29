#ifndef UCI_ENGINE_HPP
#define UCI_ENGINE_HPP

#include <string>
#include <vector>
#include <map>
#include <iostream>
#include <sstream>
#include <thread>
#include <atomic>

/**
 * @brief UCI (Universal Chess Interface) протокол
 * 
 * Реализация стандартного протокола для взаимодействия с шахматными GUI.
 * Позволяет интеграцию движка с популярными программами: Arena, ChessBase, Fritz и др.
 */
class UCIEngine {
private:
    // Состояние движка
    std::string engineName_;
    std::string engineAuthor_;
    std::atomic<bool> shouldStop_;
    std::atomic<bool> isSearching_;
    
    // Настройки поиска
    int searchDepth_;
    int searchTime_;
    int searchNodes_;
    bool ponder_;
    
    // Опции движка
    std::map<std::string, std::string> options_;
    
    // Текущая позиция
    std::string currentPosition_;
    std::vector<std::string> moveHistory_;
    
public:
    UCIEngine(const std::string& name = "Professional Chess Engine", 
              const std::string& author = "Development Team");
    
    // Основной интерфейс UCI
    void runUCIProtocol();
    void processCommand(const std::string& command);
    
    // Команды UCI
    void handleUCI();
    void handleIsReady();
    void handlePosition(const std::string& command);
    void handleGo(const std::string& command);
    void handleStop();
    void handlePonderHit();
    void handleSetOption(const std::string& command);
    void handleUCINewGame();
    void handleQuit();
    
    // Вспомогательные функции
    std::vector<std::string> parseCommand(const std::string& command);
    std::string getCurrentMove() const;
    void sendInfo(const std::string& info);
    void sendBestMove(const std::string& move);
    
private:
    // Внутренние методы поиска
    std::string findBestMove();
    void startSearch();
    void stopSearch();
    
    // Валидация и парсинг
    bool isValidMove(const std::string& move) const;
    bool isValidFEN(const std::string& fen) const;
    std::string moveToUCI(const std::string& internalMove) const;
    std::string moveFromUCI(const std::string& uciMove) const;
};

// Константы UCI протокола
namespace UCIConstants {
    extern const std::string ENGINE_NAME;
    extern const std::string ENGINE_AUTHOR;
    extern const int DEFAULT_SEARCH_DEPTH;
    extern const int DEFAULT_SEARCH_TIME;
    extern const std::vector<std::string> SUPPORTED_OPTIONS;
}

// Утилиты для работы с UCI
namespace UCIUtils {
    std::vector<std::string> splitString(const std::string& str, char delimiter);
    std::string trimString(const std::string& str);
    bool stringStartsWith(const std::string& str, const std::string& prefix);
    std::string toLowerCase(const std::string& str);
}

#endif // UCI_ENGINE_HPP